"""签卦接口：64卦/观音灵签/诸葛神算 + AI 解卦。"""
from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.exceptions import BizError, ok
from ..core.deps import get_current_user, get_user_optional
from ..models import Question, User
from ..services import qian as qsv
from ..services import ai
from ..services.beans import charge

router = APIRouter()


def _draw_and_charge(qtype: str, biz: str, things: str, user: User, db: Session):
    cost = charge(db, user, biz, ref_id=qtype, note=things)
    if qtype == "64gua":
        res = qsv.draw_64gua(things)
    elif qtype == "guanyin":
        res = qsv.draw_guanyin(things)
    else:
        res = qsv.draw_zhuge(things)
    q = Question(uid=user.uid, type=qtype, things=things)
    db.add(q)
    db.commit()
    res["beans_cost"] = cost
    return res


@router.get("/qian/64gua/random/q")
def qian_64gua(things: str = "", user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ok(_draw_and_charge("64gua", "qian.64gua", things, user, db))


# 兼容线上别名
@router.get("/qian/guanyin/random/q")
def qian_guanyin(things: str = "", user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ok(_draw_and_charge("guanyin", "qian.guanyin", things, user, db))


@router.get("/qian/zhuGeShenSuan/random/q")
def qian_zhuge(things: str = "", user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ok(_draw_and_charge("zhuge", "qian.zhuge", things, user, db))


# ---------- 已知卦/签的详情 item ----------
@router.get("/fortune/64gua/item/{item_id}")
def gua_item(item_id: int, user=None):
    g = qsv.resolve_gua_item(item_id)
    return ok(g or {"error": "not found"})


@router.get("/fortune/guanyin/item/{item_id}")
def guanyin_item(item_id: int):
    g = qsv.resolve_guanyin_item(item_id)
    return ok(g or {"error": "not found"})


@router.get("/fortune/zhuge/item/{item_id}")
def zhuge_item(item_id: int):
    g = qsv.resolve_zhuge_item(item_id)
    return ok(g or {"error": "not found"})


# ---------- AI 解卦（SSE） ----------
def _ai_stream(qtype: str, things: str, user: User, db: Session):
    draw = _draw_and_charge(qtype, f"qian.{qtype}", things, user, db)

    async def gen():
        system = ("你是一位精通《周易》与传统文化解卦的资深命理师，"
                  "请结合卦象/签文，为用户（所问：%s）提供诚恳、正面、实用的解读。"
                  "用简体中文，分点输出，语气温和有据。" % (things or "未知"))
        prompt = f"卦/签内容：{json.dumps(draw, ensure_ascii=False)[:1200]}"
        yield f"data:{json.dumps({'draw': draw}, ensure_ascii=False)}\n\n"
        try:
            async for delta in ai.stream_chat([{"role": "user", "content": prompt}], system=system):
                yield f"data:{json.dumps({'text': delta}, ensure_ascii=False)}\n\n"
        except ai.AINotConfigured as e:
            yield f"data:{json.dumps({'error': ai.ai_error_message()}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data:{json.dumps({'error': '生成失败：' + str(e)[:100]}, ensure_ascii=False)}\n\n"
        yield "data:[DONE]\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@router.get("/qian/64gua/random/ai/stream")
def qian_64gua_ai_stream(things: str = "", user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    return _ai_stream("64gua", things, user, db)


@router.get("/qian/guanyin/random/ai/stream")
def qian_guanyin_ai_stream(things: str = "", user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    return _ai_stream("guanyin", things, user, db)


@router.get("/qian/zhuGeShenSuan/random/ai/stream")
def qian_zhuge_ai_stream(things: str = "", user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    return _ai_stream("zhuge", things, user, db)


@router.get("/question/records")
def question_records(page: int = 1, size: int = 20,
                     user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.uid == user.uid).order_by(Question.id.desc())
    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()
    return ok({"total": total, "page": page, "size": size,
               "items": [{"id": x.id, "type": x.type, "things": x.things,
                          "created_at": str(x.created_at)} for x in items]})
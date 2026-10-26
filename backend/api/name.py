"""姓名/手机/起名 + 工具历史。"""
from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.deps import get_current_user
from ..core.exceptions import ok
from ..models import ToolHistory, User
from ..schemas import NameOptReq
from ..services import ai
from ..services.beans import charge

router = APIRouter()


@router.get("/analysis/name/stream")
def name_analysis_stream(name: str = "", user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    charge(db, user, "name.nameAnalysis", note=name)
    rec = ToolHistory(uid=user.uid, tool="nameAnalysis", input=name, result="{}")
    db.add(rec)
    db.commit()

    async def gen():
        system = "你是姓名学专家，请分析该姓名的五行数理与寓意，给出积极建议。简体中文，分点。"
        try:
            async for delta in ai.stream_chat([{"role": "user", "content": f"请分析姓名：{name}"}], system=system):
                yield f"data:{json.dumps({'text': delta}, ensure_ascii=False)}\n\n"
        except ai.AINotConfigured:
            yield f"data:{json.dumps({'error': ai.ai_error_message()}, ensure_ascii=False)}\n\n"
        yield "data:[DONE]\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")


@router.get("/baxing/phoneNumber/{phone}")
def phone_analysis(phone: str, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    charge(db, user, "name.phone", note=phone)
    # 简化数理吉凶：号码数字和
    s = sum(int(c) for c in phone if c.isdigit())
    luck = "吉" if s % 2 == 0 else "中"
    result = {"phone": phone, "digits": s, "five": _phone_wuxing(phone),
              "interpret": f"号码数字和为 {s}，主{luck}。宜多行善积德，趋吉避凶。"}
    db.add(ToolHistory(uid=user.uid, tool="phone", input=phone, result=json.dumps(result)))
    db.commit()
    return ok(result)


def _phone_wuxing(phone: str):
    map5 = ["水", "木", "火", "土", "金"]
    digits = [int(c) for c in phone if c.isdigit()]
    return "".join(map5[d % 5] for d in digits[:6])


@router.post("/name-opt")
def name_opt(body: NameOptReq, user: User = Depends(get_current_user),
             db: Session = Depends(get_db)):
    charge(db, user, "name.nameOpt", note=body.surname)
    names = _generate_names(body.surname, body.gender, body.count)
    db.add(ToolHistory(uid=user.uid, tool="nameOpt", input=body.surname,
                       result=json.dumps({"names": names})))
    db.commit()
    return ok({"names": names, "style": body.style})


def _generate_names(surname, gender, count):
    from random import shuffle
    mid = list("一二三四五六七八九十子安之若依云舒朗逸永嘉真如清和明德") if gender == "male" \
        else list("静婉淑雅兰芳欣悦慧琳雪晴语颖梦蝶安然")
    tail = list("轩宇天翊泽言宏亦凡霖柏峻涛洋江") if gender == "male" \
        else list("妍汐妡露兰芷清莹柔懿菁薇")
    names = []
    for _ in range(count):
        names.append(f"{surname}{_pick(mid)}{_pick(tail)}")
    return names


def _pick(seq):
    import random
    return random.choice(seq)


@router.get("/tool-history")
def tool_history(page: int = 1, size: int = 20,
                 user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = db.query(ToolHistory).filter(ToolHistory.uid == user.uid).order_by(ToolHistory.id.desc())
    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()
    return ok({"total": total, "page": page, "size": size,
               "items": [{"id": t.id, "tool": t.tool, "input": t.input,
                          "result": t.result, "created_at": str(t.created_at)} for t in items]})


@router.delete("/tool-history/{history_id}")
def delete_tool_history(history_id: int, user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    db.query(ToolHistory).filter(ToolHistory.id == history_id, ToolHistory.uid == user.uid).delete()
    db.commit()
    return ok({"deleted": history_id})
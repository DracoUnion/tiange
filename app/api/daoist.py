"""AI 道长（流式对话）。"""
from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.deps import get_current_user
from ..core.exceptions import ok
from ..models import DaoistMessage, User
from ..schemas import DaoistChatReq
from ..services import ai

router = APIRouter()

_SYSTEM = ("你是天格的「天格道长」，一位通达《道德经》与道家智慧的智者。"
           "用温和、沉稳、富有哲理又不失落地的语气，与用户交流人生、情绪与选择。"
           "回答使用简体中文，篇幅适中，可引用经句并给出行动建议。")


@router.post("/daoist/chat/stream")
def daoist_chat_stream(body: DaoistChatReq, user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    db.add(DaoistMessage(uid=user.uid, role="user", content=body.message))
    db.commit()

    async def gen():
        try:
            async for delta in ai.stream_chat([{"role": "user", "content": body.message}],
                                               system=_SYSTEM, max_tokens=800):
                yield f"data:{json.dumps({'text': delta}, ensure_ascii=False)}\n\n"
        except ai.AINotConfigured:
            yield f"data:{json.dumps({'error': ai.ai_error_message()}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data:{json.dumps({'error': '生成失败：' + str(e)[:100]}, ensure_ascii=False)}\n\n"
        yield "data:[DONE]\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")


@router.get("/daoist/messages")
def daoist_messages(page: int = 1, size: int = 50,
                    user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = db.query(DaoistMessage).filter(DaoistMessage.uid == user.uid).order_by(DaoistMessage.id.desc())
    total = q.count()
    items = q.offset(max(0, total - size)).limit(size).all()
    return ok({"total": total, "items": [{"role": m.role, "content": m.content,
                                          "created_at": str(m.created_at)} for m in items]})


@router.get("/daoist/references")
def daoist_references(user: User = Depends(get_current_user)):
    return ok({"sources": ["《道德经》", "《阴符经》", "《周易》"]})
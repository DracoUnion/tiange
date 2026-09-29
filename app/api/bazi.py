"""八字排盘与称骨。"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.deps import get_current_user, get_user_optional
from ..core.exceptions import ok, http400
from ..models import Member, User
from ..schemas import BaziReq, ChengguReq
from ..services import bazi as bz, chenggu as cg, lunisolar as L, ai
from ..services.beans import charge

router = APIRouter()


@router.get("/bazi/pan")
def bazi_pan(params: BaziReq = Depends()):
    spec = L.member_spec_from_params(params.calendar, params.year, params.month,
                                     params.day, params.hour, params.gender)
    pan = bz.compute(spec)
    return ok(pan)


@router.get("/chenggu")
def chenggu(params: ChengguReq = Depends()):
    result = cg.compute(params.calendar, params.year, params.month, params.day, params.hour)
    return ok(result)


@router.post("/bazi/analysis/ai")
async def bazi_analysis(body: dict, user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    charge(db, user, "fortune.thisYear", note="八字AI分析")
    db.commit()
    spec = L.member_spec_from_params(body.get("calendar", "solar"), int(body.get("year", 1990)),
                                     int(body.get("month", 1)), int(body.get("day", 1)),
                                     int(body.get("hour", 0)), body.get("gender", "male"))
    pan = bz.compute(spec)
    system = "你是一位资深八字命理师。请结合四柱十神，给出恳切、积极、可落实的分析。简体中文。"
    text = await ai.complete([{"role": "user", "content":
        f"人物八字：{spec}，排盘：{pan}。请分析其性格、事业、财运、感情与健康。"}], system=system)
    return ok({"analysis": text})


@router.get("/bazi/createNameStream")
def create_name_stream(name: str = ""):
    return ok({"name": name})


# SSE：八字分析（兼容流式）
@router.post("/bazi/analysis/stream")
async def bazi_analysis_stream(body: dict, user: User = Depends(get_current_user)):
    spec = L.member_spec_from_params(body.get("calendar", "solar"), int(body.get("year", 1990)),
                                     int(body.get("month", 1)), int(body.get("day", 1)),
                                     int(body.get("hour", 0)), body.get("gender", "male"))
    pan = bz.compute(spec)

    async def gen():
        system = "你是资深八字命理师，请基于排盘给出积极诚恳的分点分析。简体中文。"
        try:
            async for delta in ai.stream_chat(
                    [{"role": "user", "content": f"排盘：{pan}"}], system=system):
                yield f"data:{__import__('json').dumps({'text': delta}, ensure_ascii=False)}\n\n"
        except ai.AINotConfigured:
            yield f"data:{__import__('json').dumps({'error': ai.ai_error_message()}, ensure_ascii=False)}\n\n"
        yield "data:[DONE]\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")
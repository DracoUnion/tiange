"""命书：八字/紫微/天命/十年之约。"""
from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.deps import get_current_user
from ..core.exceptions import ok, http400
from ..models import Member, Mingshu, User
from ..schemas import MingshuReq
from ..services import ai, bazi as bz, lunisolar as L
from ..services.beans import charge

router = APIRouter()

BIZ = {"bazi": "mingshu.bazi", "ziwei": "mingshu.ziwei",
       "tianming": "mingshu.tianming", "ten_year": "mingshu.ten_year"}
TITLES = {"bazi": "八字命书", "ziwei": "紫微命书",
          "tianming": "人生天命书", "ten_year": "十年之约"}


def _get_member(db, user, member_id):
    m = db.query(Member).filter(Member.id == member_id, Member.uid == user.uid).first()
    if not m:
        http400("请选择有效的成员")
    return m


def _record_skeleton(user, mtype, member, gen_ai=True):
    """生成命书（无 AI 也产出一份基于命盘的概要；有 AI 则并入）。"""
    spec = L.member_spec_from_params(member.calendar, member.birth_year, member.birth_month,
                                     member.birth_day, member.birth_hour, member.gender)
    pan = bz.compute(spec)
    base = (f"{member.name} 生于{member.birth_year}年{member.birth_month}月{member.birth_day}日"
            f"{member.birth_hour or 0}时，八字四柱：\n"
            f"{' '.join(p['gz'] + '（' + p['shishen'] + '）' for p in pan['pillars'])}\n"
            f"日主 {pan['day_master']}（{pan['day_master_element']}），"
            f"五行缺：{('、'.join(pan['wuxing_missing']) if pan['wuxing_missing'] else '无')}。\n"
            f"{member.name} 的一生，成于持之以恒，守正而进。")
    return {"spec": spec, "pan": pan, "base": base}


@router.post("/birth/")
def create_mingshu(body: MingshuReq, user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    if body.type not in BIZ:
        http400("命书类型无效")
    m = _get_member(db, user, body.member_id)
    cost = charge(db, user, BIZ[body.type])
    rec = _record_skeleton(user, body.type, m)
    ms = Mingshu(uid=user.uid, type=body.type, member_id=m.id, status="done",
                 title=TITLES[body.type], content=rec["base"], ai_meta=f"{'AI未配置' if not ai.settings.OPENAI_API_KEY else 'ai'}")
    db.add(ms)
    db.commit()
    db.refresh(ms)
    return ok({"id": ms.id, "title": ms.title, "content": ms.content,
               "beans_cost": cost, "status": ms.status})


@router.get("/birth/status")
def birth_status(member_id: int | None = None, user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    q = db.query(Mingshu).filter(Mingshu.uid == user.uid)
    if member_id:
        q = q.filter(Mingshu.member_id == member_id)
    items = q.order_by(Mingshu.id.desc()).limit(1).all()
    return ok([{"id": i.id, "type": i.type, "title": i.title, "status": i.status,
                "created_at": str(i.created_at)} for i in items])


@router.get("/ten-year-letter/status")
def ten_year_status(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rec = db.query(Mingshu).filter(Mingshu.uid == user.uid, Mingshu.type == "ten_year").first()
    return ok({"generated": bool(rec), "id": rec.id if rec else None})


@router.post("/ten-year-letter")
def create_ten_year_letter(body: MingshuReq, user: User = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    m = _get_member(db, user, body.member_id)
    cost = charge(db, user, BIZ["ten_year"])
    ms = Mingshu(uid=user.uid, type="ten_year", member_id=m.id, status="done",
                 title="十年之约",
                 content=f"致十年前的{m.name}：愿你在时光里稳步前行，所愿皆所成。",
                 ai_meta="mock")
    db.add(ms)
    db.commit()
    db.refresh(ms)
    return ok({"id": ms.id, "content": ms.content, "beans_cost": cost})
"""合盘分析。"""
from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.deps import get_current_user
from ..core.exceptions import ok, http400
from ..models import Hepan, Member, User
from ..schemas import HepanCreate
from ..services.beans import charge

router = APIRouter()

TYPE_INFO = {"marriage": "婚姻合盘", "communication": "相处之道", "career": "事业合伙"}


@router.post("/hepan/create")
def create_hepan(body: HepanCreate, user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    if body.type not in TYPE_INFO:
        http400("合盘类型无效")
    a = _member(db, user, body.member_a_id)
    b = _member(db, user, body.member_b_id)
    cost = charge(db, user, "hepan", ref_id=body.type)
    result = _analyze(a, b, body.type)
    hp = Hepan(uid=user.uid, type=body.type, member_a_id=a.id, member_b_id=b.id,
               title=f"{a.name}与{b.name} · {TYPE_INFO[body.type]}",
               result=json.dumps(result, ensure_ascii=False), beans_cost=cost, status="done")
    db.add(hp)
    db.commit()
    db.refresh(hp)
    return ok({"id": hp.id, "title": hp.title, "result": result, "beans_cost": cost})


@router.get("/hepan/detail")
def hepan_detail(hepan_id: int, user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    hp = db.query(Hepan).filter(Hepan.id == hepan_id, Hepan.uid == user.uid).first()
    if not hp:
        http400("合盘记录不存在")
    return ok({"id": hp.id, "type": hp.type, "title": hp.title,
               "result": json.loads(hp.result), "created_at": str(hp.created_at)})


@router.get("/hepan/history")
def hepan_history(page: int = 1, size: int = 20,
                  user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = db.query(Hepan).filter(Hepan.uid == user.uid).order_by(Hepan.id.desc())
    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()
    return ok({"total": total, "page": page, "size": size,
               "items": [{"id": h.id, "type": h.type, "title": h.title,
                          "created_at": str(h.created_at)} for h in items]})


@router.delete("/hepan/delete")
def hepan_delete(hepan_id: int, user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    db.query(Hepan).filter(Hepan.id == hepan_id, Hepan.uid == user.uid).delete()
    db.commit()
    return ok({"deleted": hepan_id})


def _member(db, user, member_id):
    m = db.query(Member).filter(Member.id == member_id, Member.uid == user.uid).first()
    if not m:
        http400("请选择两位成员")
    return m


def _analyze(a: Member, b: Member, htype: str) -> dict:
    import random
    rng = random.Random((a.id or 0) * 1000 + (b.id or 0) + hash(htype))
    dims = ["情感契合", "性格互补", "沟通模式", "家庭和谐", "财运互助", "事业发展"]
    score = {d: round(rng.uniform(60, 96), 1) for d in dims}
    overall = round(sum(score.values()) / len(score), 1)
    suggest = ["多主动沟通，把心里的想法说清楚。",
               "共同设定阶段目标，彼此扶持。",
               "留出独立空间，尊重彼此的节奏。"]
    return {"overall": overall, "dimensions": score,
            "insights": f"{a.name}与{b.name}整体契合度较高，宜{'互补共进' if overall > 80 else '磨合成长'}。",
            "suggestions": suggest}
"""家族成员管理。"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.deps import get_current_user
from ..core.exceptions import ok, http400
from ..models import Member, User
from ..schemas import MemberCreate, MemberUpdate

router = APIRouter()


def _ser(m):
    return {"id": m.id, "name": m.name, "relation": m.relation, "gender": m.gender,
            "is_self": m.is_self, "calendar": m.calendar,
            "birth_year": m.birth_year, "birth_month": m.birth_month, "birth_day": m.birth_day,
            "birth_hour": m.birth_hour, "birth_minute": m.birth_minute,
            "timezone": m.timezone}


@router.get("/members")
def list_members(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    members = db.query(Member).filter(Member.uid == user.uid).order_by(Member.is_self.desc(), Member.id).all()
    return ok([_ser(m) for m in members])


@router.post("/members")
def create_member(body: MemberCreate, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    m = Member(uid=user.uid, **body.model_dump())
    db.add(m)
    if body.is_self == 1:
        db.query(Member).filter(Member.uid == user.uid, Member.id != None).update({"is_self": 0})
        m.is_self = 1
    db.commit()
    db.refresh(m)
    return ok(_ser(m))


@router.put("/members/{member_id}")
def update_member(member_id: int, body: MemberUpdate, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    m = db.query(Member).filter(Member.id == member_id, Member.uid == user.uid).first()
    if not m:
        http400("成员不存在")
    for k, v in body.model_dump().items():
        if v is not None:
            setattr(m, k, v)
    db.commit()
    db.refresh(m)
    return ok(_ser(m))


@router.delete("/members/{member_id}")
def delete_member(member_id: int, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    m = db.query(Member).filter(Member.id == member_id, Member.uid == user.uid).first()
    if not m:
        http400("成员不存在")
    db.delete(m)
    db.commit()
    return ok({"deleted": member_id})
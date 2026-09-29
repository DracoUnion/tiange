"""运势接口。"""
from __future__ import annotations

import datetime as dt

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.deps import get_current_user, get_user_optional
from ..core.exceptions import ok, http400
from ..models import Member, User
from ..services import fortune as fsv
from ..services.beans import charge

router = APIRouter()

KIND_MAP = {
    "today": ("fortune.today", "%Y-%m-%d"),
    "thisWeek": ("fortune.thisWeek", "%Y-%m-%d"),
    "thisMonth": ("fortune.thisMonth", "%Y-%m-%d"),
    "thisYear": ("fortune.thisYear", "%Y-%m-%d"),
    "thisDayun": ("fortune.thisDayun", "%Y-%m-%d"),
    "oneLife": ("fortune.oneLife", "%Y-%m-%d"),
}


def _member_input(db, user, member_id):
    if not member_id:
        m = db.query(Member).filter(Member.uid == user.uid, Member.is_self == 1).first() \
            or db.query(Member).filter(Member.uid == user.uid).first()
    else:
        m = db.query(Member).filter(Member.id == member_id, Member.uid == user.uid).first()
    if not m:
        http400("请先创建成员信息", "需要先添加出生信息成员")
    return m


def _do_fortune(kind: str, member_id: int | None, target_date: str | None,
                user: User, db: Session):
    biz, _ = KIND_MAP[kind]
    m = _member_input(db, user, member_id)
    tdate = target_date or dt.date.today().strftime("%Y-%m-%d")
    charge(db, user, biz, ref_id=f"fortune-{kind}")
    fmin = fsv.member_to_fortune_input(m)
    result = fsv.generate(kind, fmin, tdate)
    db.commit()
    return result


@router.get("/fortune/today")
def today(member_id: int | None = None, target_date: str | None = None,
          user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ok(_do_fortune("today", member_id, target_date, user, db))


@router.get("/fortune/thisWeek")
def this_week(member_id: int | None = None, target_date: str | None = None,
              user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ok(_do_fortune("thisWeek", member_id, target_date, user, db))


@router.get("/fortune/thisMonth")
def this_month(member_id: int | None = None, target_date: str | None = None,
               user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ok(_do_fortune("thisMonth", member_id, target_date, user, db))


@router.get("/fortune/thisYear")
def this_year(member_id: int | None = None, target_date: str | None = None,
              user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ok(_do_fortune("thisYear", member_id, target_date, user, db))


@router.get("/fortune/thisDayun")
def this_dayun(member_id: int | None = None, target_date: str | None = None,
               user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ok(_do_fortune("thisDayun", member_id, target_date, user, db))


@router.get("/fortune/oneLife")
def one_life(member_id: int | None = None, target_date: str | None = None,
             user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ok(_do_fortune("oneLife", member_id, target_date, user, db))
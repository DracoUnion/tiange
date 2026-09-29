"""用户中心。"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.deps import get_current_user, get_user_optional
from ..core.exceptions import ok, http400
from ..core.security import gen_uid
from ..models import User
from ..schemas import (SolarToLunarReq, UserInfoUpdate, MemberCreate)
from ..services import lunisolar as L
from ..services.beans import get_or_create_account

router = APIRouter()


@router.get("/user/detail")
def user_detail(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = get_or_create_account(db, user.uid)
    return ok({
        "uid": user.uid, "username": user.username, "email": user.email,
        "nickname": user.nickname, "avatar": user.avatar, "lang": user.lang,
        "vip_level": user.vip_level, "vip_expire_at": str(user.vip_expire_at or ""),
        "beans": acc.balance, "invite_code": user.invite_code,
    })


@router.get("/user/info")
def user_info(user: User = Depends(get_current_user)):
    return ok({"nickname": user.nickname, "avatar": user.avatar, "lang": user.lang})


@router.put("/user/info")
def update_info(body: UserInfoUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if body.nickname is not None:
        user.nickname = body.nickname
    if body.avatar is not None:
        user.avatar = body.avatar
    if body.lang is not None:
        user.lang = body.lang
    db.commit()
    return ok({"nickname": user.nickname})


@router.get("/user/entitlements")
def entitlements(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = get_or_create_account(db, user.uid)
    return ok({
        "beans": acc.balance,
        "vip_level": user.vip_level,
        "vip_expire_at": str(user.vip_expire_at or ""),
        "daily_free": {"fortune.today": 1, "qian.64gua": 1},
    })


@router.get("/user/invitation/code")
def my_invite_code(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.invite_code:
        user.invite_code = gen_uid()[:8]
        db.commit()
    return ok({"code": user.invite_code})


@router.get("/user/invitation/records")
def invite_records(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    invited = db.query(User).filter(User.invited_by == user.invite_code).all()
    return ok([{"username": u.username, "created_at": str(u.created_at)} for u in invited])


@router.get("/user/solar-to-lunar")
def solar_to_lunar(params: SolarToLunarReq = Depends()):
    lunar = L.solar_to_lunar(params.year, params.month, params.day)
    return ok(lunar)
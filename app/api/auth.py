"""认证：注册/登录/登出/改密/邮箱验证码/验证码。"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..core import captcha as cap
from ..core.db import get_db
from ..core.deps import get_current_user
from ..core.exceptions import BizError, ok, http400
from ..core.security import create_access_token, gen_uid, hash_password, verify_password
from ..models import User
from ..schemas import (EmailCodeApplyReq, EmailCodeVerifyReq, LoginReq,
                       RegisterReq, ResetPasswordReq)
from ..services import email as email_svc
from ..services.beans import grant_bonus
from ..core.config import settings

router = APIRouter()


def _token(user: User) -> dict:
    return {"token": create_access_token(user.uid), "uid": user.uid,
            "username": user.username, "nickname": user.nickname}


@router.get("/captcha")
def get_captcha():
    return ok(cap.create_captcha())


@router.post("/captcha/verify")
def verify_captcha(body: dict):
    if cap.verify_captcha(body.get("captcha_id", ""), body.get("answer", "")):
        return ok({"valid": True})
    return ok({"valid": False})


@router.post("/register")
def register(body: RegisterReq, db: Session = Depends(get_db)):
    if not cap.verify_captcha(body.captcha_id, body.captcha_answer):
        http400("验证码错误", "验证码不正确或已过期")
    if db.query(User).filter(User.username == body.username).first():
        http400("用户名已存在", "该用户名已被注册")
    if body.email and db.query(User).filter(User.email == body.email).first():
        http400("邮箱已存在", "该邮箱已被注册")
    user = User(uid=gen_uid(), username=body.username, email=body.email or None,
                password_hash=hash_password(body.password),
                nickname=body.username, invite_code=gen_uid()[:8],
                invited_by=body.invite_code)
    db.add(user)
    db.flush()
    grant_bonus(db, user.uid, settings.REGISTER_BONUS_BEANS, "register", "首次注册赠送")
    # 邀请奖励
    if body.invite_code:
        inviter = db.query(User).filter(User.invite_code == body.invite_code).first()
        if inviter:
            grant_bonus(db, inviter.uid, settings.INVITE_BONUS_BEANS, "invite", f"邀请 {user.username}")
    db.commit()
    db.refresh(user)
    return ok(_token(user), "注册成功，赠送50心识豆")


@router.post("/login")
def login(body: LoginReq, db: Session = Depends(get_db)):
    if not cap.verify_captcha(body.captcha_id, body.captcha_answer):
        http400("验证码错误", "验证码不正确或已过期")
    user = (db.query(User).filter(User.username == body.account).first()
            or db.query(User).filter(User.email == body.account).first())
    if not user or not verify_password(body.password, user.password_hash):
        http400("用户名或密码错误", "账号或密码不正确")
    if user.status != 1:
        http400("账号已禁用")
    return ok(_token(user), "登录成功")


@router.post("/logout")
def logout(user: User = Depends(get_current_user)):
    return ok({"uid": user.uid}, "已退出登录")


@router.post("/email/code/apply")
def email_code_apply(body: EmailCodeApplyReq):
    email_svc.apply_code(body.email, body.purpose)
    return ok({"sent": True}, "验证码已发送")


@router.post("/email/code/verify")
def email_code_verify(body: EmailCodeVerifyReq):
    valid = email_svc.verify_code(body.email, "reset", body.code) or \
            email_svc.verify_code(body.email, "register", body.code)
    return ok({"valid": valid})


@router.post("/reset-password")
def reset_password(body: ResetPasswordReq, db: Session = Depends(get_db)):
    if not email_svc.verify_code(body.email, "reset", body.code):
        http400("验证码错误", "验证码不正确或已过期")
    user = db.query(User).filter(User.email == body.email).first()
    if not user:
        http400("邮箱未注册")
    user.password_hash = hash_password(body.new_password)
    db.commit()
    return ok({"reset": True}, "密码已重置")
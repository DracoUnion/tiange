"""FastAPI 依赖：当前用户、可选用户、成员归属。"""
from __future__ import annotations

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.exceptions import NotAuthorized
from ..core.security import decode_token
from ..models import User


def _bearer_token(request: Request) -> str | None:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:]
    return auth or None


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = _bearer_token(request)
    payload = decode_token(token) if token else None
    if not payload:
        raise NotAuthorized(request.url.path)
    uid = payload.get("sub")
    user = db.query(User).filter(User.uid == uid, User.status == 1).first()
    if not user:
        raise NotAuthorized(request.url.path)
    user._db = db  # 便于 service 复用会话
    return user


def get_user_optional(request: Request, db: Session = Depends(get_db)) -> User | None:
    token = _bearer_token(request)
    payload = decode_token(token) if token else None
    if not payload:
        return None
    uid = payload.get("sub")
    user = db.query(User).filter(User.uid == uid, User.status == 1).first()
    if user:
        user._db = db
    return user
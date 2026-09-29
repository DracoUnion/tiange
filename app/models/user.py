from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import mapped_column

from ..core.db import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(64), unique=True, index=True, nullable=False)
    username = mapped_column(String(64), unique=True, index=True, nullable=False)
    email = mapped_column(String(128), unique=True, nullable=True)
    phone = mapped_column(String(32), unique=True, nullable=True)
    password_hash = mapped_column(String(255), nullable=False)
    nickname = mapped_column(String(64), nullable=True)
    avatar = mapped_column(String(255), nullable=True)
    status = mapped_column(Integer, default=1)  # 1 正常 0 禁用
    vip_level = mapped_column(String(16), default="free")
    vip_expire_at = mapped_column(DateTime, nullable=True)
    invite_code = mapped_column(String(16), unique=True, nullable=True)
    invited_by = mapped_column(String(64), nullable=True)  # 邀请人 uid
    lang = mapped_column(String(8), default="zh-Hans")
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import mapped_column

from ..core.db import Base


class Member(Base):
    """家族成员（出生信息），作为运势/命书/合盘的输入。"""
    __tablename__ = "members"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(64), index=True, nullable=False)      # 归属用户
    name = mapped_column(String(64), nullable=False)
    relation = mapped_column(String(32), default="self")             # self/父/母/子女/伴侣/朋友...
    gender = mapped_column(String(8), default="male")                # male/female
    is_self = mapped_column(Integer, default=0)
    calendar = mapped_column(String(8), default="solar")             # solar/lunar
    birth_year = mapped_column(Integer, nullable=False)
    birth_month = mapped_column(Integer, nullable=False)
    birth_day = mapped_column(Integer, nullable=False)
    birth_hour = mapped_column(Integer, default=0)                   # 0-23
    birth_minute = mapped_column(Integer, default=0)
    timezone = mapped_column(String(32), default="Asia/Shanghai")
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class MemberSpec:
    """从生日推导出的命理参数（八字/干支等），便于在服务间传递。"""
    pass
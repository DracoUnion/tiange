from __future__ import annotations

from datetime import datetime, date

from sqlalchemy import DateTime, Integer, String, Numeric, func
from sqlalchemy.orm import mapped_column

from ..core.db import Base


class BeansAccount(Base):
    """心识豆余额（每个用户一条）。"""
    __tablename__ = "beans_accounts"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(64), unique=True, index=True, nullable=False)
    balance = mapped_column(Integer, default=0)
    total_consumed = mapped_column(Integer, default=0)
    total_recharged = mapped_column(Integer, default=0)
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class BeansLog(Base):
    """心识豆流水。"""
    __tablename__ = "beans_logs"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(64), index=True, nullable=False)
    delta = mapped_column(Integer, nullable=False)          # 正=收入 负=消费
    balance_after = mapped_column(Integer, default=0)
    reason = mapped_column(String(64), default="")          # recharge/consume/register/redeem/invite
    ref_type = mapped_column(String(64), default="")        # fortune.today / paipan.liuyao ...
    ref_id = mapped_column(String(64), default="")
    note = mapped_column(String(255), default="")
    created_at = mapped_column(DateTime, server_default=func.now())


class BeansPackage(Base):
    """充值档位。"""
    __tablename__ = "beans_packages"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(64), nullable=False)
    beans = mapped_column(Integer, nullable=False)
    price_cny = mapped_column(Numeric(10, 2), nullable=False)
    bonus = mapped_column(Integer, default=0)
    sort = mapped_column(Integer, default=0)
    active = mapped_column(Integer, default=1)


class BeanCode(Base):
    """兑换码。"""
    __tablename__ = "bean_codes"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    code = mapped_column(String(64), unique=True, index=True, nullable=False)
    beans = mapped_column(Integer, nullable=False)
    used_by = mapped_column(String(64), nullable=True)
    used_at = mapped_column(DateTime, nullable=True)
    created_at = mapped_column(DateTime, server_default=func.now())
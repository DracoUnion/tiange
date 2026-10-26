from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import mapped_column

from ..core.db import Base


class VipTier(Base):
    """VIP 等级定义与权益（折扣、每日免费加成等）。"""
    __tablename__ = "vip_tiers"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    level = mapped_column(String(16), unique=True, nullable=False)   # free/vip1/vip2/vip3
    name = mapped_column(String(32), nullable=False)
    price_monthly_cny = mapped_column(Numeric(10, 2), default=0)
    price_yearly_cny = mapped_column(Numeric(10, 2), default=0)
    discount = mapped_column(Numeric(4, 2), default=1.00)            # 豆消耗折扣 0.8=8折
    daily_quota_bonus = mapped_column(Integer, default=0)            # 每日免费次数加成
    beans_monthly = mapped_column(Integer, default=0)                # 每月赠送豆
    sort = mapped_column(Integer, default=0)


class VipOrder(Base):
    """VIP 开通订单（本地占位支付）。"""
    __tablename__ = "vip_orders"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_no = mapped_column(String(64), unique=True, index=True, nullable=False)
    uid = mapped_column(String(64), index=True, nullable=False)
    tier = mapped_column(String(16), nullable=False)
    period = mapped_column(String(16), default="monthly")           # monthly/yearly
    amount_cny = mapped_column(Numeric(10, 2), default=0)
    status = mapped_column(String(16), default="paid")              # paid 本地直接成功
    created_at = mapped_column(DateTime, server_default=func.now())
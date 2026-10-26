from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import mapped_column

from ..core.db import Base


class Hepan(Base):
    """合盘分析（婚姻/相处/事业）。"""
    __tablename__ = "hepan"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(64), index=True, nullable=False)
    type = mapped_column(String(32), nullable=False)        # marriage / communication / career
    member_a_id = mapped_column(Integer, nullable=True)
    member_b_id = mapped_column(Integer, nullable=True)
    title = mapped_column(String(128), default="")
    result = mapped_column(Text, default="{}")              # JSON 维度结果
    report = mapped_column(Text, default="")                # AI 长文
    beans_cost = mapped_column(Integer, default=0)
    status = mapped_column(String(16), default="done")
    created_at = mapped_column(DateTime, server_default=func.now())
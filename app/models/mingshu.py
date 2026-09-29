from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import mapped_column

from ..core.db import Base


class Mingshu(Base):
    """命书（八字命书/紫微命书/人生天命书/十年之约）。生成后免费回看。"""
    __tablename__ = "mingshu"
    __table_args__ = (UniqueConstraint("uid", "type", "member_id", name="uq_ms_uid_type_member"),)

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(64), index=True, nullable=False)
    type = mapped_column(String(32), nullable=False)    # bazi / ziwei / tianming / ten_year
    member_id = mapped_column(Integer, nullable=True)
    status = mapped_column(String(16), default="done")  # generating/done/failed
    title = mapped_column(String(128), default="")
    content = mapped_column(Text, default="")
    ai_meta = mapped_column(Text, default="{}")
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
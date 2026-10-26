from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import mapped_column

from ..core.db import Base


class ContentSafetyLog(Base):
    """内容安全审核记录。"""
    __tablename__ = "content_safety_logs"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(64), nullable=True)
    content = mapped_column(Text, default="")
    result = mapped_column(String(16), default="pass")       # pass / block / review
    reason = mapped_column(String(255), default="")
    created_at = mapped_column(DateTime, server_default=func.now())
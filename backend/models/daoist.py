from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import mapped_column

from ..core.db import Base


class DaoistMessage(Base):
    """AI 道长对话消息。"""
    __tablename__ = "daoist_messages"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(64), index=True, nullable=False)
    role = mapped_column(String(16), nullable=False)        # user / assistant
    content = mapped_column(Text, default="")
    references = mapped_column(Text, default="{}")
    created_at = mapped_column(DateTime, server_default=func.now())
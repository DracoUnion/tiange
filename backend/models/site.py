from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import mapped_column

from ..core.db import Base


class SiteStats(Base):
    """站点统计（访问/接口）。"""
    __tablename__ = "site_stats"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    stat_date = mapped_column(String(16), index=True, nullable=False)   # YYYY-MM-DD
    hour = mapped_column(Integer, default=-1)                            # -1 表示全天
    pageviews = mapped_column(Integer, default=0)
    visits = mapped_column(Integer, default=0)
    updated_at = mapped_column(DateTime, server_default=func.now())
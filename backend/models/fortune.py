from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import mapped_column

from ..core.db import Base


class FortuneRecord(Base):
    """运势/占卜结果记录（对应 question/records）。"""
    __tablename__ = "fortune_records"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(64), index=True, nullable=False)
    member_id = mapped_column(Integer, nullable=True)
    type = mapped_column(String(64), index=True, nullable=False)     # fortune.today / qian.64gua ...
    question = mapped_column(String(512), default="")
    payload = mapped_column(Text, default="{}")                      # JSON 结果
    beans_cost = mapped_column(Integer, default=0)
    created_at = mapped_column(DateTime, server_default=func.now())


class Question(Base):
    """占卜提问（含 AI 解卦上下文）。"""
    __tablename__ = "questions"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(64), index=True, nullable=False)
    type = mapped_column(String(64), nullable=False)
    things = mapped_column(String(512), default="")
    answer = mapped_column(Text, default="")
    ai_text = mapped_column(Text, default="")
    created_at = mapped_column(DateTime, server_default=func.now())


class ToolHistory(Base):
    """起名/姓名/手机 等工具分析记录。"""
    __tablename__ = "tool_history"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid = mapped_column(String(64), index=True, nullable=False)
    tool = mapped_column(String(64), nullable=False)                 # nameAnalysis / phone / nameOpt / bazipan / chenggu
    input = mapped_column(String(512), default="")
    result = mapped_column(Text, default="{}")
    created_at = mapped_column(DateTime, server_default=func.now())
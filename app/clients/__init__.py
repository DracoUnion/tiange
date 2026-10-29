"""外部依赖适配层：LLM 等外部客户端（零 Qt）。"""
from __future__ import annotations

from clients.openai_client import OpenAIClient

__all__ = ["OpenAIClient"]
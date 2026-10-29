"""AI 服务门面：所有 LLM 调用统一走 OpenAIClient（见 clients/openai_client.py）。

配置项（env）：OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL。
未配置 key 时，AI 类接口返回友好错误（不做 mock）。
"""
from __future__ import annotations

from typing import Iterator

import openai

from core.config import settings
from clients.openai_client import OpenAIClient


class AINotConfigured(Exception):
    pass


def _ensure_configured():
    if not settings.OPENAI_API_KEY:
        raise AINotConfigured("AI 服务未配置：请设置 OPENAI_API_KEY")


def _client() -> OpenAIClient:
    _ensure_configured()
    return OpenAIClient(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        timeout=openai.Timeout(read=120, connect=60, write=None, pool=None),
    )


def stream_chat(messages: list[dict], system: str | None = None,
                model: str | None = None, temperature: float = 0.8,
                max_tokens: int | None = 1500) -> Iterator[str]:
    """流式对话，yield 文本增量。同步生成器，供 AIWorker/QThread 使用。"""
    client = _client()
    yield from client.stream_chat(
        messages, model or settings.OPENAI_MODEL,
        temp=temperature, max_tokens=max_tokens, system=system,
    )


def complete(messages: list[dict], system: str | None = None,
             model: str | None = None, temperature: float = 0.8,
             max_tokens: int = 1200) -> str:
    """非流式完成，返回完整文本。"""
    client = _client()
    return client.call_llm_retry(
        messages, model or settings.OPENAI_MODEL,
        temp=temperature, max_tokens=max_tokens,
    )


def ai_error_message() -> str:
    return "AI 功能需要配置 LLM（设置 OPENAI_API_KEY）后可用。"
"""AI 服务：OpenAI 兼容的 SSE 流式客户端。

配置项（env）：OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL。
未配置 key 时，AI 类接口返回友好错误（不做 mock）。
"""
from __future__ import annotations

import json

import httpx

from ..core.config import settings


class AINotConfigured(Exception):
    pass


def _ensure_configured():
    if not settings.OPENAI_API_KEY:
        raise AINotConfigured("AI 服务未配置：请在 .env 设置 OPENAI_API_KEY")


async def stream_chat(messages: list[dict], model: str | None = None,
                      temperature: float = 0.8, max_tokens: int | None = 1500,
                      system: str | None = None):
    """流式对话。yield 文本增量。messages=[{role,content}]。"""
    _ensure_configured()
    if system:
        messages = [{"role": "system", "content": system}] + messages
    payload = {
        "model": model or settings.OPENAI_MODEL,
        "messages": messages,
        "temperature": temperature,
        "stream": True,
    }
    if max_tokens:
        payload["max_tokens"] = max_tokens
    url = settings.OPENAI_BASE_URL.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}",
               "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream("POST", url, json=payload, headers=headers) as resp:
            if resp.status_code != 200:
                body = await resp.aread()
                raise RuntimeError(f"LLM HTTP {resp.status_code}: {body[:200]}")
            async for line in resp.aiter_lines():
                if not line or not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                except Exception:
                    continue
                delta = chunk.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content")
                if content:
                    yield content


async def complete(messages: list[dict], system: str | None = None,
                   model: str | None = None, temperature: float = 0.8,
                   max_tokens: int = 1200) -> str:
    """非流式完成，返回完整文本。"""
    _ensure_configured()
    if system:
        messages = [{"role": "system", "content": system}] + messages
    payload = {
        "model": model or settings.OPENAI_MODEL,
        "messages": messages, "temperature": temperature, "max_tokens": max_tokens,
    }
    url = settings.OPENAI_BASE_URL.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}",
               "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(url, json=payload, headers=headers)
        if resp.status_code != 200:
            raise RuntimeError(f"LLM HTTP {resp.status_code}: {resp.text[:200]}")
        return resp.json()["choices"][0]["message"]["content"]


def ai_error_message() -> str:
    return "AI 功能需要配置 LLM（在 .env 设置 OPENAI_API_KEY）后可用。"
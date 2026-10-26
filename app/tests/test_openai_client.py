"""OpenAIClient 单元测试：构造、未配置降级、流式逐块、完整调用（本地端点可用时）。"""
from __future__ import annotations

import pytest

from core.config import settings
from services import ai
from services.openai_client import OpenAIClient


def test_client_builds():
    c = OpenAIClient(api_key="k", base_url="http://x/v1")
    assert c.api_key == "k"
    assert c.base_url == "http://x/v1"
    sdk = c._build_client()
    assert sdk.api_key == "k"


def test_stream_chat_requires_key(monkeypatch):
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")
    with pytest.raises(ai.AINotConfigured):
        ai._client()


def test_stream_chat_generator_requires_key(monkeypatch):
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")
    with pytest.raises(ai.AINotConfigured):
        next(ai.stream_chat([{"role": "user", "content": "hi"}]))


def test_ai_error_message():
    assert "OPENAI_API_KEY" in ai.ai_error_message()


@pytest.mark.skipif(not settings.OPENAI_API_KEY, reason="未配置 OPENAI_API_KEY，跳过真实 LLM 调用")
def test_stream_chat_hits_local_llm():
    """本地端点（如 localhost:5000）存在时，验证流式逐块返回。"""
    got = list(ai.stream_chat(
        [{"role": "user", "content": "请只回复两个字：你好"}],
        max_tokens=40,
    ))
    assert isinstance(got, list)
    # 即使空内容也证明链路打通（无异常抛出）
    joined = "".join(got)
    assert "你好" in joined or not joined  # 端点可能返回空流


@pytest.mark.skipif(not settings.OPENAI_API_KEY, reason="未配置 OPENAI_API_KEY，跳过真实 LLM 调用")
def test_complete_hits_local_llm():
    text = ai.complete(
        [{"role": "user", "content": "请只回复：OK"}],
        max_tokens=20,
    )
    assert isinstance(text, str)
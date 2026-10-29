"""OpenAIClient —— 移植自 ../BookerGptTool/BookerGptTool/openai.py。

保留对话能力（call_llm / call_llm_retry / collect_stream_content / stream_chat），
移除工具调用循环、视觉 VLM、文生图 TTI、ToolsMixin 及 schema 辅助等依赖
重型库（pymupdf / pyturndown / ctx_compact / json_repair / yaml）的部分。
依赖：openai SDK。
"""
from __future__ import annotations

import json
import logging
import re
import traceback
from typing import Any, Dict, Iterable, Optional

import openai
from openai.types.chat import ChatCompletion, ChatCompletionChunk

logging.getLogger("openai._base_client").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)

NO_THINK_EXTRA_BODY = {
    "reasoning_effort": "none",
    "chat_template_kwargs": {
        "enable_thinking": False,
        "thinking_mode": "off",
        "reasoning_effort": "none",
        "reasoning_strength": "none",
    },
}


def ensure_utf8(text: str) -> str:
    return text.encode("utf8", "ignore").decode("utf8", "ignore")


def json_dump_model(obj: Any) -> str:
    """将对象（含 pydantic 模型/列表）序列化为 JSON 字符串。"""
    if hasattr(obj, "model_dump"):
        obj = obj.model_dump()
    elif isinstance(obj, list):
        obj = [it.model_dump() if hasattr(it, "model_dump") else it for it in obj]
    return json.dumps(obj, ensure_ascii=False)


def get_msgs_text(msgs):
    for m in msgs[::-1]:
        cont = m.get("content")
        if isinstance(cont, str):
            return m["content"]
        elif isinstance(cont, list):
            for it in m["content"]:
                tp = it.get("type")
                if tp == "text":
                    return it["text"]
    return ""


def repl_ins_token(msgs):
    repl_ins_token_re = lambda s: re.sub(r"<\|([\w\-\.]+)\|>", r"</\1/>", s)
    for m in msgs:
        cont = m.get("content")
        if isinstance(cont, str):
            m["content"] = ensure_utf8(repl_ins_token_re(m["content"]))
        elif isinstance(cont, list):
            for it in m["content"]:
                tp = it.get("type")
                if tp == "text":
                    it["text"] = ensure_utf8(repl_ins_token_re(it["text"]))
    return msgs


class OpenAIClient:
    """封装 OpenAI 兼容 API 对话调用（流式/非流式），配置保存在实例上。"""

    def __init__(
        self,
        api_key=None,
        base_url=None,
        user_agent="claude-cli/2.1.41 (external, cli)",
        stream=False,
        timeout=None,
        rpre="",
        no_think=False,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.user_agent = user_agent
        self.stream = stream
        self.timeout = timeout
        self.rpre = rpre
        self.no_think = no_think

    def _build_client(self) -> openai.OpenAI:
        return openai.OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            default_headers={"User-Agent": self.user_agent},
            timeout=self.timeout,
        )

    # ── 对话 ──────────────────────────────────────────

    def call_llm(
        self, msgs, model_name, *,
        temp=None,
        top_p=None,
        frequency_penalty=None,
        presence_penalty=None,
        max_tokens=None,
        extra_body=None,
    ):
        if isinstance(msgs, str):
            msgs = [{"role": "user", "content": msgs}]
        # 改变指令符号的形式，避免模型出错
        msgs = repl_ins_token(msgs)
        extra_body = extra_body or {}
        if isinstance(extra_body, str):
            extra_body = json.loads(extra_body)
        if self.no_think:
            extra_body.update(NO_THINK_EXTRA_BODY)
        logger.debug("ques: %s", json_dump_model(get_msgs_text(msgs)))
        sdk = self._build_client()
        res = sdk.chat.completions.create(
            messages=msgs,
            model=model_name,
            temperature=temp,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            max_tokens=max_tokens,
            extra_body=extra_body,
            stream=self.stream,
        )
        if self.stream:
            res: Iterable[ChatCompletionChunk]
            ans, rc = self.collect_stream_content(res)
        else:
            res: ChatCompletion
            content = res.choices[0].message.content or ""
            ans = content.strip()
            rc = (getattr(res.choices[0].message, "reasoning_content", "") or "").strip()
            # 思考型模型可能只输出 reasoning_content 而 content 为空，兜底展示
            if not ans:
                ans = rc
            self.check_model_repetition(ans)
        if not ans:
            raise ValueError(f"回复为空：{res}")

        # 还原指令格式
        ans = re.sub(r"</([\w\-\.]+)/>", r"<|\1|>", ans)
        ans = re.sub(r" thinking[\s\S]+? response", "", ans)
        logger.debug("ans: %s", json_dump_model(ans))
        return ans

    def call_llm_retry(
        self, msgs, model_name, *,
        retry=10,
        temp=None,
        top_p=None,
        frequency_penalty=None,
        presence_penalty=None,
        max_tokens=None,
        extra_body=None,
        parse_output=None,
    ):
        for i in range(retry):
            try:
                res = self.call_llm(
                    msgs, model_name,
                    temp=temp,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    max_tokens=max_tokens,
                    extra_body=extra_body,
                )
                return parse_output(res) if parse_output else res
            except KeyboardInterrupt:
                raise
            except Exception as ex:  # noqa: BLE001
                logger.debug("OpenAI retry %d", i + 1)
                logger.debug(traceback.format_exc())
                if i == retry - 1:
                    raise ex

    # ── 流式（逐块增量，供桌面 UI 实时刷新）──────────

    def stream_chat(
        self, msgs, model_name, *,
        temp=None,
        max_tokens=None,
        extra_body=None,
        system=None,
    ) -> Iterable[str]:
        """流式对话，逐块 yield 文本增量。"""
        if system:
            msgs = [{"role": "system", "content": system}] + msgs
        if isinstance(msgs, str):
            msgs = [{"role": "user", "content": msgs}]
        msgs = repl_ins_token(msgs)
        extra_body = extra_body or {}
        if isinstance(extra_body, str):
            extra_body = json.loads(extra_body)
        if self.no_think:
            extra_body.update(NO_THINK_EXTRA_BODY)
        sdk = self._build_client()
        resp = sdk.chat.completions.create(
            messages=msgs,
            model=model_name,
            temperature=temp,
            max_tokens=max_tokens,
            extra_body=extra_body,
            stream=True,
        )
        for chunk in resp:  # resp: Iterable[ChatCompletionChunk]
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            c = delta.content
            if not c:  # 思考型模型可能只带 reasoning_content
                c = getattr(delta, "reasoning_content", "") or ""
            if c:
                self.check_model_repetition(c)
                yield c

    def collect_stream_content(self, resp: Iterable[ChatCompletionChunk]):
        content = []
        rc = []
        for chunk in resp:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            delta_content = delta.content
            delta_rc = getattr(delta, "reasoning_content", "")
            if delta_content:
                content.append(delta_content)
                self.check_model_repetition("".join(content))
                logger.debug("stream: %s", json_dump_model(delta_content))
            if delta_rc:
                rc.append(delta_rc)
                self.check_model_repetition("".join(rc))
                logger.debug("reasoning stream: %s", json_dump_model(delta_rc))
        return "".join(content), "".join(rc)

    # ── 复读检测 ──────────────────────────────────────

    def check_model_repetition(self, text):
        if self.rpre and re.search(self.rpre, text):
            raise ValueError("检测到模型复读")


__all__ = ["OpenAIClient"]
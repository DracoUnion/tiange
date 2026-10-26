"""业务异常，供 UI 层展示友好提示。

桌面版不再有 HTTP：BizError 作为算法/服务硬性失败的载体，
UI 捕获后以 toast/错误条展示 msg + reason。
"""
from __future__ import annotations


class BizError(Exception):
    """业务异常。msg=主信息，reason=补充说明。"""

    def __init__(self, msg: str, code: int = 400, reason: str | None = None):
        super().__init__(msg)
        self.msg = msg
        self.code = code
        self.reason = reason


class AINotConfigured(BizError):
    def __init__(self, msg: str = "AI 服务未配置"):
        super().__init__(msg, code=400, reason="请在环境变量设置 OPENAI_API_KEY")
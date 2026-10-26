"""统一响应与异常。

线上接口统一返回 `{code, msg, res}`；错误为 `{code, msg, reason}`。
code: 0=成功, 401=未授权, 400=参数错误, 402=余额不足, 403=无权限, 409=冲突, 500=错误。
"""
from __future__ import annotations

from typing import Any, TypeVar

from fastapi import HTTPException
from fastapi.responses import JSONResponse

T = TypeVar("T")


class BizError(Exception):
    """业务异常，映射为 JSON {code, msg, reason}。"""

    def __init__(self, msg: str, code: int = 400, reason: str | None = None, http_status: int | None = None):
        self.msg = msg
        self.code = code
        self.reason = reason
        self.http_status = http_status or (200 if code == 0 else code)


class NotAuthorized(BizError):
    def __init__(self, path: str = ""):
        reason = f"需要登录后访问: {path}" if path else "需要登录"
        super().__init__("未授权访问", code=401, reason=reason, http_status=401)


class InsufficientBeans(BizError):
    def __init__(self, need: int = 0):
        super().__init__("心识豆不足", code=402, reason=f"需要 {need} 心识豆，余额不足", http_status=402)


def ok(res: Any = None, msg: str = "success") -> dict:
    return {"code": 0, "msg": msg, "res": res}


def error(msg: str, code: int = 400, reason: str | None = None) -> dict:
    return {"code": code, "msg": msg, "reason": reason}


def to_http_exception(e: BizError) -> HTTPException:
    return HTTPException(status_code=e.http_status, detail=error(e.msg, e.code, e.reason))


def biz_response(exc: BizError) -> JSONResponse:
    return JSONResponse(status_code=exc.http_status, content=error(exc.msg, exc.code, exc.reason))


def http400(msg: str, reason: str | None = None) -> None:
    raise BizError(msg, code=400, reason=reason, http_status=400)
"""邮箱验证码服务（开发环境打印/存储到内存）。"""
from __future__ import annotations

import random
import smtplib
import time
from email.mime.text import MIMEText

from ..core.config import settings

_code_store: dict[str, tuple[str, float]] = {}
_TTL = 600


def apply_code(email: str, purpose: str = "register") -> str:
    code = f"{random.randint(0, 999999):06d}"
    _code_store[email + ":" + purpose] = (code, time.time())
    if settings.EMAIL_MOCK or not settings.SMTP_HOST:
        print(f"[email-mock] {purpose} code for {email}: {code}")
        return code
    _send(email, code, purpose)
    return code


def verify_code(email: str, purpose: str, code: str) -> bool:
    rec = _code_store.get(email + ":" + purpose)
    if not rec or time.time() - rec[1] > _TTL:
        return False
    return rec[0] == code.strip()


def _send(email: str, code: str, purpose: str):
    msg = MIMEText(f"您的{purpose}验证码是：{code}，10 分钟内有效。", "plain", "utf-8")
    msg["Subject"] = f"{settings.APP_NAME} 验证码"
    msg["From"] = settings.SMTP_USER
    msg["To"] = email
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as s:
        s.login(settings.SMTP_USER, settings.SMTP_PASS)
        s.send_message(msg)
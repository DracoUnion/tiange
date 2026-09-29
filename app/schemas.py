"""Pydantic 请求/响应模型（统一枚举线上接口出入参）。"""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field


# ---------- 通用 ----------
class Ok(BaseModel):
    code: int = 0
    msg: str = "success"
    res: Any = None


# ---------- 认证 ----------
class CaptchaReq(BaseModel):
    captcha_id: str
    answer: str


class RegisterReq(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=64)
    email: Optional[str] = None
    captcha_id: str
    captcha_answer: str
    invite_code: Optional[str] = None


class LoginReq(BaseModel):
    account: str                       # 用户名或邮箱
    password: str
    captcha_id: str
    captcha_answer: str


class EmailCodeApplyReq(BaseModel):
    email: EmailStr
    purpose: str = "register"          # register/reset


class EmailCodeVerifyReq(BaseModel):
    email: EmailStr
    code: str


class ResetPasswordReq(BaseModel):
    email: EmailStr
    code: str
    new_password: str = Field(min_length=6, max_length=64)


# ---------- 用户 ----------
class UserInfoUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    lang: Optional[str] = None
    birth_year: Optional[int] = None
    birth_month: Optional[int] = None
    birth_day: Optional[int] = None


class SolarToLunarReq(BaseModel):
    year: int
    month: int
    day: int


# ---------- 成员 ----------
class MemberCreate(BaseModel):
    name: str = Field(max_length=64)
    relation: str = "self"
    gender: str = "male"
    is_self: int = 0
    calendar: str = "solar"
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: int = 0
    birth_minute: int = 0
    timezone: str = "Asia/Shanghai"


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    relation: Optional[str] = None
    gender: Optional[str] = None
    is_self: Optional[int] = None
    calendar: Optional[str] = None
    birth_year: Optional[int] = None
    birth_month: Optional[int] = None
    birth_day: Optional[int] = None
    birth_hour: Optional[int] = None
    birth_minute: Optional[int] = None
    timezone: Optional[str] = None


# ---------- 心识豆 / VIP ----------
class RedeemReq(BaseModel):
    code: str


class VipOrderReq(BaseModel):
    tier: str
    period: str = "monthly"


# ---------- 运势 ----------
class FortuneReq(BaseModel):
    member_id: Optional[int] = None
    target_date: Optional[str] = None
    params: dict = {}


# ---------- 占卜 ----------
class DivinationReq(BaseModel):
    member_id: Optional[int] = None
    things: str = ""
    numbers: Optional[list[int]] = None
    seed: Optional[int] = None
    params: dict = {}


class PaipanReq(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    hour: Optional[int] = None
    member_id: Optional[int] = None
    things: str = ""
    numbers: Optional[list[int]] = None
    seed: Optional[int] = None


# ---------- 八字/称骨 ----------
class BaziReq(BaseModel):
    calendar: str = "solar"
    year: int
    month: int
    day: int
    hour: int = 0
    gender: str = "male"


class ChengguReq(BaseModel):
    calendar: str = "solar"
    year: int
    month: int
    day: int
    hour: int = 0


# ---------- 命书 ----------
class MingshuReq(BaseModel):
    type: str                                    # bazi/ziwei/tianming/ten_year
    member_id: Optional[int] = None
    params: dict = {}


# ---------- 姓名/手机/起名 ----------
class NameOptReq(BaseModel):
    surname: str = ""
    gender: str = "male"
    count: int = 6
    style: str = "现代"
    things: str = ""


class PhoneReq(BaseModel):
    phone: str


# ---------- 合盘 ----------
class HepanCreate(BaseModel):
    type: str = "marriage"                       # marriage/communication/career
    member_a_id: Optional[int] = None
    member_b_id: Optional[int] = None


# ---------- AI 道长 ----------
class DaoistChatReq(BaseModel):
    message: str = Field(max_length=2000)
    references: Optional[list] = None


# ---------- 内容安全 ----------
class ContentCheckReq(BaseModel):
    content: str
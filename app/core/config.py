"""应用配置。所有可配置项走环境变量（.env / os.environ）。"""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "天格"
    API_PREFIX: str = "/api/v1"
    ENV: str = "dev"
    DEBUG: bool = True

    # 数据库
    DATABASE_URL: str = "sqlite:///./tiange.db"

    # 安全
    SECRET_KEY: str = "change-me-to-a-long-random-string"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # 验证码 / 邮箱
    EMAIL_MOCK: bool = True
    SMTP_HOST: str = ""
    SMTP_PORT: int = 465
    SMTP_USER: str = ""
    SMTP_PASS: str = ""

    # 赠送
    REGISTER_BONUS_BEANS: int = 50
    INVITE_BONUS_BEANS: int = 20

    # AI（OpenAI 兼容）
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o-mini"

    # CORS
    CORS_ORIGINS: List[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

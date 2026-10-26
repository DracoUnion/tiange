"""应用配置。桌面版仅保留 AI 与少量应用选项，直接读环境变量。"""
from __future__ import annotations

import os


class Settings:
    APP_NAME: str = "天格"
    DEBUG: bool = True

    # AI（OpenAI 兼容，未配置 key 时 AI 功能返回友好提示）
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


settings = Settings()
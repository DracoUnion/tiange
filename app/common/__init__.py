"""零 Qt 基础组件：事件、上下文、配置、异常。任何头less / 测试环境可独立导入。"""
from __future__ import annotations

from common.config import Settings, settings as default_settings
from common.events import EventHub
from common.context import AppContext
from common.exceptions import (
    TiangeError,
    ConfigError,
    ServiceError,
    BizError,
    AINotConfigured,
)

__all__ = [
    "TiangeError",
    "ConfigError",
    "ServiceError",
    "BizError",
    "AINotConfigured",
    "Settings",
    "default_settings",
    "EventHub",
    "AppContext",
]
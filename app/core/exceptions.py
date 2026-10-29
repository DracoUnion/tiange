"""业务异常（兼容 re-export）。

实现已迁移至 :mod:`common.exceptions`；保持既有导入面可用。
"""
from __future__ import annotations

from common.exceptions import (
    AINotConfigured,
    BizError,
    ConfigError,
    ServiceError,
    TiangeError,
)

__all__ = [
    "TiangeError",
    "ConfigError",
    "ServiceError",
    "BizError",
    "AINotConfigured",
]
"""应用配置（兼容 re-export）。

配置实现已迁移至 :mod:`common.config`；保持 ``from core.config import
settings`` 调用面不变。
"""
from __future__ import annotations

from common.config import Settings, settings

__all__ = ["Settings", "settings"]
"""pytest 配置：确保仓库根目录在 sys.path，`app` 包可从任意调用方式导入。"""
from __future__ import annotations

import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)
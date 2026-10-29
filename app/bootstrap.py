"""应用装配：把零 Qt 服务图组装为 AppContext 并返回。

UI 层不再直接构造服务；它只持有 bootstrap 返回的上下文和 Qt 桥。
"""
from __future__ import annotations

from typing import Any, Optional

from common.config import Settings, settings as default_settings
from common.context import AppContext
from common.events import EventHub
from services.facade import ServiceFacade
from tasks import TaskManager


def build_context(
    *,
    settings: Optional[Settings] = None,
    max_workers: int = 2,
    extras: Optional[dict[str, Any]] = None,
) -> AppContext:
    """装配 AppContext。"""
    settings = settings or default_settings
    events = EventHub()
    tasks = TaskManager(max_workers=max_workers, events=events)
    services = ServiceFacade(settings=settings, events=events, tasks=tasks)
    return AppContext(
        settings=settings,
        events=events,
        tasks=tasks,
        services=services,
        extras=extras or {},
    )
"""应用上下文（零 Qt）。由 bootstrap 装配，UI 持有并只经它能访问服务。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from common.events import EventHub

if TYPE_CHECKING:
    from core.config import Settings
    from services.facade import ServiceFacade
    from tasks import TaskManager


@dataclass
class AppContext:
    """bootstrap 注入的运行时服务包。"""

    settings: "Settings"
    events: EventHub
    tasks: "TaskManager"
    services: "ServiceFacade"
    extras: dict[str, Any] = field(default_factory=dict)

    def extra(self, key: str, default: Any = None) -> Any:
        return self.extras.get(key, default)
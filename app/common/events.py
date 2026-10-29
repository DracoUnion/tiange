"""线程安全的进程内发布/订阅事件总线（零 Qt）。"""
from __future__ import annotations

from threading import RLock
from typing import Any, Callable

EventHandler = Callable[[dict[str, Any]], None]


class EventHub:
    """解耦服务层与 UI 适配器的小型事件总线。"""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}
        self._lock = RLock()

    def subscribe(self, event_type: str, handler: EventHandler) -> Callable[[], None]:
        with self._lock:
            self._handlers.setdefault(event_type, []).append(handler)

        def unsubscribe() -> None:
            self.unsubscribe(event_type, handler)

        return unsubscribe

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        with self._lock:
            handlers = self._handlers.get(event_type, [])
            if handler in handlers:
                handlers.remove(handler)
            if not handlers:
                self._handlers.pop(event_type, None)

    def publish(self, event_type: str, **payload: Any) -> None:
        event = {"type": event_type, **payload}
        with self._lock:
            handlers = tuple(self._handlers.get(event_type, ()))
            handlers += tuple(self._handlers.get("*", ()))
        for handler in handlers:
            handler(event)
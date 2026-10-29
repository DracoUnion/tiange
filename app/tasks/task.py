"""零 Qt 任务状态机：耗时操作（AI 对话等）统一经 TaskManager 后台执行。"""
from __future__ import annotations

import itertools
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

from common.events import EventHub

TaskFn = Callable[..., Any]


class TaskState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    CANCELLING = "cancelling"
    DONE = "done"
    FAILED = "failed"


@dataclass
class Task:
    """后台任务单元。UI 只通过 Qt 桥接收其事件，不直接操作。"""

    id: str
    label: str
    state: TaskState = TaskState.PENDING
    progress: int = 0
    message: str = ""
    result: Any = None
    error: Optional[str] = None
    cancel_event: threading.Event = field(default_factory=threading.Event)

    def request_cancel(self) -> None:
        self.cancel_event.set()
        if self.state == TaskState.PENDING:
            self.state = TaskState.CANCELLING


class TaskManager:
    """在线程池上执行 ``fn`` 并派发生命周期事件（started/running/...）。"""

    def __init__(self, max_workers: int = 2, events: Optional[EventHub] = None) -> None:
        self._pool = ThreadPoolExecutor(max_workers, thread_name_prefix="tg-task")
        self._events = events or EventHub()
        self._tasks: dict[str, Task] = {}
        self._ids = itertools.count(1)

    def submit(self, fn: TaskFn, *, label: str = "", **kwargs: Any) -> Task:
        task = Task(id=f"task-{next(self._ids)}", label=label or getattr(fn, "__name__", "task"))
        self._tasks[task.id] = task
        self._publish("started", task=task)
        self._pool.submit(self._run, task, fn, kwargs)
        return task

    def _run(self, task: Task, fn: TaskFn, kwargs: dict[str, Any]) -> None:
        if task.cancel_event.is_set():
            task.state = TaskState.CANCELLING
            self._publish("cancelled", task=task)
            return
        task.state = TaskState.RUNNING
        self._publish("running", task=task)
        try:
            task.result = fn(cancel_event=task.cancel_event, **kwargs)
            task.state = TaskState.DONE
            task.progress = 100
            self._publish("done", task=task)
        except TaskCancelled:
            task.state = TaskState.CANCELLING
            self._publish("cancelled", task=task)
        except Exception as exc:  # noqa: BLE001
            task.state = TaskState.FAILED
            task.error = str(exc)
            self._publish("failed", task=task, error=str(exc))

    def cancel(self, task_id: str) -> bool:
        task = self._tasks.get(task_id)
        if task is not None:
            task.request_cancel()
            return True
        return False

    def progress(self, task_id: str, pct: int, message: str = "") -> None:
        task = self._tasks.get(task_id)
        if task is None:
            return
        task.progress = max(0, min(100, pct))
        task.message = message
        self._publish("progress", task=task, pct=task.progress, msg=message)

    def get(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def subscribe(self, handler) -> Callable[[], None]:
        """订阅全部生命周期事件。"""
        return self._events.subscribe("*", handler)

    def shutdown(self, wait: bool = True) -> None:
        self._pool.shutdown(wait=wait)

    def _publish(self, event_type: str, **payload: Any) -> None:
        event = {"type": event_type, **payload}
        self._events.publish(event_type, **event)
        self._events.publish("*", **event)


class TaskCancelled(Exception):
    """任务函数用于协作式取消。"""
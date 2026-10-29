"""服务门面：UI 的唯一入口（零 Qt）。

组合算法服务与 AI 服务，供 UI 通过 AppContext.services 调用；同时保持
与现有 ``services.ai`` 等模块的函数调用兼容（门面只是编排层，不复制逻辑）。
"""
from __future__ import annotations

from typing import Iterator, Optional

from core.config import Settings
from common.events import EventHub
from tasks import Task, TaskCancelled, TaskManager


class ServiceFacade:
    """UI-facing facade; no Qt imports."""

    def __init__(
        self,
        *,
        settings: Settings,
        events: EventHub,
        tasks: TaskManager,
    ) -> None:
        self.settings = settings
        self.events = events
        self.tasks = tasks

    # -- AI ------------------------------------------------------------- #

    def ai_stream(
        self,
        messages: list[dict],
        *,
        system: str | None = None,
        max_tokens: int | None = 1500,
        label: str = "ai-stream",
    ) -> Task:
        """在后台线程跑 ``services.ai.stream_chat``，逐段增量非流式收全。

        注意：AIWorker(QThread) 处理流式 UI；此方法用于非流式后台调用。
        """
        from services import ai

        def _run(*, cancel_event, **_: object) -> str:
            if cancel_event.is_set():
                raise TaskCancelled()
            return ai.complete(
                messages, system=system, max_tokens=max_tokens,
            )

        return self.tasks.submit(_run, label=label)

    # -- 算法（转发到纯函数 services，便于统一入口） ---------------------- #

    def bazi_paipan(self, year: int, month: int, day: int, hour: int,
                    gender: Optional[str] = None,
                    time_zone: Optional[str] = None,
                    lat: Optional[float] = None,
                    lng: Optional[float] = None) -> dict:
        from services import bazi, lunisolar

        solar = lunisolar.solar_to_lunar(year, month, day)
        return bazi.paipan(solar, hour, gender=gender, time_zone=time_zone,
                           lat=lat, lng=lng)

    def qian_main(self, *args, **kwargs):
        from services import qian

        return qian.main(*args, **kwargs)

    def chenggu_main(self, *args, **kwargs):
        from services import chenggu

        return chenggu.main(*args, **kwargs)

    def divination_main(self, *args, **kwargs):
        from services import divination

        return divination.main(*args, **kwargs)

    def fortune_main(self, *args, **kwargs):
        from services import fortune

        return fortune.main(*args, **kwargs)
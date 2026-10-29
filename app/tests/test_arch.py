"""架构层单测：common 事件 / tasks 状态机 / bootstrap 装配（零 Qt）。"""
from __future__ import annotations

import time

import pytest

from common.events import EventHub
from tasks import TaskManager, TaskState


# ---- EventHub ------------------------------------------------------ #

def test_eventhub_sub_and_publish():
    hub = EventHub()
    seen = []
    unsub = hub.subscribe("demo", lambda ev: seen.append(ev))
    hub.publish("demo", x=1)
    unsub()
    hub.publish("demo", x=2)
    assert len(seen) == 1
    assert seen[0]["type"] == "demo"
    assert seen[0]["x"] == 1


def test_eventhub_wildcard():
    hub = EventHub()
    seen = []
    hub.subscribe("*", lambda ev: seen.append(ev["type"]))
    hub.publish("a")
    hub.publish("b")
    assert seen == ["a", "b"]


# ---- TaskManager --------------------------------------------------- #

def test_submit_done_and_result():
    tm = TaskManager(max_workers=2)
    events = []
    tm.subscribe(lambda ev: events.append(ev["type"]))

    def work(*, cancel_event, **kwargs):
        time.sleep(0.02)
        return 42

    task = tm.submit(work, label="calc")
    deadline = time.time() + 3
    while task.state not in (TaskState.DONE, TaskState.FAILED) and time.time() < deadline:
        time.sleep(0.005)
    tm.shutdown()
    assert task.result == 42
    assert task.state == TaskState.DONE
    assert "started" in events
    assert "done" in events


def test_submit_failed_sets_error():
    tm = TaskManager(max_workers=1)

    def boom(*, cancel_event, **kwargs):
        raise ValueError("boom")

    task = tm.submit(boom, label="fail")
    deadline = time.time() + 2
    while task.state not in (TaskState.DONE, TaskState.FAILED) and time.time() < deadline:
        time.sleep(0.005)
    tm.shutdown()
    assert task.state == TaskState.FAILED
    assert task.error == "boom"


def test_cancel_sets_cooperative_flag():
    tm = TaskManager(max_workers=1)
    task = tm.submit(
        lambda *, cancel_event, **kwargs: cancel_event.wait(2),
        label="block",
    )
    time.sleep(0.03)
    assert tm.cancel(task.id)
    assert task.cancel_event.is_set()
    tm.shutdown(wait=False)


# ---- bootstrap ------------------------------------------------------ #

def test_build_context_assembles_services():
    from bootstrap import build_context

    ctx = build_context()
    assert ctx.events is not None
    assert ctx.tasks is not None
    assert ctx.services is not None
    assert ctx.settings.APP_NAME == "天格"


def test_facade_ai_stream_submits_task(monkeypatch):
    """ai_stream 异步提交，立即返回 Task（不触网、不抛）。"""
    from bootstrap import build_context
    from tasks import Task

    ctx = build_context()
    task = ctx.services.ai_stream([{"role": "user", "content": "hi"}])
    assert isinstance(task, Task)
    assert task.label == "ai-stream"


def test_ai_complete_not_configured(monkeypatch):
    """未配置 key 时 complete() 抛出友好 AINotConfigured（不触网）。"""
    from common.config import settings
    from services import ai

    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")
    with pytest.raises(ai.AINotConfigured):
        ai.complete([{"role": "user", "content": "hi"}])
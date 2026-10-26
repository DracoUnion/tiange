"""AI 流式 Worker：在 QThread 中跑 ai.stream_chat（同步生成器），逐段刷新 UI。

用法：
    worker = AIWorker(system, [messages], max_tokens=...)
    worker.delta.connect(append_text)      # str 增量
    worker.completed.connect(done)         # 正常结束（注意：不与 QThread.finished 同名）
    worker.failed.connect(on_error)        # 出错（含未配置 AI）
    worker.start()
"""
from __future__ import annotations

from PySide6.QtCore import QThread, Signal

from services import ai


class AIWorker(QThread):
    delta = Signal(str)      # 文本增量
    completed = Signal()     # 流式正常结束（重命名避免覆盖 QThread.finished）
    failed = Signal(str)     # 错误信息（含未配置 AI 的友好提示）

    def __init__(self, system: str, messages: list[dict],
                 max_tokens: int | None = None, parent=None):
        super().__init__(parent)
        self._system = system
        self._messages = messages
        self._max_tokens = max_tokens

    def run(self):
        try:
            for chunk in ai.stream_chat(
                    self._messages, system=self._system, max_tokens=self._max_tokens):
                self.delta.emit(chunk)
            self.completed.emit()
        except ai.AINotConfigured:
            self.failed.emit(ai.ai_error_message())
        except Exception as e:  # noqa: BLE001
            self.failed.emit(f"生成失败：{str(e)[:200]}")
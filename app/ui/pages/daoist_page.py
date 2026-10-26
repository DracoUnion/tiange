"""天格道长：AI 流式对话。"""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QTextBrowser, QVBoxLayout, QWidget

from ui.ai_worker import AIWorker
from ui.widgets import SectionTitle

_SYSTEM = ("你是天格的「天格道长」，一位通达《道德经》与道家智慧的智者。"
           "用温和、沉稳、富有哲理又不失落地的语气，与用户交流人生、情绪与选择。"
           "回答使用简体中文，篇幅适中，可引用经句并给出行动建议。")


class DaoistPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ai = None
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.addWidget(SectionTitle("天格道长", "一位通达道家智慧的 AI 智者"))
        self.messages = QTextBrowser()
        self.messages.setOpenExternalLinks(False)
        self.messages.append('<b style="color:#d8b872">道长 ·</b> 贫道天格，愿听施主心事。有何疑惑，尽可道来。')
        lay.addWidget(self.messages, 1)
        bottom = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("向道长请教…")
        self.input.returnPressed.connect(self._send)
        bottom.addWidget(self.input, 1)
        self.send_btn = QPushButton("发送")
        self.send_btn.clicked.connect(self._send)
        bottom.addWidget(self.send_btn)
        lay.addLayout(bottom)

    def _send(self):
        text = self.input.text().strip()
        if not text or (self._ai and self._ai.isRunning()):
            return
        self.input.clear()
        self.messages.append(f'<div style="text-align:right"><span>{text}</span></div>')
        self.messages.append('<b style="color:#d8b872">道长 ·</b> ')
        self.send_btn.setEnabled(False)
        self._ai = AIWorker(_SYSTEM, [{"role": "user", "content": text}], max_tokens=800)
        self._ai.delta.connect(self._append)
        self._ai.completed.connect(self._ai_done)
        self._ai.failed.connect(self._ai_fail)
        self._ai.start()

    def _append(self, text: str):
        self.messages.insertPlainText(text)

    def _ai_done(self):
        self.send_btn.setEnabled(True)

    def _ai_fail(self, msg: str):
        self.send_btn.setEnabled(True)
        self.messages.append(f'<span style="color:#ef9a96">{msg}</span>')
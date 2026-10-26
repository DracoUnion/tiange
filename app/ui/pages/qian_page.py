"""占卜页：64卦 / 观音灵签 / 诸葛神算（含 AI 解卦）。"""
from __future__ import annotations

import json

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from ui.ai_worker import AIWorker
from ui.widgets import Card, SectionTitle, make_result_browser, stream_plain
from services import qian as qsv

TYPES = [
    ("64gua", "周易占卜"),
    ("guanyin", "观音灵签"),
    ("zhuge", "诸葛神算"),
]

TYPE_SYSTEM = {
    "64gua": "你是一位精通《周易》与传统文化解卦的资深命理师，请结合卦象为用户提供诚恳、正面、实用的解读。用简体中文，分点输出，语气温和有据。",
    "guanyin": "你是一位解签大师，请结合观音灵签签文为用户解读。用简体中文，语气温和有据。",
    "zhuge": "你是一位解卦大师，请结合诸葛神算卦辞为用户解读。用简体中文，语气温和有据。",
}


class QianPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ai = None
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.addWidget(SectionTitle("签卦占卜", "诚心默念所问之事，点击抽签"))
        top = QHBoxLayout()
        self.type_cb = QComboBox()
        for key, label in TYPES:
            self.type_cb.addItem(label, key)
        top.addWidget(QLabel("类型"), 0)
        top.addWidget(self.type_cb, 1)
        lay.addLayout(top)

        card = Card()
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(16, 12, 16, 14)
        self.things = QLineEdit()
        self.things.setPlaceholderText("所问之事，如：近期事业运如何？")
        card_lay.addWidget(self.things)
        btns = QHBoxLayout()
        self.draw_btn = QPushButton("抽签")
        self.draw_btn.clicked.connect(lambda: self._run(use_ai=False))
        btns.addWidget(self.draw_btn)
        self.ai_btn = QPushButton("✨ AI 解卦")
        self.ai_btn.setObjectName("ghost")
        self.ai_btn.clicked.connect(lambda: self._run(use_ai=True))
        btns.addWidget(self.ai_btn)
        card_lay.addLayout(btns)
        lay.addWidget(card)

        self.err = QLabel("")
        self.err.setObjectName("err")
        lay.addWidget(self.err)
        self.result = make_result_browser()
        self.result.setVisible(False)
        lay.addWidget(self.result, 1)

    def set_mode(self, qtype: str):
        idx = self.type_cb.findData(qtype)
        if idx >= 0:
            self.type_cb.setCurrentIndex(idx)

    def _draw(self):
        qtype = self.type_cb.currentData()
        things = self.things.text().strip()
        if qtype == "64gua":
            return qsv.draw_64gua(things)
        if qtype == "guanyin":
            return qsv.draw_guanyin(things)
        return qsv.draw_zhuge(things)

    def _render(self, res):
        if res.get("name"):
            self.result.setHtml(
                f'<h3 style="margin:0">{res["name"]}'
                f'<span style="font-size:13px;color:#a99c82">　第{res.get("order", "")}卦</span></h3>'
                f'<p style="white-space:pre-wrap">{res["guaci"]}</p>'
                f'<p style="color:#a99c82;white-space:pre-wrap">{res["baihua"]}</p>'
                f'<details style="margin-top:8px"><summary style="color:#d8b872">查看卦辞详解</summary>'
                f'<p style="font-size:13px;color:#a99c82;white-space:pre-wrap">{res.get("yaoci", "")}</p></details>'
            )
        else:
            self.result.setHtml(
                f'<h3 style="margin:0">{res.get("qian", "")} · {res.get("title", "")}</h3>'
                f'<p style="white-space:pre-wrap">{res.get("text", "")}</p>'
                f'<p style="color:#a99c82;white-space:pre-wrap">{res.get("interpret", "")}</p>'
            )
        self.result.setVisible(True)

    def _run(self, use_ai=False):
        self.err.setText("")
        res = self._draw()
        self._render(res)
        if use_ai:
            self._clear_ai()
            qtype = self.type_cb.currentData()
            things = self.things.text().strip()
            self._ai = AIWorker(
                TYPE_SYSTEM[qtype].replace("用户", "用户（所问：%s）" % (things or "未知"), 1)
                if TYPE_SYSTEM[qtype].find("为用户") >= 0 else TYPE_SYSTEM[qtype],
                [{"role": "user", "content": f"卦/签内容：{json.dumps(res, ensure_ascii=False)[:1200]}"}],
            )
            self._ai.delta.connect(self._ai_append)
            self._ai.completed.connect(self._ai_done)
            self._ai.failed.connect(self._ai_fail)
            self._ai.start()

    def _clear_ai(self):
        self.result.append("<hr><b>✨ AI 解卦</b>")
        self.err.setText("")

    def _ai_append(self, text: str):
        stream_plain(self.result, text)

    def _ai_done(self):
        pass

    def _ai_fail(self, msg: str):
        self.err.setText(msg)
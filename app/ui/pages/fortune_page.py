"""运势页：今日/本周/本月/今年/大运/一生，选择成员周期。"""
from __future__ import annotations

import datetime as dt

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ui.widgets import BirthForm, SectionTitle, make_luck_label, make_result_browser
from services import bazi as bz
from services import fortune as fsv
from services import lunisolar as L

KINDS = [
    ("today", "今日运势"),
    ("thisWeek", "本周运势"),
    ("thisMonth", "本月运势"),
    ("thisYear", "今年运势"),
    ("thisDayun", "大运运势"),
    ("oneLife", "一生运势"),
]


class FortunePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.addWidget(SectionTitle("运势预测", "选择出生信息，查看多周期运势"))
        top = QHBoxLayout()
        self.kind_cb = QComboBox()
        for key, label in KINDS:
            self.kind_cb.addItem(label, key)
        top.addWidget(QLabel("运势类型"), 0)
        top.addWidget(self.kind_cb, 1)
        lay.addLayout(top)
        self.form = BirthForm()
        lay.addWidget(self.form)
        row = QHBoxLayout()
        btn = QPushButton("开始测算")
        btn.clicked.connect(self._run)
        row.addWidget(btn, 0)
        row.addStretch(1)
        lay.addLayout(row)
        self.err = QLabel("")
        self.err.setObjectName("err")
        lay.addWidget(self.err)
        self.result = make_result_browser()
        self.result.setVisible(False)
        lay.addWidget(self.result, 1)

    def set_mode(self, kind: str):
        idx = self.kind_cb.findData(kind)
        if idx >= 0:
            self.kind_cb.setCurrentIndex(idx)

    def _member_input(self) -> dict:
        spec = self.form.spec()
        pan = bz.compute(spec)
        return {
            "name": "本命",
            "gender": spec["gender"],
            "day_master": pan["day_master"],
            "wuxing_missing": pan["wuxing_missing"],
            "zodiac": spec["zodiac"],
            "member_id": 0,
        }

    def _run(self):
        kind = self.kind_cb.currentData()
        target = dt.date.today().strftime("%Y-%m-%d")
        res = fsv.generate(kind, self._member_input(), target)
        self.err.setText("")
        cat_html = "".join(
            f'<td style="text-align:center;padding:8px"><div style="font-size:12px;color:#a99c82">{k}</div>'
            f'<div style="font-weight:600">{v}</div></td>' for k, v in res["categories"].items())
        luck_cls = "great" if res["luck"] in ("大吉", "中吉", "吉") else ("mid" if res["luck"] in ("小吉", "平") else "bad")
        self.result.setHtml(
            f'<div style="display:flex;align-items:center;gap:12px">'
            f'<span style="background:rgba(76,175,80,.2);color:#8cd68c;border-radius:20px;padding:2px 10px">{res["luck"]}</span>'
            f'<b style="color:#f0dfb6">综合评分 {res["score"]}</b>'
            f'<span style="color:#a99c82;font-size:12px">宜{res["direction"]} · {res["color"]}</span></div>'
            f'<p>{res["summary"]}</p>'
            f'<table style="border-collapse:collapse">{cat_html}</table>'
            f'<p><b style="color:#d8b872">宜</b> {" · ".join(res["yi"])}<br>'
            f'<b style="color:#ef9a96">忌</b> {" · ".join(res["ji"])}</p>'
            f'<p style="color:#a99c82;font-size:12px">当日干支：{res["day_ganzhi"]}</p>'
        )
        self.result.setVisible(True)
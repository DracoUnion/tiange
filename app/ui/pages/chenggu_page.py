"""称骨论命页。"""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ui.widgets import BirthForm, SectionTitle, make_luck_label, make_result_browser
from services import chenggu as cg


class ChengguPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.addWidget(SectionTitle("称骨论命", "骨重计算，免费人生预测"))
        self.form = BirthForm()
        lay.addWidget(self.form)
        row = QHBoxLayout()
        btn = QPushButton("称骨")
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

    def _run(self):
        f = self.form.fields()
        res = cg.compute(f["calendar"], f["year"], f["month"], f["day"], f["hour"])
        self.err.setText("")
        parts = "  ".join(
            f'{v["label"]} <b>{v["value"]}</b>' for v in res["parts"].values())
        self.result.setHtml(
            f'<div style="font-size:26px;font-weight:700;color:#d8b872">{res["total"]}</div>'
            f'<span style="color:#8cd68c">{res["luck"]}</span><br><br>{parts}'
            f'<hr><b>称骨歌诀</b><p>{res["song"]}</p>'
        )
        self.result.setVisible(True)
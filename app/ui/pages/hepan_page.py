"""合盘分析页：选择两位成员，分析姻缘/相处/事业。"""
from __future__ import annotations

import random

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ..widgets import BirthForm, SectionTitle, make_result_browser
from ...services import bazi as bz, lunisolar as L

TYPES = [
    ("marriage", "婚姻合盘"),
    ("communication", "相处之道"),
    ("career", "事业合伙"),
]


def _spec_of(f: BirthForm) -> dict:
    return f.spec()


def _analyze(a_name: str, a_spec: dict, b_name: str, b_spec: dict, htype: str) -> dict:
    pa, pb = bz.compute(a_spec), bz.compute(b_spec)
    seed = sum(ord(c) for c in (a_spec["day_ganzhi"] + b_spec["day_ganzhi"] + htype))
    rng = random.Random(seed)
    dims = ["情感契合", "性格互补", "沟通模式", "家庭和谐", "财运互助", "事业发展"]
    score = {d: round(rng.uniform(60, 96), 1) for d in dims}
    overall = round(sum(score.values()) / len(score), 1)
    suggest = ["多主动沟通，把心里的想法说清楚。",
               "共同设定阶段目标，彼此扶持。",
               "留出独立空间，尊重彼此的节奏。"]
    return {
        "overall": overall, "dimensions": score,
        "insights": f"{a_name}与{b_name}整体契合度较高，宜{'互补共进' if overall > 80 else '磨合成长'}。",
        "suggestions": suggest,
    }


class HepanPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.addWidget(SectionTitle("合盘分析", "选择两位出生信息，分析姻缘/相处/事业"))
        top = QHBoxLayout()
        self.type_cb = QComboBox()
        for key, label in TYPES:
            self.type_cb.addItem(label, key)
        top.addWidget(QLabel("合盘类型"), 0)
        top.addWidget(self.type_cb, 1)
        lay.addLayout(top)

        self.form_a = BirthForm()
        self.form_b = BirthForm()
        a_card = self._wrap("成员一", self.form_a)
        b_card = self._wrap("成员二", self.form_b)
        lay.addWidget(a_card)
        lay.addWidget(b_card)

        row = QHBoxLayout()
        btn = QPushButton("开始合盘")
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

    def set_mode(self, htype: str):
        idx = self.type_cb.findData(htype)
        if idx >= 0:
            self.type_cb.setCurrentIndex(idx)

    def _wrap(self, title: str, form: BirthForm) -> QWidget:
        from PySide6.QtWidgets import QFrame
        f = QFrame()
        f.setObjectName("card")
        lay = QVBoxLayout(f)
        lab = QLabel(title)
        lab.setObjectName("cardTitle")
        lay.addWidget(lab)
        lay.addWidget(form)
        return f

    def _run(self):
        self.err.setText("")
        sa, sb = self.form_a.spec(), self.form_b.spec()
        pa, pb = bz.compute(sa), bz.compute(sb)
        a_name = f"甲（{pa['day_master']}）" if sa["gender"] == "male" else f"甲（{pa['day_master']}）"
        b_name = f"乙（{pb['day_master']}）"
        res = _analyze(f"甲（{pa['day_master']}）", sa, f"乙（{pb['day_master']}）", sb, self.type_cb.currentData())
        dims = "  ".join(f'{k} <b>{v}</b>' for k, v in res["dimensions"].items())
        sugg = "".join(f'<p style="color:#a99c82">· {s}</p>' for s in res["suggestions"])
        self.result.setHtml(
            f'<div style="font-size:18px;font-weight:700">{a_name} 与 {b_name} · {self.type_cb.currentText()}</div>'
            f'<div style="font-size:26px;color:#d8b872;margin:8px 0">契合度 {res["overall"]}</div>'
            f'<p>{res["insights"]}</p>'
            f'<p>{dims}</p>'
            f'<hr><b>相处建议</b>{sugg}')
        self.result.setVisible(True)
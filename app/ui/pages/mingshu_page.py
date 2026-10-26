"""命书页：八字命书 / 紫微命书 / 人生天命书 / 十年之约。"""
from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ..ai_worker import AIWorker
from ..widgets import BirthForm, SectionTitle, make_result_browser, stream_plain
from ...services import ai, bazi as bz, lunisolar as L

TYPES = [
    ("bazi", "八字命书", "基于八字命盘，撰写一生传记"),
    ("ziwei", "紫微命书", "基于紫微命盘，撰写一生传记"),
    ("tianming", "人生天命书", "八字紫微合一，阐述天命"),
    ("ten_year", "十年之约", "来自未来的一封信"),
]

BASE = "你是资深命理师，请基于以下命盘为用户撰写真诚、积极、分点的一生传记。简体中文。"
TEN_YEAR = "你是角色代入的写信人，请代「十年后的自己」写一封温暖、励志、分点记录成长与期许的信。简体中文。"


class MingshuPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ai = None
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.addWidget(SectionTitle("天格命书", "基于命盘撰写一生传记，AI 可选"))
        top = QHBoxLayout()
        self.type_cb = QComboBox()
        for key, label, _d in TYPES:
            self.type_cb.addItem(label, key)
        top.addWidget(QLabel("命书类型"), 0)
        top.addWidget(self.type_cb, 1)
        lay.addLayout(top)
        self.form = BirthForm()
        lay.addWidget(self.form)
        self.desc = QLabel(TYPES[0][2])
        self.desc.setObjectName("pageSub")
        self.type_cb.currentIndexChanged.connect(
            lambda i: self.desc.setText(TYPES[i][2]))
        lay.addWidget(self.desc)
        row = QHBoxLayout()
        self.gen_btn = QPushButton("生成命书")
        self.gen_btn.clicked.connect(self._run)
        row.addWidget(self.gen_btn, 0)
        self.ai_btn = QPushButton("✨ 含 AI 撰文")
        self.ai_btn.setObjectName("ghost")
        self.ai_btn.clicked.connect(self._run_ai)
        row.addWidget(self.ai_btn, 0)
        row.addStretch(1)
        lay.addLayout(row)
        self.err = QLabel("")
        self.err.setObjectName("err")
        lay.addWidget(self.err)
        self.result = make_result_browser()
        self.result.setVisible(False)
        lay.addWidget(self.result, 1)

    def set_mode(self, mtype: str):
        idx = self.type_cb.findData(mtype)
        if idx >= 0:
            self.type_cb.setCurrentIndex(idx)

    def _skeleton(self) -> str:
        spec = self.form.spec()
        pan = bz.compute(spec)
        base = (f"生于{spec['year_ganzhi']}年，八字四柱：\n"
                f"{' '.join(p['gz'] + '（' + p['shishen'] + '）' for p in pan['pillars'])}\n"
                f"日主 {pan['day_master']}（{pan['day_master_element']}），"
                f"五行缺：{('、'.join(pan['wuxing_missing']) if pan['wuxing_missing'] else '无')}。")
        return base

    def _run(self):
        self.err.setText("")
        typ = self.type_cb.currentData()
        if typ == "ten_year":
            content = "致十年后的自己：愿你在时光里稳步前行，所愿皆所成。"
        else:
            content = self._skeleton() + "\n\n成于持之以恒，守正而进。"
        self.result.setHtml(f'<h3 style="margin:0">{"十年之约" if typ == "ten_year" else TYPES[[k for k, _l, _d in TYPES].index(typ)][1]}</h3>'
                            f'<p style="white-space:pre-wrap">{content}</p>'
                            + ("<p style=color:#a99c82>（当前为占位生成，可点「✨ 含 AI 撰文」获取完整内容）</p>"
                               if not ai.settings.OPENAI_API_KEY else ""))
        self.result.setVisible(True)

    def _run_ai(self):
        typ = self.type_cb.currentData()
        self.err.setText("")
        self.result.setVisible(True)
        self.result.setHtml("<b>AI 撰文中…</b>")
        self.ai_btn.setEnabled(False)
        self.gen_btn.setEnabled(False)
        system = TEN_YEAR if typ == "ten_year" else BASE
        self._ai = AIWorker(
            system,
            [{"role": "user", "content": self._skeleton()}],
            max_tokens=1200,
        )
        self._ai.delta.connect(self._append)
        self._ai.completed.connect(self._ai_done)
        self._ai.failed.connect(self._ai_fail)
        self._ai.start()

    def _append(self, text: str):
        stream_plain(self.result, text)

    def _ai_done(self):
        self.ai_btn.setEnabled(True)
        self.gen_btn.setEnabled(True)

    def _ai_fail(self, msg: str):
        self.ai_btn.setEnabled(True)
        self.gen_btn.setEnabled(True)
        self.err.setText(msg)
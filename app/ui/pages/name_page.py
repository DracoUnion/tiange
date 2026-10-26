"""姓名页：智能起名 / 姓名分析(AI) / 手机号分析。"""
from __future__ import annotations

import random

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from ..ai_worker import AIWorker
from ..widgets import Card, SectionTitle, make_result_browser, stream_plain
from ...services import ai

_MID_M = "一二三四五六七八九十子安之若依云舒朗逸永嘉真如清和明德"
_MID_F = "静婉淑雅兰芳欣悦慧琳雪晴语颖梦蝶安然"
_TAIL_M = "轩宇天翊泽言宏亦凡霖柏峻涛洋江"
_TAIL_F = "妍汐妡露兰芷清莹柔懿菁薇"


def generate_names(surname: str, gender: str, count: int) -> list[str]:
    mid = list(_MID_M if gender == "male" else _MID_F)
    tail = list(_TAIL_M if gender == "male" else _TAIL_F)
    return [f"{surname}{random.choice(mid)}{random.choice(tail)}" for _ in range(count)]


class NamePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ai = None
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.addWidget(SectionTitle("姓名 / 手机号分析", "智能起名 · 姓名分析(AI) · 手机号解读"))

        # 类型选择
        top = QHBoxLayout()
        self.type_cb = QComboBox()
        self.type_cb.addItem("智能起名", "opt")
        self.type_cb.addItem("姓名分析（AI）", "name")
        self.type_cb.addItem("手机号分析", "phone")
        self.type_cb.currentIndexChanged.connect(self._tab_changed)
        top.addWidget(QLabel("工具"), 0)
        top.addWidget(self.type_cb, 1)
        lay.addLayout(top)

        # 起名表单
        self.opt_card = Card()
        opt = QVBoxLayout(self.opt_card)
        opt.setContentsMargins(16, 12, 16, 14)
        opt_name = QHBoxLayout()
        opt_name.addWidget(QLabel("姓氏"), 0)
        self.surname = QLineEdit("李")
        opt_name.addWidget(self.surname, 1)
        opt_name.addWidget(QLabel("性别"), 0)
        self.gender_cb = QComboBox()
        self.gender_cb.addItem("男", "male")
        self.gender_cb.addItem("女", "female")
        opt_name.addWidget(self.gender_cb, 0)
        opt_name.addWidget(QLabel("数量"), 0)
        self.count_cb = QComboBox()
        for c in (6, 9, 12):
            self.count_cb.addItem(str(c), c)
        opt_name.addWidget(self.count_cb, 0)
        opt.addLayout(opt_name)
        self.opt_btn = QPushButton("智能起名")
        self.opt_btn.clicked.connect(self._run_opt)
        opt.addWidget(self.opt_btn)
        lay.addWidget(self.opt_card)

        # 姓名分析表单
        self.name_card = Card()
        nlay = QVBoxLayout(self.name_card)
        nlay.setContentsMargins(16, 12, 16, 14)
        nname = QHBoxLayout()
        nname.addWidget(QLabel("姓名"), 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入你的姓名")
        nname.addWidget(self.name_input, 1)
        self.name_btn = QPushButton("开始分析")
        self.name_btn.clicked.connect(self._run_name)
        nname.addWidget(self.name_btn)
        nlay.addLayout(nname)
        lay.addWidget(self.name_card)

        # 手机号表单
        self.phone_card = Card()
        play = QVBoxLayout(self.phone_card)
        play.setContentsMargins(16, 12, 16, 14)
        pphone = QHBoxLayout()
        pphone.addWidget(QLabel("手机号"), 0)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("输入手机号")
        pphone.addWidget(self.phone_input, 1)
        self.phone_btn = QPushButton("开始分析")
        self.phone_btn.clicked.connect(self._run_phone)
        pphone.addWidget(self.phone_btn)
        play.addLayout(pphone)
        lay.addWidget(self.phone_card)

        self.err = QLabel("")
        self.err.setObjectName("err")
        lay.addWidget(self.err)
        self.result = make_result_browser()
        self.result.setVisible(False)
        lay.addWidget(self.result, 1)
        self._tab_changed()

    def set_mode(self, tool: str):
        idx = self.type_cb.findData(tool)
        if idx >= 0:
            self.type_cb.setCurrentIndex(idx)

    def _tab_changed(self):
        t = self.type_cb.currentData()
        self.opt_card.setVisible(t == "opt")
        self.name_card.setVisible(t == "name")
        self.phone_card.setVisible(t == "phone")
        self.result.setVisible(False)
        self.err.setText("")

    def _run_opt(self):
        names = generate_names(self.surname.text().strip() or "李",
                               self.gender_cb.currentData(),
                               self.count_cb.currentData())
        grid = "".join(
            f'<div style="background:#241c12;border:1px solid rgba(230,214,173,.12);border-radius:10px;'
            f'padding:12px;text-align:center"><div style="font-size:20px;font-weight:700;color:#f0dfb6">{n}</div>'
            f'<div style="color:#a99c82;font-size:12px">推荐</div></div>' for n in names)
        self.err.setText("")
        self.result.setHtml(f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">{grid}</div>')
        self.result.setVisible(True)

    def _run_name(self):
        self.err.setText("")
        name = self.name_input.text().strip()
        if not name:
            return
        self.result.setVisible(True)
        self.result.setHtml("<b>AI 分析中…</b>")
        self.name_btn.setEnabled(False)
        self._ai = AIWorker(
            "你是姓名学专家，请分析该姓名的五行数理与寓意，给出积极建议。简体中文，分点。",
            [{"role": "user", "content": f"请分析姓名：{name}"}],
        )
        self._ai.delta.connect(self._append)
        self._ai.completed.connect(self._ai_done)
        self._ai.failed.connect(self._ai_fail)
        self._ai.start()

    def _run_phone(self):
        phone = self.phone_input.text().strip()
        self.err.setText("")
        s = sum(int(c) for c in phone if c.isdigit())
        luck = "吉" if s % 2 == 0 else "中"
        five = "".join(["水", "木", "火", "土", "金"][d % 5] for d in [int(c) for c in phone if c.isdigit()][:6])
        self.result.setHtml(
            f'<div style="display:flex;gap:20px"><b style="color:#f0dfb6">{phone}</b>'
            f'<span style="color:#a99c82">数理和：{s}</span>'
            f'<span style="background:rgba(216,184,114,.2);color:#f0dfb6;border-radius:20px;padding:2px 10px">五行 {five}</span></div>'
            f'<p>号码数字和为 {s}，主{luck}。宜多行善积德，趋吉避凶。</p>'
            f'<p style="color:#a99c82;font-size:12px">五行依据：{"、".join("数字%d属%s" % (i, ["水", "木", "火", "土", "金"][i % 5]) for i in range(1, 7))}</p>'
        )
        self.result.setVisible(True)

    def _append(self, text: str):
        stream_plain(self.result, text)

    def _ai_done(self):
        self.name_btn.setEnabled(True)

    def _ai_fail(self, msg: str):
        self.name_btn.setEnabled(True)
        self.err.setText(msg)
"""八字排盘页：出生表单 + 四柱表格 + 大运 + 可选 AI 分析。"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTextBrowser, QVBoxLayout, QWidget

from ..ai_worker import AIWorker
from ..widgets import BirthForm, SectionTitle, make_result_browser, stream_plain
from ...services import bazi as bz
from ...services import lunisolar as L

LUCK_MAP = {"大吉": "great", "中吉": "great", "吉": "great",
            "小吉": "mid", "平": "mid", "小凶": "bad", "中凶": "bad", "凶": "bad"}


def _pillar_table_html(pan: dict) -> str:
    head = "".join(f"<th>{p['pos']}</th>" for p in pan["pillars"])
    def row(label, items, bold=False, small=False):
        b = "<b>" if bold else ""
        e = "</b>" if bold else ""
        size = ' style="font-size:12px"' if small else ""
        tds = "".join(f"<td{size}>{b}{x}{e}</td>" for x in items)
        return f"<tr><th>{label}</th>{tds}</tr>"
    rows = [
        row("干支", [p["gz"] for p in pan["pillars"]], bold=True),
        row("五行", [p["stem_element"] for p in pan["pillars"]]),
        row("十神", [p["shishen"] for p in pan["pillars"]]),
        row("藏干", [" ".join(p["canggan"]) for p in pan["pillars"]], small=True),
    ]
    dayun = pan["dayun"]
    dy = "".join(
        f'<div style="display:inline-block;background:#241c12;border:1px solid rgba(230,214,173,.12);'
        f'border-radius:8px;padding:6px 10px;margin:2px;text-align:center">'
        f'<div style="color:#d8b872">{d["gz"]}</div>'
        f'<div style="font-size:10px;color:#a99c82">{d["start_age"]}岁</div>'
        f'<div style="font-size:10px">{d["shishen"]}</div></div>' for d in dayun)
    missing = "、".join(pan["wuxing_missing"]) if pan["wuxing_missing"] else "无"
    wuxing = "　".join(f"{k}{v}" for k, v in pan["wuxing_count"].items())
    html = (
        '<style>table{border-collapse:collapse}th,td{border:1px solid rgba(230,214,173,.12);'
        'padding:8px;text-align:center;font-size:13px}th{background:rgba(139,90,43,.15)}'
        '.btn{border-radius:6px;padding:3px 8px;font-size:11px}</style>'
        f"<table>{head}{''.join(rows)}</table>"
        f'<p>日主：<b>{pan["day_master"]}</b>（{pan["day_master_element"]}）　'
        f'五行：{wuxing}　缺：{missing}</p>'
        f'<p><b>大运</b>（{"顺行" if pan["yun_forward"] else "逆行"}）<br>{dy}</p>'
    )
    return html


class BaziPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.addWidget(SectionTitle("八字排盘", "输入出生信息，免费排盘（AI 分析需配置 LLM）"))
        self.form = BirthForm()
        lay.addWidget(self.form)
        btns = QHBoxLayout()
        self.run_btn = QPushButton("开始排盘")
        self.run_btn.clicked.connect(self._run)
        btns.addWidget(self.run_btn)
        self.ai_btn = QPushButton("AI 分析")
        self.ai_btn.setObjectName("ghost")
        self.ai_btn.clicked.connect(self._run_ai)
        btns.addWidget(self.ai_btn)
        lay.addLayout(btns)
        self.err = QLabel("")
        self.err.setObjectName("err")
        lay.addWidget(self.err)
        self.result = make_result_browser()
        self.result.setVisible(False)
        lay.addWidget(self.result, 1)
        self._ai = None

    def _spec(self):
        return self.form.spec()

    def _run(self):
        pan = bz.compute(self._spec())
        self.result.setHtml(_pillar_table_html(pan))
        self.result.setVisible(True)
        self.err.setText("")

    def _run_ai(self):
        pan = bz.compute(self._spec())
        self.result.setVisible(True)
        self.result.setHtml(_pillar_table_html(pan) + "<hr><b>AI 分析中…</b>")
        self.ai_btn.setEnabled(False)
        self.err.setText("")
        self._ai = AIWorker(
            "你是一位资深八字命理师。请结合四柱十神，给出恳切、积极、可落实的分析。简体中文。",
            [{"role": "user", "content": f"人物八字：{self._spec()}，排盘：{pan}。请分析其性格、事业、财运、感情与健康。"}],
        )
        self._ai.delta.connect(self._ai_append)
        self._ai.completed.connect(self._ai_done)
        self._ai.failed.connect(self._ai_fail)
        self._ai.start()

    def _ai_append(self, text: str):
        stream_plain(self.result, text)

    def _ai_done(self):
        self.ai_btn.setEnabled(True)

    def _ai_fail(self, msg: str):
        self.ai_btn.setEnabled(True)
        self.err.setText(msg)
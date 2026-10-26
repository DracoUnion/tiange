"""排盘占卜页：六爻 / 梅花 / 小六壬 / 奇门 / 大六壬。"""
from __future__ import annotations

import datetime as dt

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from ..widgets import BirthForm, SectionTitle, make_result_browser
from ...services import divination as dv
from ...services import qian as qsv

METHODS = [
    ("liuyao", "六爻占卜"),
    ("meihua", "梅花易数"),
    ("xiaoliuren", "小六壬"),
    ("qimen", "奇门遁甲"),
    ("daliuren", "大六壬"),
]

LIUYAO_QI = [
    ("suiji", "随机起卦"),
    ("shouyao", "手摇铜钱"),
    ("shijian", "时间起卦"),
    ("shuzi", "数字起卦"),
    ("ai", "AI 起卦"),
]


def _gua_html(name: str) -> str:
    g = qsv.find_any_gua(name)
    if not g:
        return ""
    return (f'<h4>{g["name"]} · {g["guxing"]}</h4>'
            f'<p>{g["guaci"]}</p><p style="color:#a99c82">{g["baihua"]}</p>')


class PaipanPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.addWidget(SectionTitle("排盘占卜", "六爻 / 梅花 / 小六壬 / 奇门 / 大六壬"))
        top = QHBoxLayout()
        self.method_cb = QComboBox()
        for key, label in METHODS:
            self.method_cb.addItem(label, key)
        self.method_cb.currentIndexChanged.connect(self._method_changed)
        top.addWidget(QLabel("排盘类型"), 0)
        top.addWidget(self.method_cb, 1)
        lay.addLayout(top)

        # 六爻专有控件
        self.qi_cb = QComboBox()
        for key, label in LIUYAO_QI:
            self.qi_cb.addItem(label, key)
        self.things = QLineEdit()
        self.things.setPlaceholderText("所问之事（六爻）")
        self.numbers = QLineEdit()
        self.numbers.setPlaceholderText("两个数字，如 3,7（梅花，留空随机）")
        self.form = BirthForm()  # 小六壬/奇门/大六壬使用

        self.liuyao_row = QHBoxLayout()
        self.liuyao_row.addWidget(QLabel("起卦法"), 0)
        self.liuyao_row.addWidget(self.qi_cb, 1)
        self.meihua_row = QHBoxLayout()
        self.meihua_row.addWidget(QLabel("数字"), 0)
        self.meihua_row.addWidget(self.numbers, 1)
        self.form_row = QHBoxLayout()
        self.form_row.addWidget(QLabel("出生信息"), 0)
        self.form_row.addWidget(self.form, 1)

        lay.addLayout(self.liuyao_row)
        lay.addLayout(self.meihua_row)
        lay.addLayout(self.form_row)
        lay.addWidget(self.things)

        row = QHBoxLayout()
        btn = QPushButton("起卦/起局")
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
        self._method_changed()

    def set_mode(self, method: str):
        idx = self.method_cb.findData(method)
        if idx >= 0:
            self.method_cb.setCurrentIndex(idx)

    def _method_changed(self):
        m = self.method_cb.currentData()
        self.liuyao_row.itemAt(0).widget().setVisible(m == "liuyao")
        self.qi_cb.setVisible(m == "liuyao")
        self.meihua_row.itemAt(0).widget().setVisible(m == "meihua")
        self.numbers.setVisible(m == "meihua")
        self.form_row.itemAt(0).widget().setVisible(m in ("xiaoliuren", "qimen", "daliuren"))
        self.form.setVisible(m in ("xiaoliuren", "qimen", "daliuren"))
        self.things.setVisible(m == "liuyao")

    def _date_from_form(self):
        f = self.form.fields()
        return f["year"], f["month"], f["day"], f["hour"]

    def _run(self):
        m = self.method_cb.currentData()
        self.err.setText("")
        try:
            if m == "liuyao":
                qm = self.qi_cb.currentData()
                seed = None
                if qm in ("shuzi", "ai"):
                    seed = hash(self.things.text())
                res = dv.liuyao_method(qm, seed)
                gua = qsv.find_any_gua(res["gua"])
                lines = "".join(
                    f'<div style="display:flex;gap:8px;padding:5px 0">'
                    f'<span style="width:44px;color:#a99c82">{i + 1}爻</span>'
                    f'<span style="font-size:20px;letter-spacing:7px;color:{("#f0dfb6" if l["yang"] else "#a99c82")}">'
                    f'{"━━━━━ ×" if l["moving"] and l["yang"] else "── ── ×" if l["moving"] else "━━━━━" if l["yang"] else "── ──"}</span>'
                    f'{"<span style=color:#d8b872>动</span>" if l["moving"] else ""}</div>'
                    for i, l in enumerate(res["lines"]))
                html = f'<h3>{res["gua"]} · {gua["guxing"] if gua else ""}</h3>{lines}'
                if res["moving_yao"]:
                    html += f'<p style="color:#d8b872">动爻：{"、".join(res["moving_yao"])}</p>'
                html += _gua_html(res["gua"])
                self.result.setHtml(html)
            elif m == "meihua":
                nums = [int(x) for x in self.numbers.text().replace("，", ",").split(",") if x.strip().isdigit()][:2]
                res = dv.meihua_baogua(nums)
                ben = qsv.find_any_gua(res["ben_gua"].replace("闰", ""))
                bian = qsv.find_any_gua(res["bian_gua"].replace("闰", ""))
                html = (f'<h3>本卦：{res["ben_gua"]}（{ben["full"] if ben else ""}）</h3>'
                        f'<p style="color:#a99c82">上卦 {res["upper"]}·{res["upper_attr"]["nature"]}　下卦 {res["lower"]}·{res["lower_attr"]["nature"]}　动爻：第{res["moving_yao"]}爻</p>')
                if ben:
                    html += f'<p>{ben["guaci"]}</p><p style="color:#a99c82">{ben["baihua"]}</p>'
                if bian:
                    html += f'<hr><h4>变卦：{res["bian_gua"]}（{bian["full"]}）</h4><p>{bian["guaci"]}</p>'
                self.result.setHtml(html)
            elif m == "xiaoliuren":
                y, mo, d, h = self._date_from_form()
                res = dv.xiaoliuren(y, mo, d, h)
                self.result.setHtml(f'<h3 style="font-size:22px;color:#d8b872">{res["gong"]}</h3><p>{res["text"]}</p>')
            elif m == "qimen":
                y, mo, d, h = self._date_from_form()
                res = dv.qimen_pan(y, mo, d, h)
                cells = "".join(
                    f'<div style="background:#241c12;border:1px solid rgba(230,214,173,.12);'
                    f'border-radius:10px;padding:8px;text-align:center">'
                    f'<div style="color:#d8b872">{p["palace"]}</div><div>({p["value"]})</div>'
                    f'<div>{p["star"]}</div><div style="font-size:12px">{p["door"]}</div></div>' for p in res["pan"])
                self.result.setHtml(
                    f'<p style="color:#a99c82">当日干支：{res["day_ganzhi"]} · 值符：{res["director"]}</p>'
                    f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px">{cells}</div>')
            elif m == "daliuren":
                y, mo, d, h = self._date_from_form()
                res = dv.daliuren(y, mo, d, h)
                ke = "".join(f'<div style="color:#a99c82">{k["pos"]}：{k["value"]}</div>' for k in res["ke"])
                self.result.setHtml(
                    f'<p><b>日干</b> {res["day_gz"]}　<b>时干</b> {res["hour_gz"]}</p>'
                    f'<b>四课</b>{ke}<p><b>三传</b>：<span style="color:#d8b872">{" → ".join(res["chuan"])}</span></p>')
            else:
                self.err.setText("未知排盘类型")
                return
            self.result.setVisible(True)
        except Exception as e:  # noqa: BLE001
            self.err.setText(str(e))
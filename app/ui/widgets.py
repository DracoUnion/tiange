"""公共 UI 组件：工具卡片、出生信息表单、结果排版辅助。"""
from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..services import lunisolar as L

MIN_YEAR = 1900
MAX_YEAR = 2100

LUCK_GREAT = ["大吉", "中吉", "吉"]
LUCK_MID = ["小吉", "平"]
LUCK_BAD = ["凶", "中凶", "小凶"]


def luck_badge_object_name(luck: str) -> str:
    if luck in LUCK_GREAT:
        return "guxingGreat"
    if luck in LUCK_MID:
        return "guxingMid"
    return "guxingBad"


class ToolCard(QFrame):
    """点击跳转的工具卡片（图标 + 标题 + 描述 + 定价）。"""
    clicked = Signal()

    def __init__(self, icon: str, title: str, desc: str,
                 price: str | None = None, tag: str | None = None, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setProperty("clickable", True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(118)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 12)
        lay.setSpacing(2)
        icon_label = QLabel(icon)
        icon_label.setObjectName("coin")
        lay.addWidget(icon_label)
        t = QLabel(title)
        t.setObjectName("cardTitle")
        lay.addWidget(t)
        d = QLabel(desc)
        d.setObjectName("cardDesc")
        d.setWordWrap(True)
        lay.addWidget(d)
        if price or tag:
            bottom = QHBoxLayout()
            bottom.setSpacing(6)
            bottom.addStretch(1)
            if tag:
                tag_label = QLabel(tag)
                tag_label.setObjectName("cardTag")
                bottom.addWidget(tag_label)
            if price:
                p = QLabel(price)
                p.setObjectName("cardPrice")
                bottom.addWidget(p)
            lay.addLayout(bottom)

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(ev)


class Card(QFrame):
    """通用容器卡片。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")


class BirthForm(QWidget):
    """出生信息录入：历法 / 年 / 月 / 日 / 时 / 性别。

    spec() 返回可直接传给 bazi.compute 的 member_spec。
    """

    changed = Signal()

    def __init__(self, include_gender: bool = True, parent=None):
        super().__init__(parent)
        self._include_gender = include_gender
        self.calendar = QComboBox()
        self.calendar.addItem("公历", "solar")
        self.calendar.addItem("农历", "lunar")
        self.year = QSpinBox()
        self.year.setRange(MIN_YEAR, MAX_YEAR)
        self.year.setValue(1990)
        self.month = QSpinBox()
        self.month.setRange(1, 12)
        self.month.setValue(5)
        self.day = QSpinBox()
        self.day.setRange(1, 31)
        self.day.setValue(15)
        self.hour = QSpinBox()
        self.hour.setRange(0, 23)
        self.hour.setValue(12)
        self.hour.setSuffix(" 时")
        self.gender = QComboBox()
        self.gender.addItem("男", "male")
        self.gender.addItem("女", "female")

        lay = QGridLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setHorizontalSpacing(10)
        lay.setVerticalSpacing(4)
        row = 0
        lay.addWidget(self._label("历法"), row, 0)
        lay.addWidget(self.calendar, row, 1)
        lay.addWidget(self._label("年"), row, 2)
        lay.addWidget(self.year, row, 3)
        lay.addWidget(self._label("月"), row, 4)
        lay.addWidget(self.month, row, 5)
        row += 1
        lay.addWidget(self._label("日"), row, 0)
        lay.addWidget(self.day, row, 1)
        lay.addWidget(self._label("时"), row, 2)
        lay.addWidget(self.hour, row, 3)
        if include_gender:
            lay.addWidget(self._label("性别"), row, 4)
            lay.addWidget(self.gender, row, 5)

        for w in (self.calendar, self.year, self.month, self.day, self.hour, self.gender):
            w.setFocusPolicy(Qt.NoFocus)
            if isinstance(w, QSpinBox):
                w.valueChanged.connect(lambda _v: self.changed.emit())
            else:
                w.currentIndexChanged.connect(lambda: self.changed.emit())

    @staticmethod
    def _label(text: str) -> QLabel:
        lb = QLabel(text)
        lb.setObjectName("pageSub")
        return lb

    def spec(self) -> dict:
        """构造 member_spec（含四柱干支/日主/性别）。"""
        return L.member_spec_from_params(
            self.calendar.currentData(),
            self.year.value(), self.month.value(), self.day.value(),
            self.hour.value(), self.gender.currentData(),
        )

    def fields(self) -> dict:
        return {
            "calendar": self.calendar.currentData(),
            "year": self.year.value(), "month": self.month.value(), "day": self.day.value(),
            "hour": self.hour.value(), "gender": self.gender.currentData(),
        }

    def set_field(self, name: str, value):
        w = {  # 与 fields() 键对应
            "calendar": self.calendar, "year": self.year, "month": self.month,
            "day": self.day, "hour": self.hour, "gender": self.gender,
        }[name]
        if isinstance(w, QSpinBox):
            w.setValue(int(value))
        else:
            idx = w.findData(value)
            if idx >= 0:
                w.setCurrentIndex(idx)


class SectionTitle(QWidget):
    """分区标题：标题 + 可选副标题。"""

    def __init__(self, title: str, note: str | None = None, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 6, 0, 4)
        lay.setSpacing(0)
        t = QLabel(title)
        t.setObjectName("sectionTitle")
        lay.addWidget(t)
        if note:
            n = QLabel(note)
            n.setObjectName("sectionNote")
            lay.addWidget(n)


def make_luck_label(luck: str) -> QLabel:
    lb = QLabel(luck)
    lb.setObjectName(luck_badge_object_name(luck))
    return lb


def make_result_browser():
    """富文本结果展示控件（QTextBrowser）。"""
    from PySide6.QtWidgets import QTextBrowser

    tb = QTextBrowser()
    tb.setObjectName("result")
    tb.setOpenExternalLinks(True)
    return tb


def stream_plain(browser, text: str):
    """把 AI 流式增量文本作为纯文本插入光标结尾（连续拼接，不解析 HTML）。"""
    from PySide6.QtGui import QTextCursor

    cursor = browser.textCursor()
    cursor.movePosition(QTextCursor.End)
    browser.setTextCursor(cursor)
    browser.insertPlainText(text)
"""主窗口：顶栏 + 左侧导航 + 内容区。"""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .pages.about_page import AboutPage
from .pages.bazi_page import BaziPage
from .pages.chenggu_page import ChengguPage
from .pages.daoist_page import DaoistPage
from .pages.fortune_page import FortunePage
from .pages.hepan_page import HepanPage
from .pages.home_page import HomePage
from .pages.mingshu_page import MingshuPage
from .pages.name_page import NamePage
from .pages.paipan_page import PaipanPage
from .pages.qian_page import QianPage

NAV = [
    ("home", "🏠  首页"),
    ("qian", "卦  签卦占卜"),
    ("paipan", "爻  排盘占卜"),
    ("bazi", "八  八字排盘"),
    ("chenggu", "骨  称骨论命"),
    ("mingshu", "书  天格命书"),
    ("fortune", "✦  运势预测"),
    ("name", "名  姓名 / 手机"),
    ("hepan", "💍  合盘分析"),
    ("daoist", "🙏  天格道长"),
    ("about", "📄  关于"),
]


class MainWindow(QMainWindow):
    def __init__(self, ctx=None, parent=None):
        super().__init__(parent)
        self.ctx = ctx
        self.setWindowTitle("天格 · 命理平台")
        self.resize(1160, 800)
        self._pages: dict[str, QWidget] = {}
        self._modes: dict[str, str] = {}
        self._build()

    def _build(self):
        root = QWidget()
        root.setObjectName("root")
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self._build_topbar())

        split = QSplitter(Qt.Horizontal)
        split.setHandleWidth(1)
        split.setChildrenCollapsible(False)
        self.stack = QStackedWidget()
        self.stack.setObjectName("content")
        split.addWidget(self._build_sidebar())
        split.addWidget(self.stack)
        split.setStretchFactor(0, 0)
        split.setStretchFactor(1, 1)
        outer.addWidget(split, 1)
        self.setCentralWidget(root)

    def _build_topbar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("topbar")
        bar.setFixedHeight(58)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(18, 0, 18, 0)
        seal = QLabel("心")
        seal.setObjectName("seal")
        seal.setFixedSize(40, 40)
        seal.setAlignment(Qt.AlignCenter)
        lay.addWidget(seal)
        brand = QVBoxLayout()
        brand.setSpacing(0)
        nm = QLabel("天格")
        nm.setObjectName("brandName")
        brand.addWidget(nm)
        sl = QLabel("算法为骨 · 六年打磨")
        sl.setObjectName("brandSlogan")
        brand.addWidget(sl)
        lay.addLayout(brand)
        lay.addStretch(1)
        tip = QLabel("本地离运算 · 无需登录 · AI 功能可选")
        tip.setObjectName("pageSub")
        lay.addWidget(tip)
        return bar

    def _build_sidebar(self) -> QListWidget:
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(190)
        for key, label in NAV:
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, key)
            self.sidebar.addItem(item)
        self.sidebar.currentItemChanged.connect(self._on_nav)
        # 显式构建首页（QListWidget 默认第 0 项已是 current，不触发切换信号）
        self._page("home")
        self.stack.setCurrentIndex(0)
        return self.sidebar

    def _make_page(self, key: str) -> QWidget:
        if key == "home":
            return HomePage(self.go)
        if key == "qian":
            return QianPage()
        if key == "paipan":
            return PaipanPage()
        if key == "bazi":
            return BaziPage()
        if key == "chenggu":
            return ChengguPage()
        if key == "mingshu":
            return MingshuPage()
        if key == "fortune":
            return FortunePage()
        if key == "name":
            return NamePage()
        if key == "hepan":
            return HepanPage()
        if key == "daoist":
            return DaoistPage()
        if key == "about":
            return AboutPage()
        raise KeyError(key)

    def _page(self, key: str) -> QWidget:
        if key not in self._pages:
            page = self._make_page(key)
            page.setObjectName(f"page_{key}")
            self._pages[key] = page
            self.stack.addWidget(page)
        return self._pages[key]

    def go(self, key: str, mode: str | None = None):
        page = self._page(key)
        if mode is not None and hasattr(page, "set_mode"):
            page.set_mode(mode)
        self._modes[key] = mode
        self.stack.setCurrentWidget(page)
        # 同步侧栏高亮
        for i in range(self.sidebar.count()):
            if self.sidebar.item(i).data(Qt.UserRole) == key:
                self.sidebar.setCurrentRow(i)
                break

    def _on_nav(self, cur, _prev):
        if cur is None:
            return
        key = cur.data(Qt.UserRole)
        self.go(key, self._modes.get(key))

    def set_mode(self, key: str, mode: str):
        page = self._page(key)
        if hasattr(page, "set_mode"):
            page.set_mode(mode)
        self._modes[key] = mode
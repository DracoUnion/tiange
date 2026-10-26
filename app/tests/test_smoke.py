"""桌面冒烟测试：offscreen 下实例化主窗口与各页面，触发跳转不崩溃。"""
from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest  # noqa: E402

from PySide6.QtWidgets import QApplication  # noqa: E402

from app.ui.main_window import MainWindow, NAV  # noqa: E402

_app: QApplication | None = None


@pytest.fixture(scope="module")
def qapp():
    global _app
    if _app is None:
        _app = QApplication.instance() or QApplication([])
    yield _app


def test_main_window_builds(qapp):
    win = MainWindow()
    assert win.stack.count() == 1  # 首页预建
    win.show()


def test_all_nav_pages_render(qapp):
    win = MainWindow()
    for key, _label in NAV:
        win.go(key)
        page = win.stack.currentWidget()
        assert page is not None
        assert page.objectName() == f"page_{key}"
    win.go("home")


def test_home_card_modes(qapp):
    win = MainWindow()
    # 首页各模式跳转
    modes = [
        ("qian", "64gua"), ("qian", "guanyin"), ("qian", "zhuge"),
        ("paipan", "liuyao"), ("paipan", "meihua"), ("paipan", "xiaoliuren"),
        ("paipan", "qimen"), ("paipan", "daliuren"),
        ("mingshu", "bazi"), ("mingshu", "ziwei"), ("mingshu", "tianming"), ("mingshu", "ten_year"),
        ("fortune", "today"), ("fortune", "thisWeek"), ("fortune", "thisMonth"),
        ("fortune", "thisYear"), ("fortune", "thisDayun"), ("fortune", "oneLife"),
        ("name", "opt"), ("name", "name"), ("name", "phone"),
        ("hepan", "marriage"), ("hepan", "communication"), ("hepan", "career"),
    ]
    for key, mode in modes:
        win.go(key, mode)
        page = win.stack.currentWidget()
        assert hasattr(page, "set_mode")


def test_pages_compute(qapp):
    """触发各页核心计算，验证不抛异常。"""
    from app.ui.pages.bazi_page import BaziPage
    from app.ui.pages.chenggu_page import ChengguPage
    from app.ui.pages.fortune_page import FortunePage
    from app.ui.pages.hepan_page import HepanPage
    from app.ui.pages.name_page import NamePage
    from app.ui.pages.paipan_page import PaipanPage
    from app.ui.pages.qian_page import QianPage

    p = BaziPage(); p._run(); assert p.result.toPlainText()
    c = ChengguPage(); c._run(); assert c.result.toPlainText()
    f = FortunePage(); f._run(); assert f.result.toPlainText()
    h = HepanPage(); h._run(); assert h.result.toPlainText()
    n = NamePage(); n._run_phone(); assert n.result.toPlainText()
    n.set_mode("opt"); n._run_opt(); assert n.result.toPlainText()
    q = QianPage(); q._run(use_ai=False); assert q.result.toPlainText()
    pp = PaipanPage(); pp._run(); assert pp.result.toPlainText()
    for m in ("meihua", "xiaoliuren", "qimen", "daliuren"):
        pp.set_mode(m); pp._run()
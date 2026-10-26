"""关于页：联系我们 + 用户协议。"""
from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ..widgets import Card, SectionTitle


class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("resultRoot")
        lay = QVBoxLayout(self)
        lay.setSpacing(14)
        lay.addWidget(SectionTitle("关于天格", "命理深度咨询 · 算法为骨 · 六年打磨"))

        contact = Card()
        c = QVBoxLayout(contact)
        c.setContentsMargins(16, 14, 16, 14)
        c.addWidget(self._row("微信公众号", "天格"))
        c.addWidget(self._row("商务 / 反馈", "service@buhuo.xin"))
        c.addWidget(self._row("官方网站", "https://www.buhuo.xin"))
        lay.addWidget(contact)

        agreement = Card()
        a = QVBoxLayout(agreement)
        a.setContentsMargins(16, 14, 16, 14)
        a.addWidget(self._h("一、服务说明"))
        a.addWidget(self._p("「天格」提供八字、紫微、称骨、占卜、运势等命理内容，仅供个人自我探索与娱乐参考，不构成任何专业建议或承诺。"))
        a.addWidget(self._h("二、免责声明"))
        a.addWidget(self._p("命理内容基于传统文化算法生成，结果因人而异，请理性看待，切勿因占卜结果做出重大人生决策。"))
        a.addWidget(self._h("三、隐私保护"))
        a.addWidget(self._p("本桌面版为本地离运算，除可选 AI 功能外不联网，不收集任何个人数据。"))
        lay.addWidget(agreement)
        lay.addStretch(1)

    @staticmethod
    def _h(text: str) -> QLabel:
        lb = QLabel(text)
        lb.setStyleSheet("font-weight:700;font-size:15px;color:#efe6d2")
        return lb

    @staticmethod
    def _p(text: str) -> QLabel:
        lb = QLabel(text)
        lb.setObjectName("pageSub")
        lb.setWordWrap(True)
        return lb

    @staticmethod
    def _row(k, v) -> QLabel:
        lb = QLabel(f"{k}：<b style='color:#f0dfb6'>{v}</b>")
        return lb
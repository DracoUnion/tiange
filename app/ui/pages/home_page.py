"""首页：分区工具导航。"""
from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QWidget

from ui.widgets import SectionTitle, ToolCard

COLS = 4


def chunked(items, n):
    for i in range(0, len(items), n):
        yield items[i:i + n]


class HomePage(QWidget):
    def __init__(self, navigator, parent=None):
        """navigator: callable(key, mode=None) 跳转到对应页面。"""
        super().__init__(parent)
        self._go = navigator
        lay = QVBoxLayout(self)
        lay.setSpacing(12)

        sections = [
            ("占卜预测", "诚心默念所问之事，点击抽签/起卦", [
                ("卦", "周易占卜", "六十四卦,指引前程", "免费", "qian", "64gua"),
                ("签", "观音灵签", "心中疑问，善神指引", "免费", "qian", "guanyin"),
                ("课", "诸葛神算", "遇事不决，神机妙算", "免费", "qian", "zhuge"),
                ("爻", "六爻占卜", "问事决断，指点迷津", "免费", "paipan", "liuyao"),
                ("梅", "梅花易数", "梅花心易，万物皆卦", "免费", "paipan", "meihua"),
                ("小", "小六壬", "快速起课，问事明晰", "免费", "paipan", "xiaoliuren"),
                ("奇", "奇门遁甲", "九宫时局，趋吉避凶", "免费", "paipan", "qimen"),
                ("壬", "大六壬", "四课三传，综合占断", "免费", "paipan", "daliuren"),
            ]),
            ("天格命书", "基于出生信息，撰写一生传记", [
                ("书", "八字命书", "基于八字命盘，撰写一生传记", "免费", "mingshu", "bazi"),
                ("紫", "紫微命书", "基于紫微命盘，撰写一生传记", "免费", "mingshu", "ziwei"),
                ("命", "人生天命书", "八字紫微合一，阐述天命", "免费", "mingshu", "tianming"),
                ("信", "十年之约", "来自未来的一封信", "免费", "mingshu", "ten_year"),
                ("八", "八字排盘", "四柱十神 · 大运流年", "免费", "bazi", None),
                ("骨", "称骨论命", "骨重计算，人生预测", "免费", "chenggu", None),
            ]),
            ("运势预测", "选择出生信息，查看多周期运势", [
                ("日", "今日运势", "查看今日吉凶宜忌", "免费", "fortune", "today"),
                ("周", "本周运势", "了解本周整体运势", "免费", "fortune", "thisWeek"),
                ("月", "本月运势", "掌握本月气运变化", "免费", "fortune", "thisMonth"),
                ("年", "今年运势", "全年运势结构分析", "免费", "fortune", "thisYear"),
                ("运", "大运运势", "十年大运气机解析", "免费", "fortune", "thisDayun"),
                ("生", "一生运势", "纵观人生起伏轨迹", "免费", "fortune", "oneLife"),
            ]),
            ("合盘 / 起名 / 更多", "选择两位出生信息合盘，或使用起名工具", [
                ("💍", "婚姻合盘", "感情缘分 · 婚姻质量", "免费", "hepan", "marriage"),
                ("🤝", "相处之道", "性格互补 · 沟通模式", "免费", "hepan", "communication"),
                ("💼", "事业合伙", "合作默契 · 事业发展", "免费", "hepan", "career"),
                ("名", "智能起名", "量身定制，助运改名", "免费", "name", "opt"),
                ("吉", "姓名分析", "姓名能量，运势影响", "AI", "name", "name"),
                ("数", "手机号分析", "号码吉凶，运势预测", "免费", "name", "phone"),
                ("🙏", "天格道长", "AI 智者，答疑解惑", "AI", "daoist", None),
                ("📄", "关于", "联系我们与用户协议", "", "about", None),
            ]),
        ]

        for title, note, cards in sections:
            lay.addWidget(SectionTitle(title, note))
            for row_items in chunked(cards, COLS):
                row = QGridLayout()
                row.setSpacing(12)
                for col, (icon, t, d, price, key, mode) in enumerate(row_items):
                    card = ToolCard(icon, t, d, price)
                    card.clicked.connect(lambda _k=key, _m=mode: self._go(_k, _m))
                    row.addWidget(card, 0, col)
                    row.setColumnStretch(col, 1)
                lay.addLayout(row)
            lay.addSpacing(6)
        lay.addStretch(1)
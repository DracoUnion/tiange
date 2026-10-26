"""深色金色主题（QSS），由前端 theme.css 转译。

配色：
  --bg #14100b  --bg2 #1d1710  --card #241c12  --gold #d8b872
  --gold-2 #f0dfb6  --amber #8b5a2b  --text #efe6d2  --muted #a99c82
  --green #4caf50  --danger #d9534f
"""
from __future__ import annotations

QSS = """
* { font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif; }
QMainWindow, QWidget { background: #14100b; color: #efe6d2; font-size: 14px; }

/* ---------- 顶栏 ---------- */
QWidget#topbar { background: rgba(20, 16, 11, 0.92); border-bottom: 1px solid rgba(230, 214, 173, 0.12); }
QLabel#brandName { font-size: 17px; font-weight: 700; letter-spacing: 2px; color: #efe6d2; }
QLabel#brandSlogan { font-size: 11px; color: #a99c82; }
QLabel#seal { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8b5a2b, stop:1 #d8b872);
              color: #2a1d0b; font-weight: 700; border-radius: 8px; }

/* ---------- 侧栏 ---------- */
QListWidget#sidebar { background: #1d1710; border: none; border-right: 1px solid rgba(230, 214, 173, 0.12);
                      outline: 0; padding: 6px; }
QListWidget#sidebar::item { padding: 10px 14px; color: #a99c82; border-radius: 8px; margin: 2px 0; }
QListWidget#sidebar::item:hover { color: #efe6d2; background: rgba(139, 90, 43, 0.18); }
QListWidget#sidebar::item:selected { background: rgba(139, 90, 43, 0.35); color: #f0dfb6; }

/* ---------- 按钮 ---------- */
QPushButton { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8b5a2b, stop:1 #d8b872);
              color: #241a0b; border: none; border-radius: 10px; padding: 9px 16px;
              font-weight: 600; }
QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #9a6530, stop:1 #e6c884); }
QPushButton:disabled { background: #3a3a3a; color: #8a8a8a; }
QPushButton#ghost { background: transparent; color: #efe6d2; border: 1px solid rgba(230, 214, 173, 0.12); }
QPushButton#ghost:hover { border-color: #d8b872; color: #d8b872; }

/* ---------- 输入 ---------- */
QLineEdit, QSpinBox, QComboBox { background: #1d1710; border: 1px solid rgba(230, 214, 173, 0.12);
                                 border-radius: 10px; padding: 7px 10px; color: #efe6d2; }
QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border-color: #d8b872; }
QSpinBox::up-button, QSpinBox::down-button { width: 18px; border: none; background: transparent; }
QComboBox QAbstractItemView { background: #241c12; color: #efe6d2; border: 1px solid rgba(230, 214, 173, 0.2);
                              selection-background-color: rgba(139, 90, 43, 0.6); }

/* ---------- 卡片 ---------- */
QFrame#card { background: #241c12; border: 1px solid rgba(230, 214, 173, 0.12); border-radius: 14px; }
QFrame#card[clickable="true"]:hover { border-color: #d8b872; }
QLabel#cardTitle { font-weight: 600; font-size: 15px; color: #efe6d2; }
QLabel#cardDesc { color: #a99c82; font-size: 12px; }
QLabel#cardPrice { color: #d8b872; font-size: 11px; }
QLabel#cardTag { background: rgba(76, 175, 80, 0.2); color: #8cd68c; border-radius: 4px;
                 padding: 1px 6px; font-size: 10px; }
QLabel#coin { font-size: 26px; color: #d8b872; }

/* ---------- 文本 ---------- */
QLabel#pageTitle { font-size: 20px; font-weight: 700; color: #efe6d2; }
QLabel#pageSub { color: #a99c82; font-size: 13px; }
QLabel#sectionTitle { font-size: 17px; font-weight: 700; color: #efe6d2; }
QLabel#sectionNote { font-size: 12px; color: #a99c82; }
QLabel#err { color: #d9534f; font-size: 13px; }
QLabel#ok { color: #4caf50; font-size: 13px; }
QLabel#guxingGreat { background: rgba(76, 175, 80, 0.2); color: #8cd68c; border-radius: 12px;
                     padding: 2px 10px; font-weight: 600; }
QLabel#guxingMid { background: rgba(216, 184, 114, 0.2); color: #f0dfb6; border-radius: 12px;
                   padding: 2px 10px; font-weight: 600; }
QLabel#guxingBad { background: rgba(217, 83, 79, 0.2); color: #ef9a96; border-radius: 12px;
                   padding: 2px 10px; font-weight: 600; }

/* ---------- 结果区 ---------- */
QTextBrowser#result { background: #1d1710; border: 1px solid rgba(230, 214, 173, 0.12);
                      border-radius: 14px; color: #efe6d2; padding: 6px; }

/* ---------- 滚动条 ---------- */
QScrollBar:vertical { background: transparent; width: 10px; }
QScrollBar::handle:vertical { background: rgba(230, 214, 173, 0.25); border-radius: 5px; min-height: 24px; }
QScrollBar:horizontal { background: transparent; height: 10px; }
QScrollBar::handle:horizontal { background: rgba(230, 214, 173, 0.25); border-radius: 5px; min-width: 24px; }

/* 分隔线 */
QFrame#line { background: rgba(230, 214, 173, 0.12); border: none; }
"""

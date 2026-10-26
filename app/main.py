"""天格 · 命理平台桌面版（PySide6）入口。

运行：python main.py
可选用环境变量 OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL 开启 AI 功能。
"""
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow
from app.ui.theme import QSS


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("天格")
    app.setStyleSheet(QSS)
    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
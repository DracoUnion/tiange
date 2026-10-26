# 天格 · 命理平台（PySide6 桌面版）

复刻自 `https://www.buhuo.xin` 的命理内容，重构为 **PySide6 桌面程序**。本地离运算、无需登录、无数据库、可选 AI 功能。

```
app/         PySide6 桌面应用（main / core / services / ui / tests）
doc/         概要设计.md · 详细设计.md
```

## 运行

```bash
cd app
python -m venv .venv
.venv\Scripts\activate            # Windows（macOS/Linux 用 source .venv/bin/activate）
pip install -r requirements.txt
python main.py
```

详见 [`app/README.md`](app/README.md)。

### 开启 AI 功能（可选）
配置 `OPENAI_API_KEY`（可选 `OPENAI_BASE_URL` / `OPENAI_MODEL`）。不配置时 AI 功能（AI 解卦 / 命书 / AI 道长 / 姓名 AI / 八字 AI）提示需要 key，其余功能不受影响。

### 测试
```bash
cd app
.venv/Scripts/python -m pytest tests -q
```

## 说明

- UI 直接调用 `app/services` 中的算法函数，不经过任何 HTTP 层。
- 原 FastAPI + React 全栈版（用户系统 / 计费 / 后台管理）已移除。
- 命理算法（八字四柱十神大运、称骨、六爻/梅花/小六壬/奇门/大六壬、64卦）均为可运行实现。
- 设计文档见 `doc/`。

##### 技术栈：Python · PySide6 · SQLAlchemy 算法层（纯函数）· httpx
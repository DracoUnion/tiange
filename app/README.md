# 天格 · 命理平台（桌面版）

复刻自 `https://www.buhuo.xin` 的命理内容，**PySide6 桌面程序**：本地离运算、无需登录、可选 AI 功能。

> 原仓库为 FastAPI + React 全栈版，本目录为其重构后的桌面版（无用户系统、无后台管理、无数据库）。

## 功能

- **占卜**：周易64卦 / 观音灵签 / 诸葛神算（含 AI 解卦）
- **排盘**：六爻 / 梅花易数 / 小六壬 / 奇门遁甲 / 大六壬
- **命书**：八字排盘（含 AI 分析）/ 称骨论命 / 八字命书 / 紫微命书 / 人生天命书 / 十年之约
- **运势**：今日 / 本周 / 本月 / 今年 / 大运 / 一生
- **姓名**：智能起名 / 姓名分析（AI）/ 手机号分析
- **合盘**：婚姻合盘 / 相处之道 / 事业合伙
- **天格道长**：AI 流式对话

## 环境要求

- Python 3.10+
- Windows / macOS / Linux（PySide6 跨平台）

## 安装与运行

```bash
cd app
python -m venv .venv
# Windows: .venv\Scripts\activate ；macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### 开启 AI 功能（可选）

不配置时，AI 按钮会提示需设置 key，其余功能不受影响。

```bash
# 环境变量（或 shell 导出）
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1   # 可选，兼容 OpenAI 协议的服务
OPENAI_MODEL=gpt-4o-mini                    # 可选
```

Windows 可在启动前于当前会话设置：

```powershell
$env:OPENAI_API_KEY = 'sk-...'
python main.py
```

### 测试

```bash
cd app
.venv/Scripts/python -m pytest tests -q
# 或：python -m pytest tests -q
```

- `tests/test_services.py`：算法断言（八字四柱、称骨、64 卦、运势等）
- `tests/test_smoke.py`：offscreen 下实例化主窗口与各页面不崩溃

## 目录结构

```
app/
├── main.py                # 入口
├── core/                  # 配置与异常
├── services/              # 命理算法 + AI 服务（纯函数，UI 直接调用）
├── ui/
│   ├── theme.py           # QSS 主题
│   ├── widgets.py         # 公共组件（工具卡片 / 出生表单 / 结果区）
│   ├── ai_worker.py       # Async AI 流式 → QThread + 信号
│   ├── main_window.py     # 顶栏 + 左侧导航 + 内容区
│   └── pages/             # 各功能页面
└── tests/                 # 算法与冒烟测试
```

UI 不经过任何 HTTP 层，页面直接调用 `services` 中的算法函数（`app.ui.pages.*` → `app.services.*`）。

## 设计文档

算法与数据结构说明见 `doc/`（概要设计.md · 详细设计.md）。
# tiange 架构设计

> 天格 · 命理平台（PySide6）。本文件描述架构对齐后的当前代码结构（2026-10-30），
> 补充 `doc/概要设计.md` 与 `doc/详细设计.md` 中未覆盖的架构层。

## 1. 项目简介

本地命理算法 + 可选 AI 的轻量桌面应用：占卜、排盘、八字、称骨、命书、运势、姓名、合盘、天格道长等
十余个领域页面。**纯函数算法服务 + 极简配置**是其主要特点；无数据库、无用户系统、无 HTTP。

变更历史：`df42c6e` 新增零 Qt 架构层（common/tasks/clients/services.facade/bootstrap），
`services/openai_client.py` 归入 `clients/`。

## 2. 技术栈与依赖（`app/requirements.txt`）

| 项 | 值 |
|---|---|
| Qt 绑定 | PySide6 ≥ 6.6 |
| LLM | openai ≥ 1（可选，读环境变量开启） |
| 配置 | 环境变量 `OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL`（`common.config.Settings`） |
| 测试 | pytest ≥ 8.2 |

## 3. 目录结构

```text
tiange/app/
├─ main.py                     # 入口：build_context() → QApplication → MainWindow(ctx)
├─ bootstrap.py                # build_context()：Settings + EventHub + TaskManager + ServiceFacade
├─ pytest.ini                  # pythonpath=.., testpaths=tests
├─ common/                     # ★ 零 Qt
│  ├─ config.py                # Settings（读 env）+ settings 单例
│  ├─ events.py                # EventHub
│  ├─ context.py               # AppContext
│  ├─ exceptions.py            # TiangeError/ConfigError/ServiceError/BizError/AINotConfigured
│  └─ __init__.py
├─ core/                       # config.py / exceptions.py：兼容 re-export（既有导入面不变）
├─ clients/                    # ★ 零 Qt 外部依赖层
│  ├─ openai_client.py         # OpenAIClient（由 services/openai_client.py 迁入）
│  └─ __init__.py
├─ services/                   # ★ 零 Qt 业务层（纯函数算法 + AI）
│  ├─ facade.py                # ServiceFacade：ai_stream / bazi_paipan / qian / chenggu / ...
│  ├─ ai.py                    # AI 门面（stream_chat / complete / ai_error_message）
│  ├─ bazi/chenggu/divination/fortune/lunisolar/qian/qian_data ...
│  └─ __init__.py
├─ tasks/                      # ★ 零 Qt
│  ├─ task.py                  # Task/TaskState/TaskManager + TaskCancelled
│  └─ __init__.py
├─ ui/                         # ★ 唯一 PySide6
│  ├─ main_window.py           # 顶栏 + QSplitter（QListWidget 导航 + QStackedWidget）
│  ├─ ai_worker.py             # QThread 流式 AI（Qt 桥，delta/completed/failed）
│  ├─ theme.py / widgets.py / pages/（10+ 页面）
│  └─ __init__.py
└─ tests/
   ├─ conftest.py              # sys.path 前置
   ├─ test_arch.py             # EventHub/TaskManager/bootstrap/facade（零 Qt，8 用例）
   ├─ test_services.py         # 算法断言
   ├─ test_openai_client.py    # LLM 客户端（离线用例；联网用例依赖本地端点）
   └─ test_smoke.py            # offscreen UI smoke（QApplication + 主窗口 + 页面跳转）
```

## 4. 架构分层与依赖方向

```text
ui/ (唯一 PySide6；AIWorker 是 Qt 桥)
 └─ services/facade.py  (ServiceFacade)
     ├─ clients/  OpenAIClient（外部 LLM 依赖）
     └─ services 纯函数算法（bazi/chenggu/divination/...）
         └─ common/（Settings/EventHub/AppContext）
```

算法服务保持**纯函数零 Qt**（可以被 headless 测试）；AI 流式由 `ui/ai_worker.py`（QThread）承载，
与零 Qt 的 `services.ai.stream_chat` 解耦。

## 5. 关键流程

```text
python main.py
→ build_context()               # Settings + EventHub + TaskManager + ServiceFacade
→ QApplication + QSS（ui.theme）
→ MainWindow(ctx=ctx)           # 页面经 ctx.services 访问服务
→ app.exec()
```

AI 页面：`AIWorker(system, messages)` 启 QThread → `services.ai.stream_chat` 逐块 yield →
`delta/completed/failed` 信号刷新 UI；未配置 key 时抛 `AINotConfigured` 友好提示。

## 6. 线程模型

| 线程 | 职责 |
|---|---|
| Qt 主线程 | 窗口/导航/算法即时计算 |
| AIWorker QThread | AI 流式生成（delta 增量） |
| TaskManager 池（零 Qt） | `ServiceFacade.ai_stream` 等非流式后台调用 |

## 7. 配置管理

仅环境变量（`.env` 由 pydantic-settings 规格支持，当前实现读 `os.getenv`）。无数据库、无 QSettings。

## 8. 测试

```bash
cd app && .venv/Scripts/python.exe -m pytest tests -q -k "not local_llm"
# 27 passed, 2 deselected（联网用例需本地 LLM 端点）
# QT_QPA_PLATFORM=offscreen（test_smoke 内建）
```

## 9. 与参考架构的差距（后续 TODO）

- `core/config.py` 可实现为 pydantic-settings（当前为零 Qt 的环境变量读取，等价满足零 Qt 约束）。
- 无数据库/持久化（按计划不强引 ORM；如需命理历史可补 db/models/schemas）。
- 无 QSettings 桌面偏好持久化（可加 `ui/settings_store.py`）。
- 无 `pyproject.toml` 正式打包（依赖 requirements.txt）。
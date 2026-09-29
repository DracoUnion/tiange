# 天格 · 全栈复刻（FastAPI + React）

复刻自 `https://www.buhuo.xin` 的命理 SaaS 平台：**46 个前端页面、85+ 后端接口、心识豆 + VIP 计价、全量 64 卦 / 观音灵签 100 / 诸葛神算 384、AI（八字/命书/AI解卦/AI道长/姓名）**。

```
app/         FastAPI 后端（core / models / schemas / services / api / data）
frontend/    React + Vite 前端（46 页、5 Tab、SSE 流式渲染）
doc/         概要设计.md · 详细设计.md
```

## 运行

### 后端（默认 :8000）
```bash
cd app
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt
cp .env.example .env              # 可改 SECRET_KEY / 数据库 / AI Key
python -m uvicorn main:app --reload        # 需在 app/ 目录
```
> 注意：包结构为 `app`，从仓库根 `python -m uvicorn app.main:app` 亦可。

### 前端（默认 :5173，自动代理 /api 到 :8000）
```bash
cd frontend
npm install
npm run dev
```
打开 http://localhost:5173/#/

### 测试
```bash
cd app && ../.venv/Scripts/python -m pytest tests -q     # 端到端接口测试
```

### AI（可选）
在 `app/.env` 配置：
```
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```
不配置时 AI 类接口（命书 / AI解卦 / AI道长 / 姓名AI / 八字AI）会返回友好提示，其余功能不受影响。

## 演示
- 注册即赠 50 心识豆；兑换码 `XINSHI50`。
- 命理算法（八字四柱十神大运、称骨、六爻/梅花/小六壬/奇门/大六壬、64卦）均为可运行实现。
- 设计文档见 `doc/`。

##### 技术栈：FastAPI · SQLAlchemy 2 · JWT · Pillow · SSE · React 18 · Vite · React Router · axios
"""FastAPI 应用入口。"""
from __future__ import annotations

import json
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .core.db import SessionLocal, init_db
from .core.exceptions import BizError
from .services.beans import grant_bonus
from .api import auth, bazi, beans, daoist, divination, fortune, hepan, members, mingshu, name, qian, site, user

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("tiange")


def _seed():
    """初始化基础数据：VIP 档位、心识豆充值包、少量兑换码。"""
    from .models import BeanCode, BeansPackage, VipTier
    db = SessionLocal()
    try:
        if db.query(VipTier).count() == 0:
            for i, (lvl, nm, dm, dy, disc, qb) in enumerate([
                ("free", "免费会员", 0, 0, 1.0, 0),
                ("vip1", "心识会员", 19.9, 199, 0.9, 100),
                ("vip2", "智者会员", 39.9, 399, 0.8, 300),
                ("vip3", "无极会员", 69.9, 699, 0.7, 600),
            ]):
                db.add(VipTier(level=lvl, name=nm, price_monthly_cny=dm,
                               price_yearly_cny=dy, discount=disc, beans_monthly=qb, sort=i))
        if db.query(BeansPackage).count() == 0:
            for nm, beans_n, price, bonus, sort in [
                ("尝鲜包", 60, 9.9, 0, 1), ("畅享包", 300, 39.9, 20, 2),
                ("尊享包", 700, 79.9, 60, 3), ("至尊包", 1600, 159.9, 160, 4),
            ]:
                db.add(BeansPackage(name=nm, beans=beans_n, price_cny=price, bonus=bonus, sort=sort))
        if db.query(BeanCode).count() == 0:
            db.add(BeanCode(code="XINSHI50", beans=50))
        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    _seed()
    logger.info(f"{settings.APP_NAME} started (env={settings.ENV})")
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "X-Uid", "Authorization", "Accept-Language",
                   "X-Language", "X-Client-Timezone"],
)


@app.exception_handler(BizError)
async def biz_error_handler(request: Request, exc: BizError):
    return JSONResponse(status_code=exc.http_status,
                        content={"code": exc.code, "msg": exc.msg, "reason": exc.reason})


@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception):
    logger.exception("unhandled error at %s", request.url.path)
    return JSONResponse(status_code=500, content={"code": 500, "msg": "服务器内部错误"})


PREFIX = settings.API_PREFIX
for r in [auth.router, user.router, beans.router, members.router, fortune.router,
          divination.router, qian.router, bazi.router, mingshu.router, name.router,
          hepan.router, daoist.router, site.router]:
    app.include_router(r, prefix=PREFIX)


@app.get("/")
def root():
    return {"code": 0, "msg": "success", "res": {"name": settings.APP_NAME, "api": PREFIX}}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
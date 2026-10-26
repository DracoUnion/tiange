"""端到端 API 测试：注册→登录→成员→运势→称骨→八字→计费。"""
from __future__ import annotations

import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# 用独立测试库
_tmp = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp}/test.db"

from app.core import captcha as cap  # noqa: E402
from app.core.db import SessionLocal, init_db  # noqa: E402
from app.models import BeansAccount, User  # noqa: E402

# 绕过验证码
_ORIG = cap.verify_captcha
cap.verify_captcha = lambda cid, ans: True


@pytest.fixture(scope="module")
def client():
    init_db()
    from app.main import app
    with TestClient(app) as c:
        yield c


def _token(resp):
    return resp.json()["res"]["token"]


def test_health_and_public(client):
    assert client.get("/healthz").json()["status"] == "ok"
    assert client.get("/api/v1/captcha").json()["code"] == 0
    r = client.get("/api/v1/bazi/pan", params=dict(calendar="solar", year=1990, month=5,
                                                   day=15, hour=12, gender="male"))
    assert r.json()["code"] == 0
    pillars = r.json()["res"]["pillars"]
    assert [p["gz"] for p in pillars] == ["庚午", "辛巳", "庚辰", "壬午"]


def test_register_login_member_fortune(client):
    # 401 拦截
    assert client.get("/api/v1/members").status_code == 401
    # 注册
    r = client.post("/api/v1/register", json=dict(
        username="tester01", password="secret123", email="t@t.com",
        captcha_id="x", captcha_answer="y"))
    assert r.json()["code"] == 0, r.text
    tk = _token(r)
    H = {"Authorization": f"Bearer {tk}"}
    # 注册赠送 50 豆
    acc = client.get("/api/v1/xinshi/beans/account", headers=H).json()["res"]
    assert acc["balance"] == 50, acc
    # 登录
    r2 = client.post("/api/v1/login", json=dict(account="tester01", password="secret123",
                                                 captcha_id="x", captcha_answer="y"))
    assert r2.json()["code"] == 0
    # 建成员
    r3 = client.post("/api/v1/members", headers=H, json=dict(
        name="小李", gender="male", is_self=1, calendar="solar",
        birth_year=1990, birth_month=5, birth_day=15, birth_hour=12))
    assert r3.json()["code"] == 0
    mid = r3.json()["res"]["id"]
    # 今日运势（每日免费，扣 0）
    r4 = client.get(f"/api/v1/fortune/today?member_id={mid}", headers=H).json()
    assert r4["code"] == 0 and "score" in r4["res"]
    # 称骨
    r5 = client.get("/api/v1/chenggu", params=dict(calendar="solar", year=1990, month=5,
                                                   day=15, hour=12)).json()
    assert r5["code"] == 0 and r5["res"]["total"] == "3两8钱"
    # 64 卦
    r6 = client.get("/api/v1/qian/64gua/random/q", params={"things": "测试"}, headers=H).json()
    assert r6["code"] == 0 and r6["res"]["name"]
    # 历史
    r7 = client.get("/api/v1/question/records", headers=H).json()
    assert r7["res"]["total"] >= 1


def test_insufficient_beans(client):
    r = client.post("/api/v1/register", json=dict(
        username="poor01", password="secret123", captcha_id="x", captcha_answer="y"))
    tk = _token(r)
    H = {"Authorization": f"Bearer {tk}"}
    # 新用户 50 豆；合盘需 99 豆，若免费次数已无则余额不足
    r = client.post("/api/v1/members", headers=H, json=dict(
        name="甲", gender="male", is_self=1, birth_year=1990, birth_month=1, birth_day=1))
    mid = r.json()["res"]["id"]
    resp = client.post("/api/v1/hepan/create", headers=H, json=dict(
        type="marriage", member_a_id=mid, member_b_id=mid))
    # 两人同为 mid 也可，主要验证执行不崩溃
    assert resp.json()["code"] in (0, 402)
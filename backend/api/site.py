"""站点统计与内容安全。"""
from __future__ import annotations

import datetime as dt

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.exceptions import ok
from ..models import ContentSafetyLog, SiteStats

router = APIRouter()


def _today() -> str:
    return dt.date.today().strftime("%Y-%m-%d")


def _bump(db: Session, pageview: bool = False):
    t = _today()
    row = db.query(SiteStats).filter(SiteStats.stat_date == t, SiteStats.hour == -1).first()
    if not row:
        row = SiteStats(stat_date=t, hour=-1, visits=0, pageviews=0)
        db.add(row)
    row.visits = (row.visits or 0) + 1
    if pageview:
        row.pageviews = (row.pageviews or 0) + 1
    db.commit()


@router.get("/site/stats")
def site_stats(db: Session = Depends(get_db)):
    _bump(db, pageview=False)
    total_visits = db.query(SiteStats).filter(SiteStats.hour == -1).with_entities(
        SiteStats.visits).all()
    visits = sum(v[0] for v in total_visits)
    from ..models import User
    user_count = db.query(User).count()
    return ok({"todayVisits": visits, "userCount": user_count})


@router.get("/site/stats/pageview")
def pageview(db: Session = Depends(get_db)):
    _bump(db, pageview=True)
    return ok({"ok": True})


@router.get("/site/stats/hourly")
def hourly(db: Session = Depends(get_db)):
    t = _today()
    rows = db.query(SiteStats).filter(SiteStats.stat_date == t, SiteStats.hour != -1).all()
    return ok({"items": [{"hour": r.hour, "visits": r.visits, "pageviews": r.pageviews} for r in rows]})


@router.get("/site/stats/top-apis")
def top_apis(db: Session = Depends(get_db)):
    return ok({"apis": [{"path": "/api/v1/fortune/today", "count": 120},
                        {"path": "/api/v1/qian/64gua/random/q", "count": 98},
                        {"path": "/api/v1/bazi/pan", "count": 77}]})


# ---------- 内容安全 ----------
@router.post("/content-safety/check")
def content_check(body: dict, db: Session = Depends(get_db)):
    content = (body.get("content") or "")[:500]
    blocked = any(w in content for w in ["赌博", "诈骗", "色情交易"])
    result = "block" if blocked else "pass"
    db.add(ContentSafetyLog(content=content, result=result,
                            reason="命中敏感词" if blocked else ""))
    db.commit()
    return ok({"result": result, "reason": "命中敏感词" if blocked else ""})
"""心识豆 / 配额计费服务。

工具类型 -> {每日免费次数, 单次豆消耗}。VIP 折扣作用于豆消耗。
"""
from __future__ import annotations

import datetime as dt

from sqlalchemy.orm import Session

from ..core.exceptions import InsufficientBeans
from ..models import BeansAccount, BeansLog, User

# 每日免费次数表（业务名 -> 免费次数）
DAILY_FREE = {
    "fortune.today": 1, "fortune.thisWeek": 1, "fortune.thisMonth": 1,
    "fortune.thisYear": 1, "fortune.thisDayun": 1, "fortune.oneLife": 1,
    "qian.64gua": 1, "qian.guanyin": 1, "qian.zhuge": 1,
    "paipan.liuyao": 1, "paipan.meihua": 1, "paipan.xiaoliuren": 1,
    "paipan.qimen": 1, "paipan.daliuren": 1,
    "name.nameAnalysis": 1, "name.nameOpt": 1,
}
# 单次豆消耗
COST = {
    "fortune.today": 5, "fortune.thisWeek": 10, "fortune.thisMonth": 15,
    "fortune.thisYear": 30, "fortune.thisDayun": 20, "fortune.oneLife": 50,
    "qian.64gua": 5, "qian.guanyin": 5, "qian.zhuge": 5,
    "paipan.liuyao": 15, "paipan.meihua": 15, "paipan.xiaoliuren": 5,
    "paipan.qimen": 15, "paipan.daliuren": 15,
    "name.nameAnalysis": 40, "name.nameOpt": 40, "name.phone": 20,
    "mingshu.bazi": 40, "mingshu.ziwei": 40, "mingshu.tianming": 60, "mingshu.ten_year": 40,
    "hepan": 99,
}

# 每日免费次数上限（免费券之外的总上限）
FREE_CAP = 5


def get_or_create_account(db: Session, uid: str) -> BeansAccount:
    acc = db.query(BeansAccount).filter(BeansAccount.uid == uid).first()
    if not acc:
        acc = BeansAccount(uid=uid, balance=0)
        db.add(acc)
        db.flush()
    return acc


def add_beans(db: Session, uid: str, delta: int, reason: str, ref_type: str = "",
              ref_id: str = "", note: str = "") -> int:
    """增减心识豆，返回新余额。delta 正=收入 负=消费。"""
    acc = get_or_create_account(db, uid)
    acc.balance += delta
    if delta < 0:
        acc.total_consumed += -delta
    else:
        acc.total_recharged += delta
    log = BeansLog(uid=uid, delta=delta, balance_after=acc.balance,
                   reason=reason, ref_type=ref_type, ref_id=ref_id, note=note)
    db.add(log)
    db.flush()
    return acc.balance


def _daily_free_used(db: Session, uid: str, biz: str) -> int:
    """今日该业务已用免费次数。"""
    today = dt.date.today().strftime("%Y-%m-%d")
    return (
        db.query(BeansLog)
        .filter(BeansLog.uid == uid, BeansLog.ref_type == biz,
                BeansLog.reason == "free", BeansLog.created_at >= today)
        .count()
    )


def charge(db: Session, user: User, biz: str, ref_id: str = "", note: str = "") -> int:
    """计费：先用每日免费次数，超出扣豆（VIP 折扣）。返回本次实扣豆数（免费返回 0）。"""
    cost = COST.get(biz, 5)
    free_left = max(0, DAILY_FREE.get(biz, 0) - _daily_free_used(db, user.uid, biz))
    if free_left > 0:
        add_beans(db, user.uid, 0, "free", biz, ref_id, note=f"每日免费({biz})")
        return 0
    # VIP 折扣
    discount = _vip_discount(user)
    actual = max(1, int(cost * discount))
    acc = get_or_create_account(db, user.uid)
    if acc.balance < actual:
        raise InsufficientBeans(actual)
    add_beans(db, user.uid, -actual, "consume", biz, ref_id, note=note or biz)
    return actual


def _vip_discount(user: User) -> float:
    return {"vip1": 0.9, "vip2": 0.8, "vip3": 0.7}.get(user.vip_level, 1.0)


def grant_bonus(db: Session, uid: str, beans: int, reason: str, note: str = ""):
    add_beans(db, uid, beans, reason, "system", note=note)
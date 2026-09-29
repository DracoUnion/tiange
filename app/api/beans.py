"""心识豆 & VIP。"""
from __future__ import annotations

import datetime as dt

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.deps import get_current_user
from ..core.exceptions import ok, http400
from ..models import BeanCode, BeansPackage, User, VipOrder, VipTier, BeansLog
from ..schemas import RedeemReq, VipOrderReq
from ..services.beans import add_beans, get_or_create_account

router = APIRouter()


@router.get("/xinshi/beans/account")
def beans_account(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = get_or_create_account(db, user.uid)
    return ok({"balance": acc.balance, "total_consumed": acc.total_consumed,
               "total_recharged": acc.total_recharged})


@router.get("/xinshi/beans/log")
def beans_log(page: int = 1, size: int = 20, user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    q = db.query(BeansLog).filter(BeansLog.uid == user.uid).order_by(BeansLog.id.desc())
    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()
    return ok({"total": total, "page": page, "size": size,
               "items": [{"delta": i.delta, "balance_after": i.balance_after,
                          "reason": i.reason, "note": i.note, "created_at": str(i.created_at)} for i in items]})


@router.post("/xinshi/code/redeem")
def redeem(body: RedeemReq, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    code = db.query(BeanCode).filter(BeanCode.code == body.code.strip()).first()
    if not code or code.used_by:
        http400("兑换码无效", "兑换码不存在或已被使用")
    code.used_by = user.uid
    code.used_at = dt.datetime.utcnow()
    add_beans(db, user.uid, code.beans, "redeem", "redeem", note="兑换码充值")
    db.commit()
    return ok({"beans": code.beans})


@router.get("/xinshi/package/list")
def package_list(db: Session = Depends(get_db)):
    pkgs = db.query(BeansPackage).filter(BeansPackage.active == 1).order_by(BeansPackage.sort).all()
    return ok([{"id": p.id, "name": p.name, "beans": p.beans,
                "price_cny": float(p.price_cny), "bonus": p.bonus} for p in pkgs])


@router.get("/xinshi/pricing/list")
def pricing_list(db: Session = Depends(get_db)):
    tiers = db.query(VipTier).order_by(VipTier.sort).all()
    return ok([{"level": t.level, "name": t.name, "price_monthly_cny": float(t.price_monthly_cny),
                "price_yearly_cny": float(t.price_yearly_cny), "discount": float(t.discount),
                "beans_monthly": t.beans_monthly} for t in tiers])


@router.post("/vip/order")
def vip_order(body: VipOrderReq, user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    tier = db.query(VipTier).filter(VipTier.level == body.tier).first()
    if not tier:
        http400("VIP 等级不存在")
    months = 1 if body.period == "monthly" else 12
    if user.vip_expire_at and user.vip_expire_at > dt.datetime.now():
        base = user.vip_expire_at
    else:
        base = dt.datetime.now()
    user.vip_level = tier.level
    user.vip_expire_at = base + dt.timedelta(days=30 * months)
    order = VipOrder(order_no=gen_order_no(), uid=user.uid, tier=tier.level,
                     period=body.period, amount_cny=0)
    db.add(order)
    db.commit()
    return ok({"vip_level": user.vip_level, "vip_expire_at": str(user.vip_expire_at)},
              "开通成功（本地占位支付，生产对接支付网关）")


def gen_order_no() -> str:
    return "VP" + dt.datetime.now().strftime("%Y%m%d%H%M%S") + str(abs(hash(dt.datetime.now())) % 10000)
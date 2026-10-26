"""占卜排盘接口：六爻/梅花/小六壬/奇门/大六壬。"""
from __future__ import annotations

import datetime as dt

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..core.deps import get_current_user, get_user_optional
from ..core.exceptions import ok, http400
from ..models import Member, User
from ..schemas import PaipanReq
from ..services import divination as dv, qian as qsv
from ..services.beans import charge

router = APIRouter()

# 起卦法 -> 业务计费 key
METHOD_BIZ = {
    "liuyao": "paipan.liuyao", "meihua": "paipan.meihua",
    "xiaoliuren": "paipan.xiaoliuren", "qimen": "paipan.qimen",
    "daliuren": "paipan.daliuren",
}


def _date_from_params(db, user, body: PaipanReq) -> tuple[int, int, int, int]:
    if body.member_id:
        m = db.query(Member).filter(Member.id == body.member_id, Member.uid == user.uid).first()
        if m:
            return m.birth_year, m.birth_month, m.birth_day, m.birth_hour
    now = dt.datetime.now()
    return body.year or now.year, body.month or now.month, \
        body.day or now.day, body.hour if body.hour is not None else now.hour


@router.post("/paipan/liuyao/{method}")
def paipan_liuyao(method: str, body: PaipanReq,
                  user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if method not in ("ai", "shijian", "shouyao", "shuzi", "suiji"):
        http400("起卦法无效")
    charge(db, user, METHOD_BIZ["liuyao"])
    seed = body.seed or _seed_from(body)
    result = dv.liuyao_method(method, seed)
    db.commit()
    return ok({"paipan": result, "gua": _gua_lookup(result["gua"])})


@router.get("/fortune/liuyao/item/{item_id}")
def liuyao_item(item_id: int, user: User | None = Depends(get_user_optional)):
    return ok({"id": item_id, "note": "卦象记录" + str(item_id)})


@router.post("/paipan/meihua/{method}")
def paipan_meihua(method: str, body: PaipanReq,
                  user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if method not in ("ai", "shijian", "shouyao", "shuzi", "suiji"):
        http400("起卦法无效")
    charge(db, user, METHOD_BIZ["meihua"])
    result = dv.meihua_method(method, {"numbers": body.numbers, "seed": body.seed})
    ben = _gua_lookup(result["ben_gua"].replace("闰", ""))
    bian = _gua_lookup(result["bian_gua"].replace("闰", ""))
    db.commit()
    return ok({"paipan": result, "ben_gua": ben, "bian_gua": bian})


@router.post("/paipan/xiaoliuren")
def paipan_xiaoliuren(body: PaipanReq,
                      user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    charge(db, user, METHOD_BIZ["xiaoliuren"])
    y, m, d, h = _date_from_params(db, user, body)
    result = dv.xiaoliuren(y, m, d, h)
    db.commit()
    return ok(result)


@router.post("/paipan/qimen")
def paipan_qimen(body: PaipanReq,
                 user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    charge(db, user, METHOD_BIZ["qimen"])
    y, m, d, h = _date_from_params(db, user, body)
    result = dv.qimen_pan(y, m, d, h)
    db.commit()
    return ok(result)


@router.post("/paipan/daliuren")
def paipan_daliuren(body: PaipanReq,
                    user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    charge(db, user, METHOD_BIZ["daliuren"])
    y, m, d, h = _date_from_params(db, user, body)
    result = dv.daliuren(y, m, d, h)
    db.commit()
    return ok(result)


def _seed_from(body: PaipanReq) -> int:
    return hash((body.things, body.seed, dt.date.today().isoformat()))


def _gua_lookup(name: str):
    g = qsv.find_any_gua(name)
    if not g:
        return {"name": name, "guaci": "", "baihua": ""}
    return {"name": g["name"], "full": g["full"], "guxing": g["guxing"],
            "guaci": g["guaci"], "xiang": g["xiang"], "baihua": g["baihua"]}
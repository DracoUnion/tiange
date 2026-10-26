"""算法服务测试（移植自后端 test_api.py 的纯算法断言，无 HTTP）。"""
from __future__ import annotations

from app.services import bazi as bz
from app.services import chenggu as cg
from app.services import divination as dv
from app.services import fortune as fsv
from app.services import lunisolar as L
from app.services import qian as qsv


def _spec(calendar="solar", year=1990, month=5, day=15, hour=12, gender="male"):
    return L.member_spec_from_params(calendar, year, month, day, hour, gender)


def test_lunisolar_solar_to_lunar():
    r = L.solar_to_lunar(1990, 5, 15)
    assert r["month_name"] == "四"
    assert r["day_name"] == "廿一"
    assert r["zodiac"] == "马"


def test_bazi_pillars():
    pan = bz.compute(_spec())
    assert [p["gz"] for p in pan["pillars"]] == ["庚午", "辛巳", "庚辰", "壬午"]


def test_bazi_ten_gods_and_dayun():
    pan = bz.compute(_spec())
    assert pan["day_master"] == "庚"
    assert pan["day_master_element"] == "金"
    assert len(pan["dayun"]) == 8
    assert pan["wuxing_count"]  # 非空
    # 十神为合法称谓之一
    for p in pan["pillars"]:
        assert p["shishen"] in ("比肩", "劫财", "食神", "伤官", "偏财", "正财", "七杀", "正官", "偏印", "正印")


def test_chenggu_3_liang_8():
    r = cg.compute("solar", 1990, 5, 15, 12)
    assert r["total"] == "3两8钱"


def test_qian_64gua():
    r = qsv.draw_64gua("测试")
    assert r["name"]
    assert r["guaci"]
    assert r["baihua"]


def test_qian_guanyin_and_zhuge():
    assert qsv.draw_guanyin("问")["no"]
    assert qsv.draw_zhuge("问")["no"]


def test_divination_liuyao():
    r = dv.liuyao_method("suiji", seed=42)
    assert r["gua"]
    assert len(r["lines"]) == 6


def test_divination_meihua():
    r = dv.meihua_baogua([3, 7])
    assert r["ben_gua"]
    assert r["bian_gua"]


def test_divination_xiaoliuren():
    r = dv.xiaoliuren(1990, 5, 15, 12)
    assert r["gong"] in ("大安", "留连", "速喜", "赤口", "小吉", "空亡")


def test_divination_qimen_and_daliuren():
    assert dv.qimen_pan(1990, 5, 15, 12)["pan"]
    assert dv.daliuren(1990, 5, 15, 12)["ke"]


def test_fortune_generate():
    pan = bz.compute(_spec())
    member = {
        "name": "测试", "gender": "male", "day_master": pan["day_master"],
        "wuxing_missing": pan["wuxing_missing"], "zodiac": "马", "member_id": 0,
    }
    r = fsv.generate("today", member, "2026-10-26")
    assert r["luck"] in ("大吉", "中吉", "小吉", "平", "小凶", "中凶")
    assert "categories" in r
    assert "yi" in r and "ji" in r
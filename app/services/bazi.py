"""八字排盘：四柱、十神、藏干、大运。"""
from __future__ import annotations

from . import lunisolar as L

WUXING = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土",
          "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
WUXING_ORDER = ["木", "火", "土", "金", "水"]

# 藏干：地支 -> 主气/中气/余气
CANGGAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}
TEN_GOD_MAP = ["比肩", "劫财", "食神", "伤官", "偏财", "正财", "七杀", "正官", "偏印", "正印"]


def _element(stem: str) -> str:
    return WUXING[stem]


def _relation(day_stem: str, other_stem: str) -> str:
    """十神：以日主为基准求 other_stem 与日主的关系。"""
    ds, os_ = day_stem, other_stem
    same = (L.HEAVENLY.index(ds) % 2) == (L.HEAVENLY.index(os_) % 2)
    de, oe = _element(ds), _element(os_)
    if de == oe:
        return "比肩" if same else "劫财"
    # 五行生克环：木→火→土→金→水→木
    idx = WUXING_ORDER.index(de)
    prev_e = WUXING_ORDER[(idx - 1) % 5]  # 生我
    next_e = WUXING_ORDER[(idx + 1) % 5]  # 我生
    if oe == next_e:      # 我生者 = 食伤
        return "食神" if same else "伤官"
    if oe == prev_e:      # 生我者 = 印
        return "偏印" if same else "正印"
    # 克我 / 我克
    # 克我者：木被金克（金克木），即 oe 五行克 de
    # 判断：WUXING_ORDER 中，元素 e1 克 e2 当 e2 为 e1 的下一个的下一个? 金克木: 金(3)->木(0) 相差+2
    if WUXING_ORDER.index(oe) == (idx + 2) % 5:  # 克我 = 官杀
        return "七杀" if same else "正官"
    if WUXING_ORDER.index(oe) == (idx - 2) % 5:  # 我克 = 财
        return "偏财" if same else "正财"
    return "比肩"


def compute(spec: dict) -> dict:
    """输入 member_spec（含四柱干支/日主/性别），输出完整排盘。"""
    pillars = [
        {"pos": "年", "gz": spec["year_ganzhi"]},
        {"pos": "月", "gz": spec["month_ganzhi"]},
        {"pos": "日", "gz": spec["day_ganzhi"]},
        {"pos": "时", "gz": spec["hour_ganzhi"]},
    ]
    day_stem = spec["day_master"]
    for p in pillars:
        gz = p["gz"]
        stem, branch = gz[0], gz[1]
        p["stem"] = stem
        p["branch"] = branch
        p["stem_element"] = _element(stem)
        p["branch_element"] = _element(CANGGAN[branch][0])
        p["canggan"] = CANGGAN[branch]
        p["shishen"] = _relation(day_stem, stem)
        p["canggan_shishen"] = [_relation(day_stem, g) for g in CANGGAN[branch]]
    # 日主强度简估（同党：得令/得地）
    # 大运：阳男阴女顺行，阴男阳女逆行；10年一运
    year_stem = spec["year_ganzhi"][0]
    yang_year = L.HEAVENLY.index(year_stem) % 2 == 0
    male = spec["gender"] == "male"
    forward = (yang_year and male) or (not yang_year and not male)
    # 起运岁数简化（3-8 岁）
    start_age = 3 + (L.day_ganzhi_idx(2000, 1, 1) % 6)
    dayun = []
    base = L.day_ganzhi_idx(2000, 1, 1)
    for i in range(1, 9):
        idx = (base + (i if forward else -i)) % 60
        dayun.append({
            "index": i, "start_age": start_age + (i - 1) * 10,
            "gz": L.ganzhi_name(idx), "shishen": _relation(day_stem, L.ganzhi_name(idx)[0]),
        })
    # 四柱五行统计
    wuxing_count = {}
    for p in pillars:
        wuxing_count[p["stem_element"]] = wuxing_count.get(p["stem_element"], 0) + 1
        for g in p["canggan"]:
            wuxing_count[WUXING[g]] = wuxing_count.get(WUXING[g], 0) + 1
    missing = [e for e in WUXING_ORDER if not wuxing_count.get(e)]
    return {
        "pillars": pillars,
        "day_master": day_stem,
        "day_master_element": _element(day_stem),
        "gender": spec["gender"],
        "zodiac": spec.get("zodiac"),
        "wuxing_count": wuxing_count,
        "wuxing_missing": missing,
        "dayun": dayun,
        "yun_forward": forward,
    }
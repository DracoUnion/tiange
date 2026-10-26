"""占卜排盘算法：六爻 / 梅花易数 / 小六壬 / 奇门遁甲 / 大六壬。"""
from __future__ import annotations

import random

from . import lunisolar as L

# 八卦（三爻，自下而上，阳=1 阴=0）
TRIGRAM_BITS = {
    "乾": (1, 1, 1), "兑": (1, 1, 0), "离": (1, 0, 1), "震": (1, 0, 0),
    "巽": (0, 1, 1), "坎": (0, 1, 0), "艮": (0, 0, 1), "坤": (0, 0, 0),
}
TRIGRAM_ATTR = {
    "乾": {"nature": "天", "element": "金", "symbol": "健"},
    "兑": {"nature": "泽", "element": "金", "symbol": "悦"},
    "离": {"nature": "火", "element": "火", "symbol": "丽"},
    "震": {"nature": "雷", "element": "木", "symbol": "动"},
    "巽": {"nature": "风", "element": "木", "symbol": "入"},
    "坎": {"nature": "水", "element": "水", "symbol": "陷"},
    "艮": {"nature": "山", "element": "土", "symbol": "止"},
    "坤": {"nature": "地", "element": "土", "symbol": "顺"},
}

# 小六壬六宫（掌诀）
LIUREN_LIUGONG = ["大安", "留连", "速喜", "赤口", "小吉", "空亡"]
LIUREN_TEXT = {
    "大安": "身不动时，事事昌盛，出行谋事顺遂，失物可寻，行人平安。属木，主安泰。",
    "留连": "卒未归时，久劳之事，事多反复，求财不利，官事拖延，病者宜缓。属水，主迟滞。",
    "速喜": "人便至时，喜事临门，出行得利，求财皆遂，行人立至。属火，主快速。",
    "赤口": "官事凶时，口舌是非，出行不利，求财无得，官事有伤。属金，主口舌。",
    "小吉": "人来喜时，凡事和合，出行顺利，求财遂心，行人有信。属木，主吉庆。",
    "空亡": "音信稀时，谋事无成，求财无利，行人有阻，病者难愈。属土，主虚无。",
}


def _trigram_bits(name: str) -> tuple:
    return TRIGRAM_BITS[name]


def trigram_name(bits: tuple) -> str:
    for k, v in TRIGRAM_BITS.items():
        if v == bits:
            return k
    return "坤"


# ---------------- 六爻 ----------------
def liuyao(lines: list[dict]) -> dict:
    """lines: [{value:6/7/8/9, moving:bool, yang:bool}...] 自下而上。匹配 64 卦。"""
    lower_bits = tuple(l["yang"] for l in lines[:3])
    upper_bits = tuple(l["yang"] for l in lines[3:6])
    lower = trigram_name(lower_bits)
    upper = trigram_name(upper_bits)
    moving = [i for i, l in enumerate(lines) if l["moving"]]
    gua_name = upper + lower
    return {
        "lines": [{"pos": f"{'初' if i == 0 else '二' if i == 1 else '三' if i == 2 else '四' if i == 3 else '五' if i == 4 else '上'}爻",
                   "value": l["value"], "yang": l["yang"], "moving": l["moving"]} for i, l in enumerate(lines)],
        "gua": gua_name, "lower": lower, "upper": upper,
        "moving_yao": [f"第{i + 1}爻" for i in moving],
    }


def _toss_coin_line(rng: random.Random) -> dict:
    """三枚铜钱：3阳=老阳9(动)，2阳1阴=少阴8，1阳2阴=少阳7，3阴=老阴6(动)。"""
    coins = [rng.choice([1, 0]) for _ in range(3)]
    yang = sum(coins)
    if yang == 3:
        return {"value": 9, "yang": True, "moving": True}
    if yang == 0:
        return {"value": 6, "yang": False, "moving": True}
    return {"value": 7 if yang == 2 else 8, "yang": yang >= 2, "moving": False}


def liuyao_method(method: str, seed: int | None = None) -> dict:
    rng = random.Random(seed)
    lines = [_toss_coin_line(rng) for _ in range(6)]
    return liuyao(lines)


# ---------------- 梅花易数 ----------------
def meihua_baogua(numbers: list[int]) -> dict:
    """以两组数定上下卦，数之和取动爻。"""
    if len(numbers) < 2:
        numbers = [random.randint(1, 9), random.randint(1, 9)]
    n_upper, n_lower = numbers[0], numbers[1]
    upper = trigram_name(tuple((int(n_upper)) & 1 for _ in range(3)))
    # 用数对 8 取余定卦（先天八卦序：乾1兑2离3震4巽5坎6艮7坤8）
    seq = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]
    upper = seq[(n_upper - 1) % 8]
    lower = seq[(n_lower - 1) % 8]
    moving = ((n_upper + n_lower) % 6) + 1  # 1..6
    ben = upper + lower
    # 变卦：动爻翻转
    bits = list(TRIGRAM_BITS[lower] + TRIGRAM_BITS[upper])
    bits[moving - 1] = 0 if bits[moving - 1] else 1
    bian_lower = trigram_name(tuple(bits[:3]))
    bian_upper = trigram_name(tuple(bits[3:]))
    return {
        "upper": upper, "lower": lower, "moving_yao": moving, "ben_gua": ben,
        "bian_gua": bian_upper + bian_lower,
        "upper_attr": TRIGRAM_ATTR[upper], "lower_attr": TRIGRAM_ATTR[lower],
    }


def meihua_method(method: str, params: dict) -> dict:
    if method == "shuzi" and params.get("numbers"):
        return meihua_baogua(params["numbers"])
    seed = int(params.get("seed") or 1)
    rng = random.Random(seed)
    return meihua_baogua([rng.randint(1, 9), rng.randint(1, 9)])


# ---------------- 小六壬 ----------------
def xiaoliuren(year: int, month: int, day: int, hour: int) -> dict:
    """月日时（农历）起课：月->宫，日->宫，时->宫。"""
    rng = random.Random(year * 10000 + month * 100 + day)
    # 以农历月(1..12)为起点偏移，日/时再偏移
    idx = 0
    idx = (idx + month - 1) % 6
    idx = (idx + day - 1) % 6
    idx = (idx + ((hour + 1) // 2)) % 6
    gong = LIUREN_LIUGONG[idx]
    return {"gong": gong, "index": idx, "text": LIUREN_TEXT[gong],
            "method": "月日时"}


# ---------------- 奇门遁甲（简化九宫局） ----------------
def qimen_pan(year: int, month: int, day: int, hour: int) -> dict:
    """生成简化九宫奇门局。"""
    # 九宫 1坎2坤3震4巽5中6乾7兑8艮9离
    palace_names = {1: "坎", 2: "坤", 3: "震", 4: "巽", 5: "中", 6: "乾", 7: "兑", 8: "艮", 9: "离"}
    base = L.day_ganzhi_idx(year, month, day) % 9
    rng = random.Random(day * 13 + hour)
    pan = []
    for p in range(1, 10):
        value = (base + p - 1) % 9 + 1
        star = ["天蓬", "天芮", "天冲", "天辅", "天禽", "天心", "天柱", "天任", "天英"][(value - 1)]
        door = ["休门", "死门", "伤门", "杜门", "中门", "开门", "惊门", "生门", "景门"][(value - 1)]
        pan.append({"palace": palace_names[p], "number": p, "value": value,
                    "star": star, "door": door})
    return {"pan": pan, "director": star_from_rng(rng), "day_ganzhi": L.ganzhi_name(L.day_ganzhi_idx(year, month, day))}


def star_from_rng(rng) -> str:
    return rng.choice(["天蓬", "天芮", "天冲", "天辅", "天禽", "天心", "天柱", "天任", "天英"])


# ---------------- 大六壬（简化四课三传） ----------------
def daliuren(year: int, month: int, day: int, hour: int) -> dict:
    rng = random.Random(day * 100 + hour)
    day_gz = L.ganzhi_name(L.day_ganzhi_idx(year, month, day))
    hour_gz = L.ganzhi_name(L.hour_ganzhi_idx(year, month, day, hour))
    fys = ["贵人", "螣蛇", "朱雀", "六合", "勾陈", "青龙", "天空", "白虎", "太常", "玄武", "太阴", "天后"]
    chuan = rng.sample(fys, 3)
    return {
        "day_gz": day_gz, "hour_gz": hour_gz,
        "ke": [{"pos": "一课", "value": day_gz}, {"pos": "二课", "value": hour_gz},
               {"pos": "三课", "value": L.ganzhi_name(L.ganzhi_from_sb(0, (day_gz[1] and L.EARTHLY.index(day_gz[1]) + 1) % 12))},
               {"pos": "四课", "value": hour_gz}],
        "chuan": chuan,
    }
"""签卦服务：64卦 / 观音灵签 / 诸葛神算。"""
from __future__ import annotations

import random
import time

from . import qian_data as Q


def draw_64gua(things: str = "") -> dict:
    gua = random.choice(Q.GUA_DATA)
    img = f"https://static.k366.com/d/file/gua/2013-07-27/{hash(gua['name'])%999999999}.gif"
    lines = "\n".join(f"【{y['pos']}】{y['text']} {y['interpret']}" for y in gua["yao"])
    return {
        "name": gua["name"],
        "full": gua["full"],
        "order": str(gua["order"]),
        "guxing": gua["guxing"],
        "guaci": gua["guaci"],
        "xiang": gua["xiang"],
        "baihua": gua["baihua"],
        "yaoci": f"【{gua['name']}卦】\n{gua['guaci']}\n\n象曰：{gua['xiang']}\n\n【爻辞】\n{lines}",
        "jiexi": f"【{gua['name']}】\n\n{gua['baihua']}\n\n{gua['summary']}",
        "imgURL": img,
        "things": things,
    }


def draw_guanyin(things: str = "") -> dict:
    qian = random.choice(Q.GUANYIN_LINGQIAN)
    return {
        "no": qian["no"], "qian": qian["qian"], "title": qian["title"],
        "text": qian["text"], "interpret": qian["interpret"], "things": things,
    }


def draw_zhuge(things: str = "") -> dict:
    qian = random.choice(Q.ZHUGU)
    return {
        "no": qian["no"], "text": qian["text"], "interpret": qian["interpret"], "things": things,
    }


def resolve_gua_item(order: int) -> dict | None:
    return Q.get_gua(order=order)


def resolve_guanyin_item(no: int) -> dict | None:
    return next((q for q in Q.GUANYIN_LINGQIAN if q["no"] == no), None)


def resolve_zhuge_item(no: int) -> dict | None:
    return next((q for q in Q.ZHUGU if q["no"] == no), None)


def resolve_by_type(qtype: str, item_id: str) -> dict | None:
    m = {
        "64gua": resolve_gua_item, "guanyin": resolve_guanyin_item, "zhuge": resolve_zhuge_item,
        "liuyao": resolve_gua_item, "meihua": resolve_gua_item,
    }
    fn = m.get(qtype)
    return fn(int(item_id)) if fn else None


def find_any_gua(name: str) -> dict | None:
    """按卦名（短名/全名/上下卦组合）查找。"""
    if not name:
        return None
    n = name.replace("闰", "")
    for g in Q.GUA_DATA:
        if g["name"] == n or g["full"] == n:
            return g
        if g["lower"] + g["upper"] == n:
            return g
    return None


find_gua_by_name = find_any_gua
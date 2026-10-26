"""运势生成：今日/本周/本月/今年/大运/一生。基于八字五行 + 日期确定性种子。"""
from __future__ import annotations

import datetime as dt
import random

from . import bazi, lunisolar as L

LUCK_LEVELS = ["大吉", "中吉", "小吉", "平", "小凶", "中凶"]
LUCKY_COLORS = ["朱红", "金黄", "翠绿", "天青", "藏蓝", "淡紫", "暖橙", "米白", "玄黑", "绛紫"]


def _seed(uid_or_member: str, target: str) -> int:
    h = 0
    for ch in str(uid_or_member) + target:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return h


def _score_to_luck(score: float) -> str:
    if score >= 0.85:
        return "大吉"
    if score >= 0.7:
        return "中吉"
    if score >= 0.55:
        return "小吉"
    if score >= 0.45:
        return "平"
    if score >= 0.3:
        return "小凶"
    return "中凶"


def generate(kind: str, member: dict, target_date: str) -> dict:
    """kind: today/week/month/year/dayun/onelife。member 含姓名/生日/性别。"""
    rng = random.Random(_seed(member.get("name", "unknown"), target_date))
    # 缺失五行影响运势
    missing = member.get("wuxing_missing") or []
    base = 0.62
    # 与当日干支的相合相克简估
    y, m, d = map(int, target_date.split("-"))
    day_gz = L.ganzhi_name(L.day_ganzhi_idx(y, m, d))
    if member.get("day_master"):
        ds = member["day_master"]
        # 日主五行与当日天干五行相同则增益
        if bazi.WUXING.get(ds) == bazi.WUXING.get(day_gz[0]):
            base += 0.10
    score = max(0.15, min(0.98, base + rng.uniform(-0.18, 0.18)))

    cats = {
        "感情": round(score + rng.uniform(-0.1, 0.1), 2),
        "事业": round(score + rng.uniform(-0.12, 0.1), 2),
        "财运": round(score + rng.uniform(-0.1, 0.12), 2),
        "健康": round(score + rng.uniform(-0.12, 0.08), 2),
        "学业": round(score + rng.uniform(-0.08, 0.1), 2),
    }
    yi = rng.sample(["宜出行", "宜会友", "宜求财", "宜修身", "宜签约", "宜安床", "宜祭祀", "宜纳财"], 3)
    ji = rng.sample(["忌争执", "忌急躁", "忌远行", "忌冲动消费", "忌熬夜", "忌轻信", "忌冒险", "忌口舌"], 3)
    direction = rng.choice(["正东", "正南", "正西", "正北", "东南", "西南", "东北", "西北"])
    return {
        "type": kind,
        "date": target_date,
        "luck": _score_to_luck(score),
        "score": round(score * 100, 1),
        "categories": cats,
        "yi": yi, "ji": ji,
        "color": rng.choice(LUCKY_COLORS),
        "direction": direction,
        "summary": _summary(kind, member.get("name", ""), score),
        "day_ganzhi": day_gz,
        "missing_wuxing": missing,
    }


def _summary(kind: str, name: str, score: float) -> str:
    who = name or "你"
    if kind == "today":
        return f"{who}今日气运{'通畅' if score > 0.6 else '平淡'}，宜{('顺势而为' if score > 0.6 else '稳中求进')}，把握当下。"
    if kind == "thisWeek":
        return f"{who}本周整体运势{'稳中有升' if score > 0.6 else '平稳'}，宜提前规划，留意人际合作。"
    if kind == "thisMonth":
        return f"{who}本月气运{'渐旺' if score > 0.6 else '待养'}，宜深耕专业，蓄势待发。"
    if kind == "thisYear":
        return f"{who}今年运势{'昂扬向上' if score > 0.6 else '需循序渐进'}，把握主线，行稳致远。"
    if kind == "dayun":
        return f"{who}此大运十年，{('财官两旺' if score > 0.6 else '宜守正蓄力')}，为人生关键阶段。"
    return f"{who}一生运势起伏有致，{'贵人多助、晚景可期' if score > 0.6 else '宜厚积薄发、守正持恒'}。"


def member_to_fortune_input(member) -> dict:
    """把 Member 模型转为运势所需字典（含八字 spec）。"""
    spec = L.member_spec_from_params(member.calendar, member.birth_year, member.birth_month,
                                     member.birth_day, member.birth_hour, member.gender)
    b = bazi.compute(spec)
    return {
        "name": member.name,
        "gender": member.gender,
        "day_master": b["day_master"],
        "wuxing_missing": b["wuxing_missing"],
        "zodiac": spec["zodiac"],
        "member_id": member.id,
    }
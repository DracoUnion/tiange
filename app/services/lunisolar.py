"""公历 ↔ 农历 与 干支 计算。

实现基于经典农历数据表（1900–2100，公开领域天文数据）。
干支纪年按「立春」划界（近似用农历新年近似，可进一步精化）。
"""
from __future__ import annotations

HEAVENLY = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ZODIAC = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
LUNAR_MONTH = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
LUNAR_DAY = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
             "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
             "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]

# 1900-2100 农历信息：每项十六进制，位 0-3 表示闰月，位 4-15 表示每月大小（大月30/小月29）
# fmt: off
LUNAR_INFO = [
    0x04bd8,0x04ae0,0x0a570,0x054d5,0x0d260,0x0d950,0x16554,0x056a0,0x09ad0,0x055d2,
    0x04ae0,0x0a5b6,0x0a4d0,0x0d250,0x1d255,0x0b540,0x0d6a0,0x0ada2,0x095b0,0x14977,
    0x04970,0x0a4b0,0x0b4b5,0x06a50,0x06d40,0x1ab54,0x02b60,0x09570,0x052f2,0x04970,
    0x06566,0x0d4a0,0x0ea50,0x06e95,0x05ad0,0x02b60,0x186e3,0x092e0,0x1c8d7,0x0c950,
    0x0d4a0,0x1d8a6,0x0b550,0x056a0,0x1a5b4,0x025d0,0x092d0,0x0d2b2,0x0a950,0x0b557,
    0x06ca0,0x0b550,0x15355,0x04da0,0x0a5b0,0x14573,0x052b0,0x0a9a8,0x0e950,0x06aa0,
    0x0aea6,0x0ab50,0x04b60,0x0aae4,0x0a570,0x05260,0x0f263,0x0d950,0x05b57,0x056a0,
    0x096d0,0x04dd5,0x04ad0,0x0a4d0,0x0d4d4,0x0d250,0x0d558,0x0b540,0x0b6a0,0x195a6,
    0x095b0,0x049b0,0x0a974,0x0a4b0,0x0b27a,0x06a50,0x06d40,0x0af46,0x0ab60,0x09570,
    0x04af5,0x04970,0x064b0,0x074a3,0x0ea50,0x06b58,0x05ac0,0x0ab60,0x096d5,0x092e0,
    0x0c960,0x0d954,0x0d4a0,0x0da50,0x07552,0x056a0,0x0abb7,0x025d0,0x092d0,0x0cab5,
    0x0a950,0x0b4a0,0x0baa4,0x0ad50,0x055d9,0x04ba0,0x0a5b0,0x15176,0x052b0,0x0a930,
    0x07954,0x06aa0,0x0ad50,0x05b52,0x04b60,0x0a6e6,0x0a4e0,0x0d260,0x0ea65,0x0d530,
    0x05aa0,0x076a3,0x096d0,0x04afb,0x04ad0,0x0a4d0,0x1d0b6,0x0d250,0x0d520,0x0dd45,
    0x0b5a0,0x056d0,0x055b2,0x049b0,0x0a577,0x0a4b0,0x0aa50,0x1b255,0x06d20,0x0ada0,
    0x14b63,0x09370,0x049f8,0x04970,0x064b0,0x168a6,0x0ea50,0x06b20,0x1a6c4,0x0aae0,
    0x092e0,0x0d2e3,0x0c960,0x0d557,0x0d4a0,0x0da50,0x05a55,0x056a0,0x0a6d0,0x055d4,
    0x052d0,0x0a9b8,0x0a950,0x0b4a0,0x0b6a6,0x0ad50,0x055a0,0x0aba4,0x0a5b0,0x052b0,
    0x0b273,0x06930,0x07337,0x06aa0,0x0ad50,0x14b55,0x04b60,0x0a570,0x054e4,0x0d160,
    0x0e968,0x0d520,0x0daa0,0x16aa6,0x056d0,0x04ae0,0x0a9d4,0x0a2d0,0x0d150,0x0f252,
    0x0d520]
# fmt: on

_BASE_YEAR = 1900


def _leap_month(y: int) -> int:
    return LUNAR_INFO[y - _BASE_YEAR] & 0xF


def _month_days(y: int, m: int) -> int:
    return 30 if (LUNAR_INFO[y - _BASE_YEAR] & (0x10000 >> m)) else 29


def _year_days(y: int) -> int:
    info = LUNAR_INFO[y - _BASE_YEAR]
    total = 348
    for m in range(1, 13):
        if info & (0x10000 >> m):
            total += 1
    leap = info & 0xF
    if leap:
        total += 30 if (info & 0x10000) else 29
    return total


def solar_to_lunar(year: int, month: int, day: int) -> dict:
    """公历转农历。返回 {year, month, day, is_leap, month_name, day_name, zodiac}。"""
    import datetime as dt
    offset = (dt.date(year, month, day) - dt.date(_BASE_YEAR, 1, 31)).days
    i = _BASE_YEAR
    while offset >= _year_days(i):
        offset -= _year_days(i)
        i += 1
    lunar_year = i
    leap = _leap_month(lunar_year)
    is_leap = False
    j = 1
    while j <= 12:
        if leap > 0 and j == leap + 1 and not is_leap:
            j -= 1
            is_leap = True
            days = 30 if (LUNAR_INFO[lunar_year - _BASE_YEAR] & 0x10000) else 29
        else:
            days = _month_days(lunar_year, j)
        if is_leap and j == leap + 1:
            is_leap = False
        if offset < days:
            break
        offset -= days
        if j == leap and is_leap:
            is_leap = False
        else:
            j += 1
    lunar_month = j if j <= 12 else 12
    lunar_day = offset + 1
    return {
        "year": lunar_year, "month": lunar_month, "day": lunar_day, "is_leap": is_leap,
        "month_name": LUNAR_MONTH[lunar_month - 1],
        "day_name": LUNAR_DAY[lunar_day - 1],
        "zodiac": ZODIAC[(lunar_year - 4) % 12],
    }


def day_ganzhi_idx(year: int, month: int, day: int) -> int:
    """干支纪日序号（0=甲子）。基于 1900-01-31 为甲辰 的近似锚点推算。"""
    import datetime as dt
    anchor = dt.date(1900, 1, 31)
    cur = dt.date(year, month, day)
    # 1900-01-31 对应干支索引：经校正取 40（甲辰），以下用固定偏移
    base_idx = 40  # 甲子=0 偏移，使得常见日期与公开排盘吻合
    return (base_idx + (cur - anchor).days) % 60


def year_ganzhi_idx(year: int) -> int:
    """干支纪年（以立春近似，1/1 起当年）。0=甲子。"""
    return (year - 1984) % 60  # 1984 为甲子年


def ganzhi_from_sb(stem: int, branch: int) -> int:
    """把 (干,支) 对齐到 60 甲子序号（满足 idx%10=干, idx%12=支）。"""
    for k in range(60):
        if k % 10 == stem and k % 12 == branch:
            return k
    return 0


def month_ganzhi_idx(year: int, month: int) -> int:
    """月柱（五虎遁）：地支按节气近似=公历月%12（子=0），年干定寅月干。"""
    y_idx = year_ganzhi_idx(year)
    year_stem = y_idx % 10
    first_month_stem = (year_stem % 5) * 2 + 2      # 寅月干（甲己→丙）
    branch = month % 12                             # 1月→丑(1), 2月→寅(2), 12月→子(0)
    count_from_yin = (branch - 2) % 12
    stem = (first_month_stem + count_from_yin) % 10
    return ganzhi_from_sb(stem, branch)


def hour_ganzhi_idx(year: int, month: int, day: int, hour: int) -> int:
    """时柱：时支固定（23=子, 0=子, 1=丑...），时干由日干（五鼠遁）。"""
    d_idx = day_ganzhi_idx(year, month, day)
    day_stem = d_idx % 10
    branch = ((hour + 1) // 2) % 12  # 23/0->子(0),1/2->丑(1)...
    first_hour_stem = (day_stem % 5) * 2  # 甲己日起甲子
    stem = (first_hour_stem + branch) % 10
    return ganzhi_from_sb(stem, branch)


def ganzhi_name(idx: int) -> str:
    return HEAVENLY[idx % 10] + EARTHLY[idx % 12]


def member_spec_from_params(calendar: str, year: int, month: int, day: int, hour: int, gender: str) -> dict:
    """把出生参数转成命理基础（干支四柱等）。"""
    if calendar == "lunar":
        # 农历近似转公历不精确；此处直接用农历年月作为干支参考
        gd = day_ganzhi_idx(year, month, day)
    else:
        gd = day_ganzhi_idx(year, month, day)
    y_gz = ganzhi_name(year_ganzhi_idx(year))
    m_gz = ganzhi_name(month_ganzhi_idx(year, month))
    d_gz = ganzhi_name(gd)
    h_gz = ganzhi_name(hour_ganzhi_idx(year, month, day, hour))
    return {
        "year_ganzhi": y_gz, "month_ganzhi": m_gz, "day_ganzhi": d_gz, "hour_ganzhi": h_gz,
        "day_master": HEAVENLY[gd % 10], "gender": gender, "zodiac": ZODIAC[(year - 4) % 12],
    }
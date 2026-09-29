"""图形验证码（Pillow 生成 + 内存态存储）。"""
from __future__ import annotations

import io
import random
import string
import time
import uuid

from PIL import Image, ImageDraw, ImageFont

# 验证码有效期（秒）
_CAPTCHA_TTL = 300
_store: dict[str, tuple[str, float]] = {}

_CHARS = string.digits + string.ascii_uppercase


def _get_font(size: int):
    """尝试加载系统中文字体，失败则用默认。"""
    for path in [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _cleanup():
    now = time.time()
    expired = [k for k, v in _store.items() if now - v[1] > _CAPTCHA_TTL]
    for k in expired:
        _store.pop(k, None)


def create_captcha() -> dict:
    """生成验证码，返回 {b64s, id}。"""
    _cleanup()
    code = "".join(random.choices(_CHARS, k=4))
    captcha_id = uuid.uuid4().hex
    _store[captcha_id] = (code, time.time())

    w, h = 150, 48
    img = Image.new("RGB", (w, h), (43, 43, 43))
    draw = ImageDraw.Draw(img)
    font = _get_font(30)

    # 噪点与干扰线
    for _ in range(220):
        draw.point((random.randint(0, w - 1), random.randint(0, h - 1)), fill=(120, 120, 120))
    for _ in range(4):
        draw.line(
            [
                (random.randint(0, w), random.randint(0, h)),
                (random.randint(0, w), random.randint(0, h)),
            ],
            fill=(80, 80, 80),
            width=1,
        )

    x = 12
    for ch in code:
        draw.text((x, 8), ch, font=font, fill=(230, 214, 173))
        x += 32

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    import base64
    return {"b64s": base64.b64encode(buf.getvalue()).decode(), "id": captcha_id}


def verify_captcha(captcha_id: str, answer: str) -> bool:
    _cleanup()
    rec = _store.pop(captcha_id, None)
    if not rec:
        return False
    code, _ts = rec
    return code.lower() == (answer or "").strip().lower()

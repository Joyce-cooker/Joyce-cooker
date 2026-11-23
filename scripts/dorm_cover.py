# -*- coding: utf-8 -*-
"""Cover for dorm_stick_starry_narration.mp4 — night-dorm, warm-on-cool poster."""
import os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC = os.path.join(BASE, "assets", "source-frame.jpg")
OUT = os.path.join(BASE, "out")
os.makedirs(OUT, exist_ok=True)
NOTO = os.environ.get("COVER_FONT", r"C:\Windows\Fonts\NotoSansSC-VF.ttf")

CREAM = (246, 239, 226)
AMBER = (255, 182, 92)
INK   = (10, 14, 24)

_fc = {}
def F(size, weight="Black"):
    key = (int(size), weight)
    if key not in _fc:
        f = ImageFont.truetype(NOTO, int(size))
        try: f.set_variation_by_name(weight)
        except Exception: pass
        _fc[key] = f
    return _fc[key]

def tw(s, f):
    b = f.getbbox(s)
    return b[2] - b[0]

def fit(text, target_w, lo=40, hi=260):
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if tw(text, F(mid, "Black")) <= target_w: lo = mid
        else: hi = mid - 1
    return lo

# ------------------------------------------------------------------ source prep
def load_room(size=(1080, 1440)):
    im = Image.open(SRC).convert("RGB")
    if size[1] == 1440:                      # 3:4 crop
        im = im.crop((0, 300, 1080, 1740))
    else:                                    # 9:16, paint out the burned-in caption
        a = np.asarray(im).astype(np.float32)
        x0, y0, x1, y1 = 292, 86, 775, 242
        for y in range(y0, y1):
            left = a[y, 0:280].mean(axis=0)
            right = a[y, 800:1050].mean(axis=0)
            w = np.linspace(0, 1, x1 - x0)[:, None]
            a[y, x0:x1] = left * (1 - w) + right * w
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return im.resize(size, Image.LANCZOS)

def grade(im, mult=0.72, vign=0.70):
    W, H = im.size
    a = np.asarray(im).astype(np.float32) / 255.0
    a = a ** 1.04 * mult                                  # crush to night
    a += np.array([0.010, 0.018, 0.038], np.float32)      # cool lift
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W * .72)) ** 2 + ((yy - H * .58) / (H * .80)) ** 2)
    a *= np.clip(1 - np.clip(d - .25, 0, 2) ** 1.4 * vign, 0, 1)[:, :, None]
    return Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)).convert("RGBA")

def blur_band(im, y_from, y_to, radius=5):
    """tilt-shift: soften the top so type sits on a quiet field"""
    W, H = im.size
    soft = im.filter(ImageFilter.GaussianBlur(radius))
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for i in range(y_to - y_from):
        d.line([(0, y_from + i), (W, y_from + i)], fill=int(255 * (1 - i / (y_to - y_from)) ** 1.2))
    mask.paste(255, (0, 0, W, y_from))
    return Image.composite(soft, im, mask)

def scrim(im, center, radius, strength=0.70, color=INK):
    """soft radial darkening so the type block sits on a quiet field"""
    W, H = im.size
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((xx - center[0]) ** 2 + (yy - center[1]) ** 2) / radius
    a = np.clip(1 - d, 0, 1) ** 1.25 * strength
    dark = Image.new("RGBA", (W, H), color + (255,))
    dark.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    return Image.alpha_composite(im, dark)

def sound_rings(im, cx, cy, radii, color=AMBER, start=126, end=234):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # warm spill around the phone itself
    d.ellipse([cx - 118, cy - 118, cx + 118, cy + 118], fill=color + (46,))
    lay = lay.filter(ImageFilter.GaussianBlur(34))
    im = Image.alpha_composite(im, lay)
    lay2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d2 = ImageDraw.Draw(lay2)
    for r, al, w in radii:
        d2.arc([cx - r, cy - r, cx + r, cy + r], start, end, fill=color + (al,), width=w)
    glow = lay2.filter(ImageFilter.GaussianBlur(9))
    return Image.alpha_composite(Image.alpha_composite(im, glow), lay2)

def grain(im, amount=3.0, alpha=10):
    W, H = im.size
    rng = np.random.default_rng(3)
    n = rng.normal(0, amount, (H, W, 1)).repeat(3, axis=2)
    a = np.asarray(im.convert("RGB")).astype(np.float32) + n
    lay = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    lay.putalpha(alpha)
    return Image.alpha_composite(im, lay)

# ------------------------------------------------------------------ type block
def vgrad(im, y_from, y_to, a0, a1, color=INK):
    """vertical dark gradient; a0 at y_from -> a1 at y_to"""
    W, H = im.size
    lay = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(lay)
    for y in range(max(0, y_from), min(H, y_to)):
        t = (y - y_from) / max(1, (y_to - y_from))
        d.line([(0, y), (W, y)], fill=int(255 * (a0 + (a1 - a0) * t)))
    dark = Image.new("RGBA", (W, H), color + (255,))
    dark.putalpha(lay)
    return Image.alpha_composite(im, dark)

def type_block(im, s, line1, line2, accent=AMBER, y=None, anchor_x=100, eyebrow="熄灯之后 · 01"):
    """s = scale (1.0 for 1080 wide)"""
    W, H = im.size
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x = anchor_x
    xx = x
    for ch in eyebrow:
        d.text((xx, y), ch, font=F(34 * s, "Medium"), fill=CREAM + (145,), anchor="ls")
        xx += tw(ch, F(34 * s, "Medium")) + 10 * s
    d.text((x, y + 244 * s), line1, font=F(min(142, fit(line1, 760)) * s, "Black"),
           fill=CREAM + (255,), anchor="ls")
    d.text((x, y + 480 * s), line2, font=F(min(192, fit(line2, 700)) * s, "Black"),
           fill=accent + (255,), anchor="ls")
    return Image.alpha_composite(im, lay)

# ------------------------------------------------------------------ assemble
def make(size, line1, line2, out, accent=AMBER, eyebrow="熄灯之后 · 01"):
    s = size[0] / 1080
    room = load_room(size)
    im = grade(room, mult=0.74 if size[1] == 1440 else 0.72)
    im = blur_band(im, 0, int(size[1] * 0.46), radius=4.5 * s)
    im = vgrad(im, 0, int((820 if size[1] == 1440 else 980) * s), 0.74, 0.04)
    im = vgrad(im, int(size[1] - 300 * s), size[1], 0.0, 0.55)
    cx = int(807 * s)
    cy = int(737 * s) if size[1] == 1440 else int(987 * s)
    im = sound_rings(im, cx, cy, [(62 * s, 165, int(6 * s)), (100 * s, 118, int(6 * s)), (140 * s, 70, int(6 * s))])
    im = scrim(im, (320 * s, 380 * s), 820 * s, strength=0.55)
    im = type_block(im, s, line1, line2, accent, y=228 * s, eyebrow=eyebrow)
    im = grain(im)
    im.convert("RGB").save(out, quality=96)
    return im

if __name__ == "__main__":
    make((1080, 1440), "调到最小", "还是吵", os.path.join(OUT, "case-3x4.png"))
    make((1080, 1440), "说一句", "会得罪人", os.path.join(OUT, "case-3x4-b.png"))
    make((1080, 1440), "熄灯之后", "还在响", os.path.join(OUT, "case-3x4-c.png"), eyebrow="宿舍 · 01")
    make((1080, 1920), "调到最小", "还是吵", os.path.join(OUT, "case-9x16.png"))
    print("ok")

# -*- coding: utf-8 -*-
"""4:3 landscape (1440x1080) — band layout: title band on top, room band below."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from dorm_cover import F, tw, fit, grade, grain, sound_rings, CREAM, AMBER, INK

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "assets", "source-frame.jpg")
OUT = os.path.join(BASE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 1440, 1080
BAND = 372
TOP_PAD = 40

def build(s1="调到最小，", s2="还是吵", eyebrow="熄灯之后 · 01", out="case-4x3.png"):
    band_h = H - BAND
    room = Image.open(SRC).convert("RGB").crop((0, 840, 1080, 1402)).resize((W, band_h), Image.LANCZOS)
    room = grade(room, mult=0.82, vign=0.52)

    a = np.zeros((H, W, 3), np.float32)
    ramp = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    a[:] = np.array([14, 17, 28], np.float32) * (1 - ramp) + np.array([8, 9, 16], np.float32) * ramp
    canvas = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    canvas.alpha_composite(room, (0, BAND))

    # 接缝：画面顶边融进黑带
    seam = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(seam)
    for i in range(170):
        d.line([(0, BAND + i), (W, BAND + i)], fill=int(255 * (1 - i / 170) ** 1.5))
    dark = Image.new("RGBA", (W, H), (8, 9, 16, 255))
    dark.putalpha(seam)
    canvas = Image.alpha_composite(canvas, dark)
    # 再压一层从顶部往下的柔光，弱化硬边
    canvas = canvas.filter(ImageFilter.GaussianBlur(0))

    cx = int(807 / 1080 * W)
    cy = int(BAND + (1005 - 840) / 562 * band_h)
    canvas = sound_rings(canvas, cx, cy, [(86, 155, 8), (140, 112, 8), (196, 66, 8)])

    size = min(146, fit(s1 + s2, 1240))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x = 96
    xx = x
    for ch in eyebrow:
        d.text((xx, TOP_PAD + 66), ch, font=F(32, "Medium"), fill=CREAM + (150,), anchor="ls")
        xx += tw(ch, F(32, "Medium")) + 10
    base = TOP_PAD + 250
    d.text((x, base), s1, font=F(size, "Black"), fill=CREAM + (255,), anchor="ls")
    d.text((x + tw(s1, F(size, "Black")), base), s2, font=F(size, "Black"), fill=AMBER + (255,), anchor="ls")
    canvas = Image.alpha_composite(canvas, lay)

    canvas = grain(canvas)
    canvas.convert("RGB").save(os.path.join(OUT, out), quality=96)
    return canvas

if __name__ == "__main__":
    build(out="case-4x3.png")
    build("说一句，", "会得罪人", out="case-4x3-b.png")
    print("ok")

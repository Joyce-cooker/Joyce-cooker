# -*- coding: utf-8 -*-
"""原帧 → 成品：案例的前后对比图。

输入：assets/source-frame.jpg + out/case-3x4.png + out/case-4x3.png
输出：images/case-source-vs-result.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "assets", "source-frame.jpg")
OUT = os.path.join(BASE, "out")
IMG = os.path.join(BASE, "images")
NOTO = os.environ.get("COVER_FONT", r"C:\Windows\Fonts\NotoSansSC-VF.ttf")

CREAM = (247, 244, 237)
DIM = (176, 172, 186)
FAINT = (124, 120, 134)
AMBER = (255, 182, 92)
BG = (12, 13, 18)

_fc = {}
def F(size, weight="Black"):
    k = (int(size), weight)
    if k not in _fc:
        f = ImageFont.truetype(NOTO, int(size))
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
        _fc[k] = f
    return _fc[k]


def build():
    H = 900
    raw = Image.open(SRC).convert("RGB")
    raw = raw.resize((int(raw.width * H / raw.height), H), Image.LANCZOS)
    c34 = Image.open(os.path.join(OUT, "case-3x4.png")).convert("RGB")
    c34 = c34.resize((int(c34.width * H / c34.height), H), Image.LANCZOS)
    c43 = Image.open(os.path.join(OUT, "case-4x3.png")).convert("RGB")
    c43 = c43.resize((int(c43.width * H / c43.height), H), Image.LANCZOS)

    pad, gap, head = 64, 76, 252
    W = pad * 2 + raw.width + gap + c34.width
    Hh = head + H + 74
    sheet = Image.new("RGB", (W, Hh), BG)
    d = ImageDraw.Draw(sheet)

    d.rectangle([pad, 62, pad + 92, 68], fill=AMBER)
    d.text((pad, 86), "从一帧画面到一个封面", font=F(56, "Black"), fill=CREAM)
    d.text((pad, 152), "原片单机位、低对比，还烧着字幕；成品把亮度压到 0.74，只在手机位置留一个暖光源",
           font=F(25, "Medium"), fill=FAINT)

    sheet.paste(raw, (pad, head))
    x2 = pad + raw.width + gap
    sheet.paste(c34, (x2, head))
    for x, w in ((pad, raw.width), (x2, c34.width)):
        d.rectangle([x, head, x + w - 1, head + H - 1], outline=(255, 255, 255, 34), width=2)

    d.text((pad, head - 52), "原 帧", font=F(28, "Black"), fill=(146, 139, 160))
    d.text((x2, head - 52), "成 品（3:4）", font=F(28, "Black"), fill=AMBER)

    # 箭头
    ax, ay = pad + raw.width + 22, head + H // 2
    d.line([(ax, ay), (ax + 34, ay)], fill=AMBER, width=6)
    d.polygon([(ax + 48, ay), (ax + 28, ay - 12), (ax + 28, ay + 12)], fill=AMBER)

    sheet.save(os.path.join(IMG, "case-source-vs-result.png"))
    print("saved images/case-source-vs-result.png", sheet.size)


if __name__ == "__main__":
    build()

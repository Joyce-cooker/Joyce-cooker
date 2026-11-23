# -*- coding: utf-8 -*-
"""Preview sheet: three copy variants + feed-size check."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "out")
NOTO = os.environ.get("COVER_FONT", r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
WHITE = (247, 244, 237)
DIM = (176, 172, 186)
FAINT = (124, 120, 134)
AMBER = (255, 182, 92)
BG = (12, 13, 18)

_fc = {}
def F(size, weight="Black"):
    k = (int(size), weight)
    if k not in _fc:
        f = ImageFont.truetype(NOTO, int(size))
        try: f.set_variation_by_name(weight)
        except Exception: pass
        _fc[k] = f
    return _fc[k]

items = [
    ("case-3x4.png", "A｜事实悖论", "「调到最小」和「还是吵」互相打脸，最像视频本身"),
    ("case-3x4-b.png", "B｜困境代入", "说出了大家不好意思说的那句话，最容易引评论"),
    ("case-3x4-c.png", "C｜场景描述", "最稳，但钩子偏弱，适合做二选一"),
]

cw, ch = 560, 747
gap, pad = 44, 60
head = 250
SH = head + ch + 130 + 44 + 250 + 40
SW = pad * 2 + 3 * cw + 2 * gap
sheet = Image.new("RGB", (SW, SH), BG)
d = ImageDraw.Draw(sheet)

d.rectangle([pad, 74, pad + 96, 80], fill=AMBER)
d.text((pad, 100), "《熄灯之后》封面 · 3 个版本", font=F(58, "Black"), fill=WHITE)
d.text((pad, 178), "同一张画面、同一套字号与留白，只换那句钩子　|　1080×1440（3:4）",
       font=F(27, "Medium"), fill=FAINT)

for i, (fn, tag, desc) in enumerate(items):
    x = pad + i * (cw + gap)
    im = Image.open(os.path.join(OUT, fn)).convert("RGB").resize((cw, ch), Image.LANCZOS)
    sheet.paste(im, (x, head))
    d.rectangle([x, head, x + cw - 1, head + ch - 1], outline=(255, 255, 255, 30), width=2)
    d.text((x + 2, head + ch + 22), tag, font=F(30, "Black"), fill=AMBER)
    d.text((x + 2, head + ch + 62), desc, font=F(22, "Medium"), fill=DIM)

# feed-size row
fy = head + ch + 130
d.text((pad, fy), "信息流里的大小（150px 宽）+ 主页宫格大小（180px 宽）", font=F(24, "Bold"), fill=DIM)
for i, (fn, _, _) in enumerate(items):
    x = pad + i * 460
    im = Image.open(os.path.join(OUT, fn)).convert("RGB")
    sheet.paste(im.resize((148, 197), Image.LANCZOS), (x, fy + 44))
    sheet.paste(im.resize((180, 240), Image.LANCZOS), (x + 168, fy + 44))
sheet.save(os.path.join(OUT, "preview.png"))
print("ok")

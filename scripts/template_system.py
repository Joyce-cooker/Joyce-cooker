# -*- coding: utf-8 -*-
"""Douyin cover system v3 — type-led 3:4 covers, proper alpha, baseline grid."""
import os, math
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np

W, H = 1080, 1440
NOTO = os.environ.get("COVER_FONT", r"C:\Windows\Fonts\NotoSansSC-VF.ttf")  # 本机 Noto Sans SC 可变字体
OUT = os.path.join(BASE, "out")
os.makedirs(OUT, exist_ok=True)
M = 100

INK   = (11, 9, 18)
WHITE = (255, 255, 255)
DIM   = (186, 180, 200)
FAINT = (126, 118, 142)
GREY  = (74, 68, 88)
MAG   = (255, 46, 139)
GOLD  = (255, 198, 92)

_fc = {}
def F(size, weight="Black"):
    key = (int(size), weight)
    if key not in _fc:
        f = ImageFont.truetype(NOTO, int(size))
        try: f.set_variation_by_name(weight)
        except Exception: pass
        _fc[key] = f
    return _fc[key]

def tw(text, font):
    b = font.getbbox(text)
    return b[2] - b[0]

def fit_size(text, target_w, weight="Black", lo=10, hi=520):
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if tw(text, F(mid, weight)) <= target_w: lo = mid
        else: hi = mid - 1
    return lo

class Canvas:
    def __init__(self):
        self.img = Image.new("RGBA", (W, H), INK + (255,))
    def draw(self, fn):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fn(ImageDraw.Draw(lay))
        self.img.alpha_composite(lay)

def base(cv, gx=0.68, gy=0.60, gr=780, ga=70, vign=0.62):
    a = np.zeros((H, W, 3), dtype=np.float32)
    ramp = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    a[:] = np.array([10, 8, 16], np.float32) * (1 - ramp) + np.array([5, 4, 9], np.float32) * ramp
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt((xx - gx * W) ** 2 + (yy - gy * H) ** 2) / gr
    g = np.clip(1 - dist, 0, 1) ** 2 * (ga / 255.0)
    a += g[:, :, None] * np.array([255, 46, 139], np.float32)
    d2 = np.sqrt(((xx - W / 2) / (W * .85)) ** 2 + ((yy - H / 2) / (H * .85)) ** 2)
    a *= np.clip(1 - d2 ** 2 * vign, 0, 1)[:, :, None]
    cv.img.alpha_composite(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA"))

def eyebrow(cv, text, base_y=212, x=M, size=33, alpha=135, tracking=11, color=WHITE):
    def fn(d):
        xx = x
        for ch in text:
            d.text((xx, base_y), ch, font=F(size, "Medium"), fill=color + (alpha,), anchor="ls")
            xx += tw(ch, F(size, "Medium")) + tracking
    cv.draw(fn)

def rule(cv, y, x1=M, x2=W - M, alpha=30, h=2):
    cv.draw(lambda d: d.rectangle([x1, y, x2, y + h - 1], fill=WHITE + (alpha,)))

def marker(cv, x1, x2, y, thick=14, color=MAG, amp=4):
    def fn(d):
        pts = []
        n = 70
        for i in range(n + 1):
            t = i / n
            pts.append((x1 + (x2 - x1) * t, y + math.sin(t * math.pi * 1.6) * amp + math.sin(t * 8.5) * 1.4))
        d.line(pts, fill=color + (255,), width=thick, joint="curve")
    cv.draw(fn)

def note(cv, text, base_y=1262, size=42, alpha=185, color=FAINT):
    cv.draw(lambda d: d.text((M, base_y), text, font=F(size, "Medium"), fill=color + (alpha,), anchor="ls"))

# ------------------------------------------------------------------ 01 数字锚点
def cover_num4():
    cv = Canvas(); base(cv, 0.74, 0.52, 820, 74, 0.66)
    eyebrow(cv, "AGENT 底座 · 07")

    def t(d):
        d.text((M, 404), "装 Agent 之前", font=F(92, "Black"), fill=WHITE + (245,), anchor="ls")
        x = M
        d.text((x, 884), "先装这", font=F(118, "Black"), fill=WHITE + (255,), anchor="ls")
        x += tw("先装这", F(118, "Black")) + 52
        d.text((x, 884), "4", font=F(360, "Black"), fill=MAG + (255,), anchor="ls")
        x += tw("4", F(360, "Black")) + 34
        d.text((x, 884), "个", font=F(118, "Black"), fill=WHITE + (255,), anchor="ls")
    cv.draw(t)
    cv.draw(lambda d: d.text((M + 4, 1002), "少一个，Agent 都跑不顺",
                             font=F(50, "Medium"), fill=DIM + (235,), anchor="ls"))
    # 4 段刻度条
    def bars(d):
        for i in range(4):
            d.rounded_rectangle([M + i * 30, 1120, M + i * 30 + 14, 1120 + 70],
                                radius=7, fill=MAG + (255,))
        d.text((M + 148, 1173), "四件套", font=F(34, "Bold"), fill=FAINT + (235,), anchor="ls")
    cv.draw(bars)
    return cv

# ------------------------------------------------------------------ 02 对比
def cover_30to3():
    cv = Canvas(); base(cv, 0.48, 0.50, 900, 42, 0.66)
    eyebrow(cv, "SKILL 清单 · 12")

    def t(d):
        d.text((M, 640), "Skill 装得越多", font=F(66, "Bold"), fill=FAINT + (255,), anchor="ls")
        f30 = F(340, "Black")
        d.text((M, 960), "30", font=f30, fill=GREY + (255,), anchor="ls")
        bb = d.textbbox((M, 960), "30", font=f30, anchor="ls")
        cy = bb[1] + (bb[3] - bb[1]) * .54
        d.rounded_rectangle([bb[0] - 8, cy - 9, bb[2] + 8, cy + 9], radius=9, fill=MAG + (255,))
        ax1, ax2 = bb[2] + 76, bb[2] + 196
        d.rounded_rectangle([ax1, cy - 10, ax2 - 30, cy + 10], radius=10, fill=MAG + (255,))
        d.polygon([(ax2 + 4, cy), (ax2 - 34, cy - 32), (ax2 - 34, cy + 32)], fill=MAG + (255,))
        f3 = F(430, "Black")
        d.text((ax2 + 62, 960), "3", font=f3, fill=MAG + (255,), anchor="ls")
    cv.draw(t)
    cv.draw(lambda d: d.text((M, 1112), "留下来的，才真的天天用",
                             font=F(54, "Bold"), fill=DIM + (245,), anchor="ls"))
    rule(cv, 1232)
    note(cv, "多 ≠ 强，能用才算装", 1300, 40)
    return cv

# ------------------------------------------------------------------ 03 冲突
def cover_fight():
    cv = Canvas(); base(cv, 0.52, 0.26, 760, 84, 0.68)
    eyebrow(cv, "AI 团队 · 03")

    def heads(d):
        def bot(cx, cy, r, filled):
            box = [cx - r, cy - r * .86, cx + r, cy + r * .86]
            if filled:
                d.rounded_rectangle(box, radius=int(r * .32), fill=MAG + (255,))
            else:
                d.rounded_rectangle(box, radius=int(r * .32), outline=WHITE + (240,), width=8)
            ink = (12, 10, 18, 255) if filled else WHITE + (240,)
            for sx in (-1, 1):
                ey = cy - r * .04
                d.rounded_rectangle([cx + sx * r * .40 - r * .085, ey - r * .15,
                                     cx + sx * r * .40 + r * .085, ey + r * .15],
                                    radius=r * .085, fill=ink)
                d.line([(cx + sx * r * .17, ey - r * .34), (cx + sx * r * .57, ey - r * .43)],
                       fill=ink, width=int(r * .075))
            d.line([(cx, cy - r * .86), (cx, cy - r * 1.12)], fill=ink, width=int(r * .05))
            d.ellipse([cx - r * .07, cy - r * 1.24, cx + r * .07, cy - r * 1.10], fill=ink)
        bot(480, 560, 200, True)
        bot(820, 620, 176, False)
        cx, cy = 650, 570
        for ang in range(0, 360, 40):
            a = math.radians(ang + 12)
            x1, y1 = cx + math.cos(a) * 46, cy + math.sin(a) * 46
            x2, y2 = cx + math.cos(a) * (92 if ang % 80 == 0 else 68), cy + math.sin(a) * (92 if ang % 80 == 0 else 68)
            d.line([(x1, y1), (x2, y2)], fill=GOLD + (255,), width=10)
    cv.draw(heads)

    def t(d):
        f = F(210, "Black")
        d.text((M, 1076), "吵起来了", font=f, fill=WHITE + (255,), anchor="ls")
        d.text((M, 1196), "两个 agent 打架，第三个在劝架",
               font=F(44, "Medium"), fill=DIM + (238,), anchor="ls")
    cv.draw(t)
    marker(cv, M + 10, M + tw("吵起来了", F(210, "Black")) - 30, 1096, 13, MAG, 3)
    return cv

# ------------------------------------------------------------------ 04 金句
def cover_quote():
    cv = Canvas(); base(cv, 0.58, 0.62, 900, 52, 0.64)
    eyebrow(cv, "AI 时代 · 02")
    sz = fit_size("别再攒经验", 880)
    f1 = F(sz, "Black")

    def t(d):
        d.text((M, 700), "别再攒经验", font=f1, fill=WHITE + (255,), anchor="ls")
        d.text((M, 940), "让 AI 替你选", font=F(134, "Black"), fill=MAG + (255,), anchor="ls")
    cv.draw(t)
    rule(cv, 1148, M, M + 320, 44, 3)
    note(cv, "5 亿条经验，替你筛一遍", 1224, 42)
    return cv

# ------------------------------------------------------------------ 05 工具
def cover_hands():
    cv = Canvas(); base(cv, 0.5, 0.14, 800, 62, 0.66)
    eyebrow(cv, "8 个免费插件")

    def t(d):
        d.text((M, 500), "让 AI", font=F(180, "Black"), fill=WHITE + (255,), anchor="ls")
        d.text((M, 736), "长出双手", font=F(180, "Black"), fill=WHITE + (255,), anchor="ls")
        d.text((M, 892), "不然它只能陪你聊天", font=F(48, "Medium"), fill=DIM + (240,), anchor="ls")
    cv.draw(t)
    marker(cv, M + 12, M + tw("长出双手", F(180, "Black")) - 16, 772, 15, MAG, 4)

    def chips(d):
        for i in range(8):
            x = M + i * 111
            d.rounded_rectangle([x, 1064, x + 96, 1064 + 96], radius=26,
                                fill=(255, 255, 255, 16), outline=(255, 255, 255, 32), width=2)
            d.rounded_rectangle([x + 28, 1064 + 28, x + 68, 1064 + 68], radius=11,
                                outline=MAG + (215,), width=4)
    cv.draw(chips)
    note(cv, "点一下，AI 直接动手", 1250, 40)
    return cv

# ------------------------------------------------------------------ 06 公式
def cover_equation():
    cv = Canvas(); base(cv, 0.30, 0.58, 860, 60, 0.66)
    eyebrow(cv, "AI 团队 · 05")

    def t(d):
        d.text((M, 560), "1 个人", font=F(112, "Black"), fill=WHITE + (255,), anchor="ls")
        d.text((M, 728), "+ 5 个 AI", font=F(112, "Black"), fill=WHITE + (255,), anchor="ls")
        rule(cv, 800, M, M + 470, 38, 2)
        f = F(150, "Black")
        d.text((M, 980), "=", font=f, fill=MAG + (255,), anchor="ls")
        d.text((M + tw("=", f) + 46, 980), "一支团队", font=f, fill=MAG + (255,), anchor="ls")
    cv.draw(t)
    note(cv, "不招人，不发工资", 1170, 46, 210, DIM)
    return cv

COVERS = [
    (cover_num4(),     "A｜数字锚点", "把「4 个」做成最大的东西"),
    (cover_30to3(),    "B｜对比",     "一错一对，两个数字讲完"),
    (cover_fight(),    "C｜冲突图形", "先给情绪，再给信息"),
    (cover_quote(),    "D｜金句",     "纯字，一个字都不多"),
    (cover_hands(),    "E｜工具",     "插件当纹理，不用读"),
    (cover_equation(), "F｜公式",     "等式比形容词好记"),
]

def build_sheet():
    cw, ch = 596, 795
    gap, pad = 42, 58
    head_h, cap_h = 268, 78
    cols, rows = 3, 2
    SW = pad * 2 + cols * cw + (cols - 1) * gap
    SH = head_h + rows * (ch + cap_h + gap) + 300
    sheet = Image.new("RGBA", (SW, SH), (8, 7, 13, 255))
    d = ImageDraw.Draw(sheet)

    d.rounded_rectangle([pad, 62, pad + 92, 69], radius=3, fill=MAG + (255,))
    d.text((pad, 86), "同一套系统，6 种做法", font=F(60, "Black"), fill=WHITE + (255,))
    d.text((pad, 178), "一张封面 = 1 句钩子 + 1 个重点 + 2 块安静的地方　|　3:4 · 1080×1440",
           font=F(26, "Medium"), fill=FAINT + (255,))

    for i, (cv, tag, desc) in enumerate(COVERS):
        r, c = divmod(i, cols)
        x = pad + c * (cw + gap)
        y = head_h + r * (ch + cap_h + gap)
        sheet.alpha_composite(cv.img.resize((cw, ch), Image.LANCZOS), (x, y))
        d.rounded_rectangle([x, y, x + cw - 1, y + ch - 1], radius=16, outline=(255, 255, 255, 26), width=2)
        d.text((x + 2, y + ch + 16), tag, font=F(27, "Black"), fill=MAG + (255,))
        d.text((x + 2, y + ch + 48), desc, font=F(23, "Medium"), fill=DIM + (235,))

    my = head_h + rows * (ch + cap_h + gap) + 28
    d.text((pad, my), "缩到信息流大小（150px 宽）——还认得出，才算过；认不出，就是白做",
           font=F(27, "Bold"), fill=DIM + (255,))
    for i, (cv, _, _) in enumerate(COVERS):
        x = pad + i * 158
        sheet.alpha_composite(cv.img.resize((148, 197), Image.LANCZOS), (x, my + 46))
        d.rounded_rectangle([x, my + 46, x + 147, my + 242], radius=7, outline=(255, 255, 255, 22), width=1)

    sheet.convert("RGB").save(os.path.join(OUT, "system-6-templates.png"))
    return sheet

def build_compare():
    b = Image.open(os.path.join(BASE, "assets", "before-github-cover.png")).convert("RGB")
    a = cover_hire_github().img.resize((690, 920), Image.LANCZOS)

    pad, head = 54, 236
    SW = pad * 2 + b.width + 106 + a.width
    SH = head + max(b.height, a.height) + 320
    sh = Image.new("RGB", (SW, SH), (8, 7, 13))
    d = ImageDraw.Draw(sh)

    d.text((pad, 40), "同一期：装完 agent，接上 GitHub", font=F(62, "Black"), fill=WHITE)
    d.text((pad, 124), "左边 12 个信息块 / 8 级字号　→　右边 4 个信息块 / 3 级字号", font=F(28, "Medium"), fill=FAINT)

    d.text((pad, head - 48), "改 前", font=F(28, "Black"), fill=(146, 139, 160))
    sh.paste(b, (pad, head))
    bx = pad + b.width + 106
    d.text((bx, head - 48), "改 后", font=F(28, "Black"), fill=MAG)
    sh.paste(a, (bx, head))

    ax = pad + b.width + 30
    ay = head + b.height // 2
    d.line([(ax, ay), (ax + 40, ay)], fill=MAG, width=6)
    d.polygon([(ax + 56, ay), (ax + 34, ay - 13), (ax + 34, ay + 13)], fill=MAG)

    notes = [
        "①  左上栏目 + 右上分类 + 顶部一行小字：最贵的顶部 200px 全给了「我是谁」，不是「这期讲什么」",
        "②  主标用了三种处理（白字 / 色块 / 粉描边）＝三种都是重点 ＝ 没有重点",
        "③  01–04 清单缩到信息流里只有 6px 高，是噪点不是信息",
        "④  浮窗贴着人脸，人的视线被自己的字挡住",
        "⑤  点赞数、标题条、水印都烧进了封面里，和平台自带的标题栏重复",
    ]
    ny = head + max(b.height, a.height) + 56
    for i, t in enumerate(notes):
        d.text((pad, ny + i * 46), t, font=F(25, "Medium"), fill=(198, 192, 208))
    sh.save(os.path.join(OUT, "before-after.png"))

def cover_hire_github():
    cv = Canvas(); base(cv, 0.80, 0.60, 840, 70, 0.64)
    eyebrow(cv, "AGENT · 09")

    def t(d):
        d.text((M, 400), "装完 Agent", font=F(100, "Black"), fill=(214, 208, 226), anchor="ls")
        d.text((M, 620), "接上", font=F(164, "Black"), fill=WHITE + (255,), anchor="ls")
        x = M + tw("接上", F(164, "Black")) + 16
        d.text((x, 620), "GitHub", font=F(164, "Black"), fill=MAG + (255,), anchor="ls")
        d.text((M + 4, 752), "从「能聊天」到「能干活」", font=F(48, "Medium"), fill=DIM + (238,), anchor="ls")
    cv.draw(t)

    def chips(d):
        for i, s in enumerate(["省时间", "省 Token", "省钱"]):
            x = M + i * 212
            d.rounded_rectangle([x, 830, x + 192, 830 + 74], radius=37,
                                fill=(255, 255, 255, 16), outline=(255, 255, 255, 34), width=2)
            d.text((x + 96, 830 + 37), s, font=F(36, "Black"), fill=WHITE + (238,), anchor="mm")
    cv.draw(chips)

    # 人像位（示意框）
    def ph(d):
        box = [600, 944, 1016, 1392]
        dash = 22
        x0, y0, x1, y1 = box
        for xx in range(x0, x1, dash * 2):
            d.line([(xx, y0), (min(xx + dash, x1), y0)], fill=WHITE + (60,), width=2)
            d.line([(xx, y1), (min(xx + dash, x1), y1)], fill=WHITE + (60,), width=2)
        for yy in range(y0, y1, dash * 2):
            d.line([(x0, yy), (x0, min(yy + dash, y1))], fill=WHITE + (60,), width=2)
            d.line([(x1, yy), (x1, min(yy + dash, y1))], fill=WHITE + (60,), width=2)
        d.text(((x0 + x1) / 2, (y0 + y1) / 2), "人像位", font=F(38, "Medium"), fill=WHITE + (95,), anchor="mm")
        d.text(((x0 + x1) / 2, (y0 + y1) / 2 + 48), "半身，压右下角", font=F(26, "Medium"),
               fill=WHITE + (70,), anchor="mm")
    cv.draw(ph)
    return cv

if __name__ == "__main__":
    build_sheet()
    build_compare()
    for i, (cv, _, _) in enumerate(COVERS):
        cv.img.convert("RGB").save(os.path.join(OUT, f"cover-{i}.png"))
    cover_hire_github().img.convert("RGB").save(os.path.join(OUT, "case-4x3-like.png"))
    print("ok")


#!/usr/bin/env python3
"""Draw the front page for Tuesday 24 November 2026 and save entry.png.

Fresh drawing made for this competition only, with Pillow, no network
and no external assets. Layout: paper masthead "THE WORLD" with the
date, one lead story (the candy-factory fire in Banten, Indonesia)
with a hand-drawn night-fire panel, four story cards in a 2x2 grid
(Kyiv under fire, COP31 stalls, Lisbon marches, Alcaraz wins in
Turin), and an "also today" ticker strip along the bottom.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (24, 24, 22)
NAVY = (18, 34, 58)
RED = (176, 28, 28)
GOLD = (184, 124, 22)
TEAL = (14, 102, 98)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
GREY = (96, 94, 88)
LINE = (196, 188, 168)
DARK = (28, 28, 32)
ORANGE = (232, 110, 24)
FLAME = (244, 178, 44)
SMOKE = (120, 116, 110)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif(size):
    return load("DejaVuSerif-Bold.ttf", size)


def serif_reg(size):
    return load("DejaVuSerif.ttf", size)


def sans(size):
    return load("DejaVuSans.ttf", size)


def sans_b(size):
    return load("DejaVuSans-Bold.ttf", size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, max_w, fill, leading=None):
    step = leading or int(font.size * 1.35)
    for line in wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += step
    return y


def centre(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + int(font.size * 1.3)


def flame(draw, x, base_y, w, h):
    """One stylised flame: layered teardrops in yellow, orange, red."""
    for frac, col in ((1.0, RED), (0.72, ORANGE), (0.45, FLAME)):
        fw, fh = w * frac, h * frac
        x0, x1 = x - fw / 2, x + fw / 2
        y1 = base_y
        y0 = base_y - fh
        draw.pieslice([x0, y0, x1, y1], 180, 360, fill=col)
        draw.polygon([(x0, y1 - fh * 0.3), (x, y0 - fh * 0.22),
                      (x1, y1 - fh * 0.3)], fill=col)


def fire_panel(draw, x0, y0, x1, y1):
    """Night at the burning factory: dark sky, factory block, flames
    and smoke kept inside the panel, a fire truck at the gate."""
    draw.rectangle([x0, y0, x1, y1], fill=(26, 22, 34))
    for i in range(6):
        band = (26 + i * 4, 22 + i * 3, 34 + i * 5)
        yy = y0 + i * (y1 - y0) // 6
        draw.rectangle([x0, yy, x1, yy + (y1 - y0) // 6 + 1], fill=band)
    # distant town lights
    for sx, sy in [(40, 22), (120, 12), (230, 26), (330, 14), (470, 24),
                   (560, 10), (700, 22), (820, 16), (900, 26)]:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=(228, 210, 150))
    # factory block
    fx0, fx1 = x0 + 60, x1 - 60
    fy0, fy1 = y0 + 100, y1 - 38
    draw.rectangle([fx0, fy0, fx1, fy1], fill=(52, 48, 58))
    draw.rectangle([fx0, fy0, fx1, fy0 + 8], fill=(70, 64, 76))
    # roofline vents
    for vx in (fx0 + 40, fx0 + 300, fx1 - 120):
        draw.rectangle([vx, fy0 - 22, vx + 46, fy0], fill=(44, 40, 50))
    # windows, some lit by the fire
    for i in range(8):
        wx = fx0 + 30 + i * 104
        col = (240, 170, 60) if i % 3 == 0 else (30, 28, 36)
        draw.rectangle([wx, fy0 + 14, wx + 56, fy0 + 28], fill=col)
    # flames along the roof (tops stay inside the panel)
    for fx in (fx0 + 90, fx0 + 260, fx0 + 430, fx0 + 600, fx0 + 760):
        flame(draw, fx, fy0 + 6, 84, 72)
    # smoke columns, kept below the panel top
    for sx, sway in ((fx0 + 180, -1), (fx0 + 520, 1), (fx0 + 700, -1)):
        for k in range(3):
            r = 12 + k * 8
            cx = sx + sway * k * 14
            cy = fy0 - 18 - k * 16
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    # ground and fire truck
    draw.rectangle([x0, fy1, x1, y1], fill=(16, 14, 20))
    tx0 = x0 + 90
    draw.rectangle([tx0, fy1 - 30, tx0 + 150, fy1], fill=(176, 28, 28))
    draw.rectangle([tx0 + 150, fy1 - 22, tx0 + 196, fy1], fill=(140, 20, 20))
    for wx in (tx0 + 14, tx0 + 66, tx0 + 118):
        draw.ellipse([wx, fy1 - 8, wx + 16, fy1 + 8], fill=(12, 12, 12))
    draw.rectangle([tx0 + 30, fy1 - 42, tx0 + 60, fy1 - 30], fill=FLAME)
    # hose line and two rescuers
    draw.line([(tx0 + 200, fy1 - 4), (x1 - 180, fy1 - 4)], fill=GREY, width=4)
    for rx in (x1 - 260, x1 - 220):
        draw.ellipse([rx - 7, fy1 - 32, rx + 7, fy1 - 18], fill=(240, 190, 60))
        draw.rectangle([rx - 6, fy1 - 18, rx + 6, fy1], fill=(240, 190, 60))
    draw.text((x0 + 24, y1 - 28), "BANTEN, INDONESIA — AFTER DARK",
              font=sans_b(16), fill=(232, 220, 190))


def kyiv_card(draw, x0, y0, x1, y1):
    """City skyline at night, an explosion burst and drone dots."""
    draw.rectangle([x0, y0, x1, y1], fill=(24, 30, 52))
    for sx, sy in [(20, 12), (70, 22), (140, 9), (200, 19), (260, 11)]:
        draw.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1],
                     fill=(220, 220, 200))
    # skyline
    base = y1 - 22
    for bx, bw, bh in [(8, 34, 30), (52, 26, 40), (88, 40, 26),
                       (138, 30, 44), (178, 36, 34), (224, 30, 38)]:
        draw.rectangle([x0 + bx, base - bh, x0 + bx + bw, base],
                       fill=(12, 14, 24))
        for wy in range(base - bh + 6, base - 5, 12):
            draw.rectangle([x0 + bx + 6, wy, x0 + bx + 12, wy + 5],
                           fill=(240, 200, 90))
    # explosion burst
    cx, cy = x0 + 150, y0 + 40
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        ex = cx + 38 * math.cos(rad)
        ey = cy + 26 * math.sin(rad)
        draw.line([(cx, cy), (ex, ey)], fill=ORANGE, width=4)
    draw.ellipse([cx - 22, cy - 15, cx + 22, cy + 15], fill=FLAME)
    draw.ellipse([cx - 10, cy - 7, cx + 10, cy + 7], fill=WHITE)
    # drones
    for dx, dy in [(30, 52), (210, 30), (250, 56)]:
        draw.ellipse([x0 + dx - 3, y0 + dy - 3, x0 + dx + 3, y0 + dy + 3],
                     fill=(200, 60, 60))
    draw.rectangle([x0, y1 - 22, x1, y1], fill=(12, 14, 24))


def cop_card(draw, x0, y0, x1, y1):
    """A summit table that never agreed: flags around an empty chair,
    a small cracked globe above."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 222, 206))
    cx, cy, r = (x0 + x1) // 2, y0 + 34, 24
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 128, 170))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 220, 235),
                 width=2)
    draw.polygon([(cx - 14, cy - 4), (cx - 3, cy - 13), (cx + 6, cy - 6),
                  (cx - 1, cy + 4), (cx - 11, cy + 7)], fill=(96, 150, 92))
    draw.polygon([(cx + 4, cy + 7), (cx + 15, cy + 1), (cx + 17, cy + 11),
                  (cx + 7, cy + 15)], fill=(96, 150, 92))
    # crack across the globe
    draw.line([(cx - 13, cy - 16), (cx - 3, cy - 3), (cx + 7, cy - 9),
               (cx + 14, cy + 6)], fill=WHITE, width=2)
    # table
    ty = y1 - 20
    draw.ellipse([x0 + 30, ty - 18, x1 - 30, ty + 8], fill=(120, 84, 44))
    draw.ellipse([x0 + 30, ty - 24, x1 - 30, ty + 2], fill=(146, 104, 58))
    # flags around the table
    for fx, col in ((x0 + 52, RED), (x0 + 96, TEAL), (x1 - 96, GOLD),
                    (x1 - 52, NAVY)):
        draw.line([(fx, ty - 22), (fx, ty - 48)], fill=INK, width=2)
        draw.polygon([(fx, ty - 48), (fx + 24, ty - 41), (fx, ty - 34)],
                     fill=col)
    # one empty chair
    draw.rectangle([(x0 + x1) // 2 - 14, ty - 46, (x0 + x1) // 2 + 14,
                    ty - 24], outline=INK, width=3)


def lisbon_card(draw, x0, y0, x1, y1):
    """A street march: a crowd of heads and shoulders, placards up."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 214, 176))
    # rooftops behind
    draw.rectangle([x0, y0 + 14, x1, y0 + 34], fill=(198, 120, 60))
    for wx in range(14, 260, 44):
        draw.rectangle([x0 + wx, y0 + 18, x0 + wx + 26, y0 + 30],
                       fill=(250, 240, 210))
    # crowd
    cols = [(52, 60, 70), (120, 70, 60), (176, 28, 28), (60, 90, 110),
            (90, 60, 90)]
    for i, col in enumerate(cols * 2):
        hx = x0 + 26 + i * 26
        hy = y0 + 58 + (i % 2) * 6
        draw.ellipse([hx - 9, hy - 9, hx + 9, hy + 9], fill=(222, 178, 140))
        draw.pieslice([hx - 15, hy + 6, hx + 15, hy + 30], 180, 360, fill=col)
    # placards
    for px, py, txt in ((x0 + 44, y0 + 24, "VIDA"), (x0 + 170, y0 + 20, "JUSTA")):
        draw.line([(px + 12, py + 18), (px + 12, py + 44)], fill=INK, width=3)
        draw.rectangle([px - 14, py - 6, px + 38, py + 18], fill=WHITE,
                       outline=INK, width=2)
        draw.text((px - 8, py - 2), txt, font=sans_b(13), fill=INK)
    draw.rectangle([x0, y1 - 22, x1, y1], fill=(198, 120, 60))


def tennis_card(draw, x0, y0, x1, y1):
    """Centre court from above: green court, white lines, one ball."""
    draw.rectangle([x0, y0, x1, y1], fill=(36, 110, 74))
    draw.rectangle([x0 + 26, y0 + 12, x1 - 26, y1 - 12], outline=WHITE, width=3)
    draw.line([(x0 + 26, (y0 + y1) // 2), (x1 - 26, (y0 + y1) // 2)],
              fill=WHITE, width=3)
    draw.line([((x0 + x1) // 2, y0 + 12), ((x0 + x1) // 2, y1 - 12)],
              fill=WHITE, width=2)
    draw.rectangle([x0 + 60, y0 + 28, x1 - 60, y1 - 28], outline=WHITE, width=2)
    # net
    draw.rectangle([(x0 + x1) // 2 - 3, y0 + 12, (x0 + x1) // 2 + 3, y1 - 12],
                   fill=(20, 60, 44))
    # ball mid-flight with trail
    bx, by = x0 + 196, y0 + 34
    for k in range(4):
        r = 5 + k
        draw.ellipse([bx - 46 - k * 14 - r, by + k * 8 - r,
                      bx - 46 - k * 14 + r, by + k * 8 + r],
                     outline=(220, 240, 90), width=2)
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(214, 232, 64),
                 outline=WHITE, width=2)
    draw.arc([bx - 12, by - 12, bx + 12, by + 12], 300, 60, fill=WHITE, width=2)
    # trophy glint
    draw.polygon([(x0 + 34, y1 - 18), (x0 + 52, y1 - 40), (x0 + 70, y1 - 18)],
                 fill=GOLD)


def card(draw, x0, y0, x1, y1, kicker, title, body, art):
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=LINE, width=2)
    art(draw, x0 + 2, y0 + 2, x1 - 2, y0 + 92)
    draw.text((x0 + 14, y0 + 98), kicker, font=sans_b(15), fill=RED)
    y = para(draw, x0 + 14, y0 + 118, title, serif(22), x1 - x0 - 28, INK)
    para(draw, x0 + 14, y + 4, body, sans(16), x1 - x0 - 28, (52, 50, 46),
         leading=21)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)
    d.rectangle([16, 16, W - 17, H - 17], outline=LINE, width=1)

    # masthead
    centre(d, W // 2, 22, "THE WORLD", serif(84), INK)
    d.line([(48, 140), (W - 48, 140)], fill=RED, width=4)
    centre(d, W // 2, 148, "TUESDAY 24 NOVEMBER 2026  ·  ONE DAY, ONE PICTURE",
           sans_b(20), (70, 68, 62))
    d.line([(48, 182), (W - 48, 182)], fill=INK, width=2)

    # lead headline + deck
    y = para(d, 48, 192, "FIRE AT INDONESIA CANDY FACTORY KILLS AT LEAST 24",
             serif(36), W - 96, INK, leading=43)
    para(d, 48, y + 6,
         "Rescuers dig through the gutted plant in Banten for around 30 "
         "workers still missing, as families wait at the gates.",
         serif_reg(21), W - 96, (52, 50, 46), leading=26)

    # lead picture
    fire_panel(d, 48, 344, W - 48, 514)

    # 2x2 story cards
    gx, gy = 48, 528
    cw, ch, gap = 452, 204, 24
    card(d, gx, gy, gx + cw, gy + ch, "UKRAINE",
         "Kyiv region hit again",
         "Russian drones and missiles hit homes in Dymer; several killed "
         "and missing. A ship burns off Finland.",
         kyiv_card)
    card(d, gx + cw + gap, gy, gx + 2 * cw + gap, gy + ch, "CLIMATE",
         "COP31 ends divided",
         "Talks in Antalya close with no deal on phasing out fossil "
         "fuels, as negotiators stay split.",
         cop_card)
    card(d, gx, gy + ch + gap, gx + cw, gy + 2 * ch + gap, "PORTUGAL",
         "Lisbon marches on prices",
         "Thousands fill Lisbon's streets to protest the rising cost of "
         "living across Europe.",
         lisbon_card)
    card(d, gx + cw + gap, gy + ch + gap, gx + 2 * cw + gap,
         gy + 2 * ch + gap, "SPORT",
         "Alcaraz takes Turin",
         "Carlos Alcaraz beats Zverev for a first ATP Finals title. "
         "Gukesh opens his chess defence in Geneva.",
         tennis_card)

    # ticker (two lines)
    ty = 960
    d.rectangle([48, ty, W - 48, ty + 46], fill=INK)
    d.text((60, ty + 4), "ALSO TODAY", font=sans_b(15), fill=(240, 200, 80))
    d.text((188, ty + 4),
           "EU unveils 22nd Russia sanctions  ·  Ukraine sinks Russian "
           "warship off Libya  ·  Nvidia brings back Huang",
           font=sans(14), fill=WHITE)
    d.text((188, ty + 24),
           "Migrant boat capsizes off Senegal  ·  ICJ: Myanmar committed "
           "genocide  ·  India–Nepal train flagged off",
           font=sans(14), fill=WHITE)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

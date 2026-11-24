#!/usr/bin/env python3
"""Paint the front page for Tuesday 24 November 2026 as entry.png.

Everything here is drawn in this file with Pillow: no network, no
outside assets, no fonts beyond the DejaVu set on the machine. The
page is a newspaper front: a masthead naming the day, a lead picture
story on the factory fire in Banten, four smaller stories (Kyiv,
COP31, Lisbon, Turin) and a strip of the day's other headlines.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
SHEET = (247, 243, 232)
INK_COL = (24, 24, 22)
MIDNIGHT = (18, 34, 58)
CRIMSON = (176, 28, 28)
BRASS = (184, 124, 22)
PINE = (14, 102, 98)
SNOW = (255, 255, 255)
CARD_BG = (255, 255, 255)
ASH = (96, 94, 88)
RULE_COL = (196, 188, 168)
EMBER = (232, 110, 24)
GOLDEN = (244, 178, 44)
HAZE = (120, 116, 110)
NIGHT_SKY = (26, 22, 34)

TYPE_DIR = "/usr/share/fonts/truetype/dejavu"


def typeface(filename, pts):
    return ImageFont.truetype(os.path.join(TYPE_DIR, filename), pts)


def headline_font(pts):
    return typeface("DejaVuSerif-Bold.ttf", pts)


def serif_body(pts):
    return typeface("DejaVuSerif.ttf", pts)


def plain_font(pts):
    return typeface("DejaVuSans.ttf", pts)


def bold_font(pts):
    return typeface("DejaVuSans-Bold.ttf", pts)


def wrap_words(pen, text, font, width):
    """Split text into lines that fit width, word by word."""
    out, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if pen.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def text_block(pen, left, top, text, font, width, colour, gap=None):
    """Draw a wrapped paragraph; return the y just below it."""
    step = gap if gap is not None else int(font.size * 1.35)
    cursor = top
    for line in wrap_words(pen, text, font, width):
        pen.text((left, cursor), line, font=font, fill=colour)
        cursor += step
    return cursor


def centered_line(pen, middle, top, text, font, colour):
    """Draw one line centred on middle; return the y below it."""
    wide = pen.textlength(text, font=font)
    pen.text((middle - wide / 2, top), text, font=font, fill=colour)
    return top + int(font.size * 1.3)


def flame_shape(pen, middle, floor, wide, tall):
    """A stylised flame: three stacked teardrops, red to yellow."""
    for share, colour in ((1.0, CRIMSON), (0.72, EMBER), (0.45, GOLDEN)):
        fw, fh = wide * share, tall * share
        left, right = middle - fw / 2, middle + fw / 2
        base = floor
        tip = floor - fh
        pen.pieslice([left, tip, right, base], 180, 360, fill=colour)
        pen.polygon(
            [(left, base - fh * 0.3), (middle, tip - fh * 0.22),
             (right, base - fh * 0.3)],
            fill=colour,
        )


def night_fire(pen, left, top, right, bottom):
    """The burning factory at night: dark sky, a low factory block
    with flames on its roof, smoke staying inside the frame, and a
    fire engine with two rescuers at the gate."""
    pen.rectangle([left, top, right, bottom], fill=NIGHT_SKY)
    span = bottom - top
    for band in range(6):
        shade = (26 + band * 4, 22 + band * 3, 34 + band * 5)
        yb = top + band * span // 6
        pen.rectangle([left, yb, right, yb + span // 6 + 1], fill=shade)
    for sx, sy in [(40, 22), (120, 12), (230, 26), (330, 14), (470, 24),
                   (560, 10), (700, 22), (820, 16), (900, 26)]:
        pen.ellipse([left + sx - 2, top + sy - 2, left + sx + 2, top + sy + 2],
                    fill=(228, 210, 150))
    fx0, fx1 = left + 60, right - 60
    fy0, fy1 = top + 100, bottom - 38
    pen.rectangle([fx0, fy0, fx1, fy1], fill=(52, 48, 58))
    pen.rectangle([fx0, fy0, fx1, fy0 + 8], fill=(70, 64, 76))
    for vx in (fx0 + 40, fx0 + 300, fx1 - 120):
        pen.rectangle([vx, fy0 - 22, vx + 46, fy0], fill=(44, 40, 50))
    for i in range(8):
        wx = fx0 + 30 + i * 104
        lit = (240, 170, 60) if i % 3 == 0 else (30, 28, 36)
        pen.rectangle([wx, fy0 + 14, wx + 56, fy0 + 28], fill=lit)
    for fx in (fx0 + 90, fx0 + 260, fx0 + 430, fx0 + 600, fx0 + 760):
        flame_shape(pen, fx, fy0 + 6, 84, 72)
    for sx, drift in ((fx0 + 180, -1), (fx0 + 520, 1), (fx0 + 700, -1)):
        for k in range(3):
            r = 12 + k * 8
            cx = sx + drift * k * 14
            cy = fy0 - 18 - k * 16
            pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=HAZE)
    pen.rectangle([left, fy1, right, bottom], fill=(16, 14, 20))
    tx0 = left + 90
    pen.rectangle([tx0, fy1 - 30, tx0 + 150, fy1], fill=CRIMSON)
    pen.rectangle([tx0 + 150, fy1 - 22, tx0 + 196, fy1], fill=(140, 20, 20))
    for wx in (tx0 + 14, tx0 + 66, tx0 + 118):
        pen.ellipse([wx, fy1 - 8, wx + 16, fy1 + 8], fill=(12, 12, 12))
    pen.rectangle([tx0 + 30, fy1 - 42, tx0 + 60, fy1 - 30], fill=GOLDEN)
    pen.line([(tx0 + 200, fy1 - 4), (right - 180, fy1 - 4)], fill=ASH, width=4)
    for rx in (right - 260, right - 220):
        pen.ellipse([rx - 7, fy1 - 32, rx + 7, fy1 - 18], fill=(240, 190, 60))
        pen.rectangle([rx - 6, fy1 - 18, rx + 6, fy1], fill=(240, 190, 60))
    pen.text((left + 24, bottom - 28), "BANTEN, INDONESIA — AFTER DARK",
             font=bold_font(16), fill=(232, 220, 190))


def kyiv_scene(pen, left, top, right, bottom):
    """A night skyline, a burst over the rooftops, drone dots."""
    pen.rectangle([left, top, right, bottom], fill=(24, 30, 52))
    for sx, sy in [(20, 12), (70, 22), (140, 9), (200, 19), (260, 11)]:
        pen.ellipse([left + sx - 1, top + sy - 1, left + sx + 1, top + sy + 1],
                    fill=(220, 220, 200))
    base = bottom - 22
    for bx, bw, bh in [(8, 34, 30), (52, 26, 40), (88, 40, 26),
                       (138, 30, 44), (178, 36, 34), (224, 30, 38)]:
        pen.rectangle([left + bx, base - bh, left + bx + bw, base],
                      fill=(12, 14, 24))
        for wy in range(base - bh + 6, base - 5, 12):
            pen.rectangle([left + bx + 6, wy, left + bx + 12, wy + 5],
                          fill=(240, 200, 90))
    cx, cy = left + 150, top + 40
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        ex = cx + 38 * math.cos(rad)
        ey = cy + 26 * math.sin(rad)
        pen.line([(cx, cy), (ex, ey)], fill=EMBER, width=4)
    pen.ellipse([cx - 22, cy - 15, cx + 22, cy + 15], fill=GOLDEN)
    pen.ellipse([cx - 10, cy - 7, cx + 10, cy + 7], fill=SNOW)
    for dx, dy in [(30, 52), (210, 30), (250, 56)]:
        pen.ellipse([left + dx - 3, top + dy - 3, left + dx + 3, top + dy + 3],
                    fill=(200, 60, 60))
    pen.rectangle([left, bottom - 22, right, bottom], fill=(12, 14, 24))


def summit_scene(pen, left, top, right, bottom):
    """A climate summit that never agreed: little flags around a
    table, one empty chair, a small cracked globe above it all."""
    pen.rectangle([left, top, right, bottom], fill=(226, 222, 206))
    cx, cy, r = (left + right) // 2, top + 34, 24
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 128, 170))
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 220, 235),
                width=2)
    pen.polygon([(cx - 14, cy - 4), (cx - 3, cy - 13), (cx + 6, cy - 6),
                 (cx - 1, cy + 4), (cx - 11, cy + 7)], fill=(96, 150, 92))
    pen.polygon([(cx + 4, cy + 7), (cx + 15, cy + 1), (cx + 17, cy + 11),
                 (cx + 7, cy + 15)], fill=(96, 150, 92))
    pen.line([(cx - 13, cy - 16), (cx - 3, cy - 3), (cx + 7, cy - 9),
              (cx + 14, cy + 6)], fill=SNOW, width=2)
    ty = bottom - 20
    pen.ellipse([left + 30, ty - 18, right - 30, ty + 8], fill=(120, 84, 44))
    pen.ellipse([left + 30, ty - 24, right - 30, ty + 2], fill=(146, 104, 58))
    for fx, colour in ((left + 52, CRIMSON), (left + 96, PINE),
                       (right - 96, BRASS), (right - 52, MIDNIGHT)):
        pen.line([(fx, ty - 22), (fx, ty - 48)], fill=INK_COL, width=2)
        pen.polygon([(fx, ty - 48), (fx + 24, ty - 41), (fx, ty - 34)],
                    fill=colour)
    pen.rectangle([(left + right) // 2 - 14, ty - 46, (left + right) // 2 + 14,
                   ty - 24], outline=INK_COL, width=3)


def march_scene(pen, left, top, right, bottom):
    """A street march: rooftops behind, a crowd of heads below,
    two placards held up."""
    pen.rectangle([left, top, right, bottom], fill=(232, 214, 176))
    pen.rectangle([left, top + 14, right, top + 34], fill=(198, 120, 60))
    for wx in range(14, 260, 44):
        pen.rectangle([left + wx, top + 18, left + wx + 26, top + 30],
                      fill=(250, 240, 210))
    shirts = [(52, 60, 70), (120, 70, 60), (176, 28, 28), (60, 90, 110),
              (90, 60, 90)]
    for i, colour in enumerate(shirts * 2):
        hx = left + 26 + i * 26
        hy = top + 58 + (i % 2) * 6
        pen.ellipse([hx - 9, hy - 9, hx + 9, hy + 9], fill=(222, 178, 140))
        pen.pieslice([hx - 15, hy + 6, hx + 15, hy + 30], 180, 360, fill=colour)
    for px, py, word in ((left + 44, top + 24, "VIDA"),
                         (left + 170, top + 20, "JUSTA")):
        pen.line([(px + 12, py + 18), (px + 12, py + 44)], fill=INK_COL, width=3)
        pen.rectangle([px - 14, py - 6, px + 38, py + 18], fill=SNOW,
                      outline=INK_COL, width=2)
        pen.text((px - 8, py - 2), word, font=bold_font(13), fill=INK_COL)
    pen.rectangle([left, bottom - 22, right, bottom], fill=(198, 120, 60))


def court_scene(pen, left, top, right, bottom):
    """A tennis court seen from above: green, white lines, a ball
    flying in with its trail, a small trophy glint in the corner."""
    pen.rectangle([left, top, right, bottom], fill=(36, 110, 74))
    pen.rectangle([left + 26, top + 12, right - 26, bottom - 12],
                  outline=SNOW, width=3)
    pen.line([(left + 26, (top + bottom) // 2),
              (right - 26, (top + bottom) // 2)], fill=SNOW, width=3)
    pen.line([((left + right) // 2, top + 12),
              ((left + right) // 2, bottom - 12)], fill=SNOW, width=2)
    pen.rectangle([left + 60, top + 28, right - 60, bottom - 28],
                  outline=SNOW, width=2)
    pen.rectangle([(left + right) // 2 - 3, top + 12,
                   (left + right) // 2 + 3, bottom - 12], fill=(20, 60, 44))
    bx, by = left + 196, top + 34
    for k in range(4):
        r = 5 + k
        pen.ellipse([bx - 46 - k * 14 - r, by + k * 8 - r,
                     bx - 46 - k * 14 + r, by + k * 8 + r],
                    outline=(220, 240, 90), width=2)
    pen.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(214, 232, 64),
                outline=SNOW, width=2)
    pen.arc([bx - 12, by - 12, bx + 12, by + 12], 300, 60, fill=SNOW, width=2)
    pen.polygon([(left + 34, bottom - 18), (left + 52, bottom - 40),
                 (left + 70, bottom - 18)], fill=BRASS)


def story_card(pen, left, top, right, bottom, tag, title, body, scene):
    """One story card: a picture on top, then a kicker, a headline
    and two lines of text."""
    pen.rectangle([left, top, right, bottom], fill=CARD_BG, outline=RULE_COL,
                  width=2)
    scene(pen, left + 2, top + 2, right - 2, top + 92)
    pen.text((left + 14, top + 98), tag, font=bold_font(15), fill=CRIMSON)
    after = text_block(pen, left + 14, top + 118, title, headline_font(22),
                       right - left - 28, INK_COL)
    text_block(pen, left + 14, after + 4, body, plain_font(16),
               right - left - 28, (52, 50, 46), gap=21)


def paint():
    sheet = Image.new("RGB", (PAGE_W, PAGE_H), SHEET)
    pen = ImageDraw.Draw(sheet)
    pen.rectangle([10, 10, PAGE_W - 11, PAGE_H - 11], outline=INK_COL, width=2)
    pen.rectangle([16, 16, PAGE_W - 17, PAGE_H - 17], outline=RULE_COL, width=1)

    centered_line(pen, PAGE_W // 2, 22, "THE WORLD", headline_font(84), INK_COL)
    pen.line([(48, 140), (PAGE_W - 48, 140)], fill=CRIMSON, width=4)
    centered_line(pen, PAGE_W // 2, 148,
                  "TUESDAY 24 NOVEMBER 2026  ·  ONE DAY, ONE PICTURE",
                  bold_font(20), (70, 68, 62))
    pen.line([(48, 182), (PAGE_W - 48, 182)], fill=INK_COL, width=2)

    after_head = text_block(
        pen, 48, 192, "FIRE AT INDONESIA CANDY FACTORY KILLS AT LEAST 24",
        headline_font(36), PAGE_W - 96, INK_COL, gap=43)
    text_block(
        pen, 48, after_head + 6,
        "Rescuers dig through the gutted plant in Banten for around 30 "
        "workers still missing, as families wait at the gates.",
        serif_body(21), PAGE_W - 96, (52, 50, 46), gap=26)

    night_fire(pen, 48, 344, PAGE_W - 48, 514)

    gx, gy = 48, 528
    cw, ch, gap = 452, 204, 24
    story_card(pen, gx, gy, gx + cw, gy + ch, "UKRAINE",
               "Kyiv region hit again",
               "Russian drones and missiles hit homes in Dymer; several killed "
               "and missing. A ship burns off Finland.",
               kyiv_scene)
    story_card(pen, gx + cw + gap, gy, gx + 2 * cw + gap, gy + ch, "CLIMATE",
               "COP31 ends divided",
               "Talks in Antalya close with no deal on phasing out fossil "
               "fuels, as negotiators stay split.",
               summit_scene)
    story_card(pen, gx, gy + ch + gap, gx + cw, gy + 2 * ch + gap, "PORTUGAL",
               "Lisbon marches on prices",
               "Thousands fill Lisbon's streets to protest the rising cost of "
               "living across Europe.",
               march_scene)
    story_card(pen, gx + cw + gap, gy + ch + gap, gx + 2 * cw + gap,
               gy + 2 * ch + gap, "SPORT",
               "Alcaraz takes Turin",
               "Carlos Alcaraz beats Zverev for a first ATP Finals title. "
               "Gukesh opens his chess defence in Geneva.",
               court_scene)

    ty = 960
    pen.rectangle([48, ty, PAGE_W - 48, ty + 46], fill=INK_COL)
    pen.text((60, ty + 4), "ALSO TODAY", font=bold_font(15),
             fill=(240, 200, 80))
    pen.text((188, ty + 4),
             "EU unveils 22nd Russia sanctions  ·  Ukraine sinks Russian "
             "warship off Libya  ·  Nvidia brings back Huang",
             font=plain_font(14), fill=SNOW)
    pen.text((188, ty + 24),
             "Migrant boat capsizes off Senegal  ·  ICJ: Myanmar committed "
             "genocide  ·  India–Nepal train flagged off",
             font=plain_font(14), fill=SNOW)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    sheet.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    paint()

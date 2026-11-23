#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page.

One self-contained Pillow program: it paints a dense newspaper front
page (masthead, burning-tanker lead, six-story grid, also-today strip)
and writes entry.png next to itself. No network, no clock, no random
input, so two runs are byte-identical.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (24, 24, 22)
RED = (178, 34, 34)
NAVY = (31, 52, 84)
NAVY_DARK = (19, 33, 57)
ORANGE = (232, 116, 39)
GOLD = (233, 179, 60)
TEAL = (15, 118, 110)
GREY = (92, 90, 82)
HAIR = (180, 174, 158)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width, word by word."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, width, leading):
    """Draw a wrapped paragraph, return the y below its last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_masthead(draw):
    """THE WORLD TODAY + red date line + double rule."""
    title = "THE WORLD TODAY"
    fnt = serif_b(88)
    tw = draw.textlength(title, font=fnt)
    draw.text(((W - tw) / 2, 14), title, font=fnt, fill=INK)
    draw.line([(28, 118), (W - 28, 118)], fill=INK, width=4)
    draw.line([(28, 126), (W - 28, 126)], fill=INK, width=2)
    date = "MONDAY 23 NOVEMBER 2026"
    dfnt = sans_b(33)
    dw = draw.textlength(date, font=dfnt)
    draw.text(((W - dw) / 2, 140), date, font=dfnt, fill=RED)
    draw.line([(28, 188), (W - 28, 188)], fill=HAIR, width=2)


def flame(draw, x, base, w, h, core):
    """One flame tongue: outer orange triangle, inner gold core."""
    draw.polygon([(x, base), (x + w / 2, base - h), (x + w, base)],
                 fill=ORANGE)
    draw.polygon([(x + w * 0.25, base), (x + w / 2, base - h * 0.62),
                  (x + w * 0.75, base)], fill=core)


def draw_scene(draw, x0, y0, x1, y1):
    """Night strait on the right of the lead: tanker afire, smoke, sun."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY_DARK)
    # low orange sun and drifting smoke
    draw.ellipse([x0 + 28, y0 + 26, x0 + 96, y0 + 94], fill=ORANGE)
    draw.ellipse([x0 + 48, y0 + 44, x0 + 76, y0 + 72], fill=(246, 196, 120))
    for cx, cy, r in [(246, 56, 28), (284, 46, 34), (306, 62, 24)]:
        draw.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r],
                     fill=(110, 116, 130))
    # sea band
    sea = y0 + (y1 - y0) * 0.62
    draw.rectangle([x0, sea, x1, y1], fill=(24, 58, 92))
    for wx in range(0, int(x1 - x0), 46):
        draw.arc([x0 + wx, sea + 26, x0 + wx + 34, sea + 48],
                 start=180, end=360, fill=(140, 180, 215), width=3)
    # tanker hull with portholes, deck containers, bridge tower
    hull_top = sea - 58
    draw.polygon([(x0 + 18, hull_top), (x0 + 330, hull_top),
                  (x0 + 308, sea + 34), (x0 + 40, sea + 34)], fill=(12, 12, 14))
    draw.rectangle([x0 + 18, hull_top - 6, x0 + 330, hull_top + 4],
                   fill=(178, 34, 34))
    for px in range(52, 320, 44):
        draw.ellipse([x0 + px, sea + 6, x0 + px + 12, sea + 18],
                     fill=(246, 196, 120))
    draw.rectangle([x0 + 236, hull_top - 52, x0 + 300, hull_top - 6],
                   fill=(226, 224, 216))
    draw.rectangle([x0 + 246, hull_top - 42, x0 + 290, hull_top - 26],
                   fill=NAVY)
    # flames licking from the deck
    for fx, fw, fh in [(60, 44, 64), (118, 52, 76), (184, 46, 58)]:
        flame(draw, x0 + fx, hull_top - 4, fw, fh, GOLD)
    # missile streaks overhead
    draw.line([(x0 + 30, y0 + 118), (x0 + 150, y0 + 52)], fill=(246, 241, 227),
              width=4)
    draw.ellipse([x0 + 142, y0 + 44, x0 + 158, y0 + 60], fill=(246, 241, 227))


def draw_lead(draw):
    """Dark lead block: kicker, headline, deck, scene on the right."""
    x0, y0, x1, y1 = 28, 204, W - 28, 462
    draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=NAVY)
    tx = x0 + 26
    draw.text((tx, y0 + 20), "THE GULF WAR  ·  STRAIT OF HORMUZ",
              font=sans_b(21), fill=ORANGE)
    head = "TANKER ATTACKS\nAT RECORD LEVEL"
    hy = y0 + 52
    for line in head.split("\n"):
        draw.text((tx, hy), line, font=serif_b(52), fill=(246, 241, 227))
        hy += 60
    deck = ("Three tankers struck in two days as Iran tightens its grip "
            "on the strait. Bahrain base hit; the US blockade runs to "
            "day 130.")
    para(draw, (tx, y0 + 186), deck, sans(20), (214, 210, 198), 560, 26)
    draw_scene(draw, 640, y0 + 14, x1 - 14, y1 - 14)


GRID = [
    # (kicker, kicker colour, headline, deck)
    ("CLIMATE  ·  ANTALYA", RED,
     "COP31 collapses as EU walks out",
     "No fossil-fuel deal after the longest summit."),
    ("AMERICA  ·  WASHINGTON", NAVY,
     "Democrats take control of Congress",
     "Midterm win; 11 December funding fight looms."),
    ("MEXICO  ·  SINALOA", RED,
     "\u201cChapo Isidro\u201d seized in cartel raid",
     "$5m FBI fugitive faces US extradition."),
    ("UKRAINE  ·  KYIV REGION", NAVY,
     "14 missing after drone hits a block",
     "Russian cargo ship still burning off Finland."),
    ("ASIA  ·  NEW DELHI", TEAL,
     "Nepal PM holds talks with Modi",
     "State visit reviews the full range of ties."),
    ("SPORT  ·  WELLINGTON", TEAL,
     "India post a record 720 in Test",
     "India declare on 720/9 \u2014 a record total."),
]


def draw_grid(draw):
    """Two columns, three rows of stories with hairline dividers."""
    top, col_w, gap = 478, 468, 32
    row_h = 134
    for i, (kick, colour, head, deck) in enumerate(GRID):
        col, row = i % 2, i // 2
        x = 28 + col * (col_w + gap)
        y = top + row * row_h
        draw.text((x, y), kick, font=sans_b(19), fill=colour)
        hy = para(draw, (x, y + 26), head, serif_b(28), INK, col_w, 33)
        para(draw, (x, hy + 2), deck, sans(17), GREY, col_w, 23)
        if row < 2:
            draw.line([(x, y + row_h - 10), (x + col_w, y + row_h - 10)],
                      fill=HAIR, width=2)
    midx = 28 + col_w + gap // 2
    draw.line([(midx, top), (midx, top + 3 * row_h - 16)], fill=HAIR, width=2)


ALSO = ("Korea minister quits over AI cheating  ·  Indonesia factory fire: "
        "7 dead, 50 missing  ·  Lisbon cost-of-living march  ·  Youth "
        "Congress protests Meta  ·  Myanmar slams ASEAN")


def draw_also(draw):
    """Black ALSO TODAY band plus the footer line."""
    x0, y0, x1, y1 = 28, 892, W - 28, 986
    draw.rectangle([x0, y0, x1, y1], fill=(18, 18, 16))
    draw.text((x0 + 20, y0 + 12), "ALSO TODAY", font=sans_b(22), fill=GOLD)
    para(draw, (x0 + 20, y0 + 44), ALSO, sans(19), (238, 234, 222),
         x1 - x0 - 40, 26)
    foot = "All stories reported on Monday 23 November 2026  ·  THE WORLD TODAY"
    ffnt = sans(15)
    fw = draw.textlength(foot, font=ffnt)
    draw.text(((W - fw) / 2, 994), foot, font=ffnt, fill=GREY)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw_grid(draw)
    draw_also(draw)
    here = os.path.dirname(os.path.abspath(__file__))
    img.save(os.path.join(here, "entry.png"), format="PNG")
    return img


if __name__ == "__main__":
    build()

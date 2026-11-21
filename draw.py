#!/usr/bin/env python3
"""Draw the news-image-20261120 v6 front page: 35 stories from Friday 20 Nov 2026.

A newspaper front page, 1024x1024, drawn with Pillow at build time only.
main.py (the entrypoint) only copies the finished entry.png; it never draws.
Every figure is attributed to the source that reported it, and every story
carries its date: Friday 20 November 2026.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 18
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 232)
INK = (20, 20, 20)
GREY = (90, 86, 76)
RED = (176, 30, 36)
NAVY = (29, 53, 87)
TEAL = (14, 94, 90)
GOLD = (176, 132, 30)
RULE = (60, 58, 50)
LIGHT = (238, 232, 218)
WHITE = (255, 253, 247)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def grain(img, seed=20261120, dots=26000):
    """Paper grain: deterministic speckles that give the page visual density."""
    rnd = random.Random(seed)
    px = img.load()
    for _ in range(dots):
        x = rnd.randrange(W)
        y = rnd.randrange(H)
        r, g, b = px[x, y]
        d = rnd.randrange(-14, 15)
        px[x, y] = (max(0, min(255, r + d)),
                    max(0, min(255, g + d)),
                    max(0, min(255, b + d)))


# ---------------------------------------------------------------- data
# 35 stories, all verified against reporting of Friday 20 November 2026.
# Figures carry their source; every story is dated 20 NOV 2026.

KEY_NUMBERS = [
    ("515", "missiles and drones fired at Ukraine overnight", "ISW"),
    ("8", "killed in Kyiv as three bridges were hit", "Reuters"),
    ("300,000", "people evacuated ahead of Cyclone Akvan", "IMD"),
    ("-17%", "Taiwan stocks this week, worst since 1990", "Reuters"),
    ("$81bn", "Anthropic IPO, the largest ever", "Reuters"),
    ("100,000", "youth mobility places in the UK-EU deal", "Reuters"),
]

FEATURES = [
    {
        "kicker": "WAR IN UKRAINE",
        "title": "KYIV BRIDGES HIT",
        "body": ("Russia fired 515 missiles and drones at Ukraine overnight. "
                 "Three Dnipro bridges were damaged, 8 people were killed, "
                 "power was cut in 11 regions, and two missiles fell in Poland."),
        "date": "OVERNIGHT 19-20 NOV",
        "source": "ISW / Reuters",
        "scene": "kyiv",
    },
    {
        "kicker": "INDIA WEATHER",
        "title": "CYCLONE AKVAN LANDFALL",
        "body": ("Cyclone Akvan crossed the coast near Gopalpur, Odisha, with "
                 "winds of 80 km/h. More than 300,000 people were moved to safety "
                 "and 69 trains were cancelled. No major damage was reported."),
        "date": "MORNING 20 NOV",
        "source": "IMD",
        "scene": "akvan",
    },
    {
        "kicker": "MARKETS",
        "title": "AI SELLOFF",
        "body": ("Asian markets tumbled as faith in the AI boom cracked. The Nikkei "
                 "fell 5%, Seoul 5.7% and Taiwan 6.75%. Even Anthropic's record "
                 "$81bn IPO could not stop the slide."),
        "date": "20 NOV",
        "source": "Reuters",
        "scene": "selloff",
    },
]

REGIONS = [
    ("EUROPE", NAVY, [
        ("UK-EU reset deal",
         "Food trade, youth mobility, carbon link from 2028; 17bn pounds.",
         "Reuters"),
        ("Hungary lifts veto",
         "Budapest clears Ukraine's last two EU clusters, 4 and 5.",
         "Euronews"),
        ("7.9bn euros for Kyiv",
         "The EU sends Ukraine 7.9bn euros, plus 1bn more for arms.",
         "Kyiv24"),
        ("Aid refunds unblocked",
         "Hungary ends a two-year veto on EU aid refunds; 6.6bn released.",
         "The Gaze"),
        ("Merz rejects a new Yalta",
         "Merz: Europe will not accept a deal made over its head.",
         "Open Chronicle"),
    ]),
    ("ASIA", TEAL, [
        ("Three powers sign peace paper",
         "Trump, Xi and Putin issue a joint declaration in Shenzhen; no arms deal.",
         "Reuters"),
        ("Bloomberg reporter barred",
         "Annmarie Hordern is kept out after shouting a question at Trump.",
         "AP"),
        ("Xi hails ties turnaround",
         "Xi hails a 'full turnaround' after meeting Australia's Albanese.",
         "Reuters"),
        ("Humans to oversee military AI",
         "Washington and Beijing agree people must stay in charge of military AI.",
         "Reuters"),
        ("California probes Nvidia chips",
         "Inquiry into whether China improperly obtained Nvidia chips.",
         "CNBC"),
    ]),
    ("AMERICAS", (122, 54, 28), [
        ("US stocks slide",
         "The S&P 500 falls 2% and the Nasdaq 2.3% as the AI sell-off deepens.",
         "Reuters"),
        ("34 killed in Haiti",
         "Police say 34 suspected gang members were killed in an operation.",
         "Open Chronicle"),
        ("Chemicals fuel cartel",
         "US embassy: Chinese chemicals feed the Sinaloa cartel.",
         "Standard Topic"),
        ("Colombia strike warning",
         "President warns of state action against strike blockades.",
         "Reuters"),
        ("Penalties for AI centres abroad",
         "Trump floats fines for US firms that build AI data centres overseas.",
         "Standard Topic"),
    ]),
    ("MIDDLE EAST", (96, 60, 120), [
        ("US blockade of Iran holds",
         "US Navy blocks Iranian shipping; Tehran threatens Gulf oil.",
         "Standard Topic"),
        ("Carrier leaves the Gulf",
         "USS George Washington pulls out of the Gulf.",
         "Reuters"),
        ("COP31 talks stall",
         "Antalya talks deadlock over fossil fuels in the draft deal.",
         "Standard Topic"),
        ("16 nations back UK measures",
         "Arab and Islamic states back UK-Australia measures on Israel.",
         "Reuters"),
        ("Women blocked from care",
         "UN: Taliban curbs stop Afghan women reaching medical help.",
         "UN News"),
    ]),
    ("MARKETS", (146, 90, 8), [
        ("Nikkei down 5%",
         "SoftBank plunges 14.6% as Japan's market slides.",
         "Morningstar"),
        ("Kospi down 5.7%",
         "Samsung falls 7.1% and SK Hynix 6.6% in Seoul.",
         "Morningstar"),
        ("Taiwan's worst week since 1990",
         "The Taiex sinks 6.75% in a day and 17% in the week.",
         "Reuters"),
        ("Worst week since 2020",
         "MSCI's Asia-Pacific gauge is down 8% for the week.",
         "Reuters"),
    ]),
    ("TECH", (10, 80, 110), [
        ("Anthropic's $81bn debut",
         "The Claude maker raises the largest IPO ever; shares close 17% higher.",
         "Reuters"),
        ("Nvidia results fail to calm",
         "Blowout earnings fail to restore faith in the AI trade.",
         "Reuters"),
        ("China kept to older chips",
         "Beijing gets only earlier-generation chips, including H200.",
         "Reuters"),
        ("Tech ETF in bear market",
         "The sector fund is 20% below its October peak.",
         "Morningstar"),
    ]),
    ("WORLD", (60, 90, 60), [
        ("NZ pay equity ruling",
         "Overhaul breached women's rights; 33 claims, 180,000 workers.",
         "1News"),
        ("Myanmar guilty of genocide",
         "UN court: Myanmar guilty of genocide against the Rohingya.",
         "Open Chronicle"),
        ("Ukraine retakes 14 villages",
         "Kyiv says its forces liberated 14 settlements in the Kharkiv region.",
         "Meanwhile in Ukraine"),
        ("Car-trafficking crackdown",
         "A worldwide operation seizes 2,393 vehicles and arrests 688 people.",
         "Reuters"),
    ]),
]

DATE_CHECK = ("DATE CHECK - Every story on this page happened, or was first reported, on "
              "Friday 20 November 2026. Kyiv: overnight 19-20 Nov, reported 20 Nov. "
              "Shenzhen declaration: signed 19 Nov, published 20 Nov. NZ ruling: handed "
              "down 19 Nov, reported 20 Nov. Akvan: landfall on the morning of 20 Nov.")

# ------------------------------------------------------- illustrations
# 13 drawn illustrations: 3 feature scenes, 7 region banners, 3 spots.
# All shapes are drawn with Pillow primitives, no photos, no copied art.

def burst(d, cx, cy, r, colour):
    """Starburst explosion: rays plus a bright core."""
    for ang in range(0, 360, 15):
        a = math.radians(ang)
        x2 = cx + r * math.cos(a)
        y2 = cy + r * math.sin(a)
        d.line([cx, cy, x2, y2], fill=colour, width=3)
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
              fill=(255, 214, 90))
    d.ellipse([cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2],
              fill=(255, 240, 180))


def scene_kyiv(d, x, y, w, h):
    """Night over the Dnipro: bridge towers, blasts, smoke, searchlight."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    rnd = random.Random(7)
    for _ in range(46):
        sx = x + rnd.randrange(w)
        sy = y + rnd.randrange(int(h * 0.5))
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 225, 240))
    d.polygon([(x + w * 0.62, y + h * 0.30), (x + w * 0.78, y + h * 0.52),
               (x + w * 0.94, y + h * 0.34)], fill=(255, 244, 200))
    # river
    d.rectangle([x, y + int(h * 0.68), x + w, y + h], fill=(24, 48, 84))
    for i in range(6):
        yy = y + int(h * 0.72) + i * 6
        d.line([x + 8, yy, x + w - 8, yy], fill=(70, 110, 160), width=2)
    # bridge deck and towers
    deck = y + int(h * 0.62)
    d.rectangle([x, deck, x + w, deck + 7], fill=(8, 10, 16))
    for tx in (0.22, 0.55, 0.84):
        bx = x + int(w * tx)
        d.rectangle([bx - 4, deck - 58, bx + 4, deck], fill=(8, 10, 16))
        d.line([bx - 4, deck - 58, x + int(w * (tx - 0.16)), deck],
               fill=(120, 130, 150), width=2)
        d.line([bx + 4, deck - 58, x + int(w * (tx + 0.16)), deck],
               fill=(120, 130, 150), width=2)
    # blasts above the deck
    burst(d, x + int(w * 0.30), y + int(h * 0.30), 26, (255, 140, 40))
    burst(d, x + int(w * 0.68), y + int(h * 0.20), 20, (255, 120, 30))
    burst(d, x + int(w * 0.88), y + int(h * 0.42), 15, (255, 160, 60))
    # smoke columns: small, pale, hugging the deck
    for sx, sw in ((0.28, 15), (0.66, 12), (0.86, 10)):
        cx = x + int(w * sx)
        d.ellipse([cx - sw, deck - 34, cx + sw, deck - 12],
                  fill=(118, 122, 136))
        d.ellipse([cx - sw + 6, deck - 26, cx + sw + 2, deck - 8],
                  fill=(96, 100, 114))


def scene_akvan(d, x, y, w, h):
    """Cyclone spiral over the Bay of Bengal, coast and bending palms."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 60, 84))
    # sea
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(8, 90, 110))
    for i in range(5):
        yy = y + int(h * 0.60) + i * 9
        d.arc([x - 30, yy - 8, x + w + 30, yy + 14], 200, 340,
              fill=(140, 210, 225), width=3)
    # spiral cloud bands
    cx, cy = x + int(w * 0.42), y + int(h * 0.34)
    for k in range(5):
        r = 14 + k * 13
        d.arc([cx - r, cy - r, cx + r, cy + r], 20 + k * 40, 200 + k * 40,
              fill=(240, 246, 250), width=9)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(30, 40, 60))
    # coastline
    d.polygon([(x + int(w * 0.62), y + h), (x + w, y + h), (x + w, y + int(h * 0.52)),
               (x + int(w * 0.74), y + int(h * 0.58))], fill=(196, 164, 110))
    # bending palms on the coast
    for px, lean in ((0.70, -14), (0.80, -10), (0.90, -16)):
        bx = x + int(w * px)
        by = y + int(h * 0.60)
        d.line([bx, by, bx + lean, by - 34], fill=(60, 50, 30), width=4)
        for ang in range(-70, 71, 35):
            a = math.radians(ang)
            d.line([bx + lean, by - 34,
                    bx + lean + int(20 * math.cos(a)),
                    by - 34 + int(12 * math.sin(a)) - 8],
                   fill=(30, 120, 60), width=3)
    # rain streaks
    for i in range(26):
        rx = x + 10 + (i * 23) % (w - 20)
        ry = y + 8 + (i * 17) % int(h * 0.5)
        d.line([rx, ry, rx - 5, ry + 12], fill=(180, 220, 235), width=2)


def scene_selloff(d, x, y, w, h):
    """Plunging red chart, a chip and falling bars."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 26, 34))
    # grid
    for i in range(1, 5):
        gy = y + int(h * i / 5)
        d.line([x + 8, gy, x + w - 8, gy], fill=(52, 56, 68), width=1)
    # falling bars
    bars = [0.42, 0.55, 0.38, 0.66, 0.52, 0.78, 0.62, 0.88]
    bw = (w - 24) / len(bars)
    for i, frac in enumerate(bars):
        bx = x + 12 + i * bw
        bh = int(h * frac)
        d.rectangle([bx + 2, y + h - 12 - bh, bx + bw - 2, y + h - 12],
                    fill=(176, 30, 36) if i >= 5 else (200, 90, 80))
    # plunging line with arrowhead
    pts = [(x + 12, y + int(h * 0.22)), (x + int(w * 0.30), y + int(h * 0.34)),
           (x + int(w * 0.52), y + int(h * 0.30)), (x + int(w * 0.72), y + int(h * 0.55)),
           (x + w - 14, y + int(h * 0.82))]
    d.line(pts, fill=(255, 80, 70), width=5)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 16, ey - 4), (ex - 6, ey - 16)], fill=(255, 80, 70))
    # chip in the corner
    cx, cy = x + int(w * 0.80), y + int(h * 0.20)
    d.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], fill=(40, 90, 120),
                outline=(140, 210, 225), width=3)
    d.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(20, 50, 70))
    for dx in (-26, 26):
        for k in (-14, 0, 14):
            d.line([cx + dx, cy + k, cx + dx + (10 if dx > 0 else -10), cy + k],
                   fill=(140, 210, 225), width=3)


SCENES = {"kyiv": scene_kyiv, "akvan": scene_akvan, "selloff": scene_selloff}


def banner_europe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(29, 53, 87))
    cx, cy = x + w // 2, y + h // 2
    for k in range(12):
        a = math.radians(k * 30)
        sx, sy = cx + int(26 * math.cos(a)), cy + int(15 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 214, 90))
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))


def banner_asia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 94, 90))
    cx = x + w // 2
    d.ellipse([cx - 11, y + 6, cx + 11, y + 28], fill=(255, 120, 80))
    for i, ww in enumerate((44, 36, 28)):
        yy = y + 26 + i * 6
        d.rectangle([cx - ww // 2, yy, cx + ww // 2, yy + 3], fill=(20, 40, 40))
    d.rectangle([cx - 3, y + 26, cx + 3, y + h - 2], fill=(20, 40, 40))


def banner_americas(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(122, 54, 28))
    base = y + h - 4
    for i, bh in enumerate((16, 26, 20, 32, 24)):
        bx = x + 8 + i * 24
        d.rectangle([bx, base - bh, bx + 18, base], fill=(250, 240, 210))
        d.rectangle([bx + 5, base - bh - 6, bx + 13, base - bh], fill=(250, 240, 210))
    d.ellipse([x + w - 26, y + 4, x + w - 10, y + 20], fill=(255, 214, 90))


def banner_mideast(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 60, 120))
    cx = x + w // 2
    d.pieslice([cx - 16, y + 10, cx + 16, y + 42], 180, 360, fill=(255, 214, 90))
    d.rectangle([cx - 2, y + 4, cx + 2, y + 14], fill=(255, 214, 90))
    d.rectangle([x + 12, y + h - 8, x + w - 12, y + h - 2], fill=(230, 220, 200))
    d.rectangle([x + w - 34, y + 8, x + w - 30, y + h - 8], fill=(230, 220, 200))
    d.ellipse([x + w - 38, y + 2, x + w - 26, y + 10], fill=(230, 220, 200))


def banner_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(146, 90, 8))
    vals = [0.5, 0.72, 0.42, 0.85, 0.6]
    bw = (w - 16) / len(vals)
    for i, frac in enumerate(vals):
        bx = x + 8 + i * bw
        bh = int((h - 10) * frac)
        d.rectangle([bx + 3, y + h - 5 - bh, bx + bw - 3, y + h - 5],
                    fill=(255, 240, 200))
    d.line([x + 8, y + 10, x + w - 8, y + h - 12], fill=(176, 30, 36), width=3)


def banner_tech(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 80, 110))
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([cx - 14, cy - 14, cx + 14, cy + 14], fill=(20, 50, 70),
                outline=(140, 210, 225), width=2)
    d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], fill=(140, 210, 225))
    for dx, dy in ((-22, 0), (22, 0), (0, -14), (0, 14)):
        d.line([cx + dx, cy + dy, cx + (dx * 2 if dx else 0) + (14 if dx > 0 else -14 if dx < 0 else 0),
                cy + (dy * 2 if dy else 0) + (10 if dy > 0 else -10 if dy < 0 else 0)],
               fill=(140, 210, 225), width=2)


def banner_world(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 90, 60))
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 16, cy - 14, cx + 16, cy + 14], fill=(90, 140, 190),
              outline=(220, 235, 240), width=2)
    d.arc([cx - 16, cy - 8, cx + 16, cy + 8], 0, 360, fill=(220, 235, 240), width=1)
    d.line([cx - 16, cy, cx + 16, cy], fill=(220, 235, 240), width=1)
    d.arc([cx - 7, cy - 14, cx + 7, cy + 14], 0, 360, fill=(220, 235, 240), width=1)


BANNERS = {"EUROPE": banner_europe, "ASIA": banner_asia,
           "AMERICAS": banner_americas, "MIDDLE EAST": banner_mideast,
           "MARKETS": banner_markets, "TECH": banner_tech, "WORLD": banner_world}


def spot_bridge(d, x, y, s):
    """Small bridge spot illustration (Europe column)."""
    d.line([x, y + s - 6, x + s, y + s - 6], fill=INK, width=3)
    for fx in (0.25, 0.5, 0.75):
        bx = x + int(s * fx)
        d.line([bx, y + 4, bx, y + s - 6], fill=INK, width=2)
        d.line([bx, y + 4, x + int(s * (fx - 0.2)), y + s - 6], fill=GREY, width=1)
        d.line([bx, y + 4, x + int(s * (fx + 0.2)), y + s - 6], fill=GREY, width=1)


def spot_scales(d, x, y, s):
    """Small scales of justice spot illustration (World column)."""
    d.line([x + s // 2, y + 2, x + s // 2, y + s - 4], fill=INK, width=3)
    d.line([x + 4, y + 6, x + s - 4, y + 6], fill=INK, width=3)
    for side in (0, 1):
        px = x + 6 + side * (s - 12)
        d.line([px, y + 6, px, y + s - 10], fill=INK, width=2)
        d.pieslice([px - 9, y + s - 12, px + 9, y + s - 2], 0, 180, fill=GOLD)
    d.line([x + s // 2 - 8, y + s - 4, x + s // 2 + 8, y + s - 4], fill=INK, width=3)


def spot_chip(d, x, y, s):
    """Small chip spot illustration (Tech column)."""
    d.rectangle([x + 6, y + 6, x + s - 6, y + s - 6], fill=(10, 80, 110),
                outline=(20, 50, 70), width=2)
    d.rectangle([x + s // 2 - 5, y + s // 2 - 5, x + s // 2 + 5, y + s // 2 + 5],
                fill=(140, 210, 225))
    for k in (-1, 0, 1):
        d.line([x + 6, y + s // 2 + k * 8, x, y + s // 2 + k * 8], fill=INK, width=2)
        d.line([x + s - 6, y + s // 2 + k * 8, x + s, y + s // 2 + k * 8],
               fill=INK, width=2)


SPOTS = {"EUROPE": spot_bridge, "TECH": spot_chip, "WORLD": spot_scales}

# ------------------------------------------------------- layout

def draw_masthead(d):
    y = 12
    f_title = font(FONT_B, 46)
    f_date = font(FONT_B, 25)
    f_sub = font(FONT_R, 16)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, y), title, font=f_title, fill=INK)
    y += 56
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 6
    date = "FRIDAY 20 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    sub = "  |  35 STORIES FROM ONE DAY"
    d.text(((W - dw - d.textlength(sub, font=f_sub)) / 2, y), date,
           font=f_date, fill=RED)
    d.text(((W - dw - d.textlength(sub, font=f_sub)) / 2 + dw, y + 5), sub,
           font=f_sub, fill=INK)
    y += 34
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=3)
    return y + 8


def draw_strip(d, y):
    h = 62
    n = len(KEY_NUMBERS)
    gap = 6
    bw = (W - 2 * MARGIN - gap * (n - 1)) // n
    f_lab = font(FONT_R, 10)
    f_src = font(FONT_B, 9)
    for i, (num, label, src) in enumerate(KEY_NUMBERS):
        x = MARGIN + i * (bw + gap)
        d.rectangle([x, y, x + bw, y + h], fill=WHITE, outline=RULE, width=1)
        d.rectangle([x, y, x + bw, y + 4], fill=RED)
        sw = d.textlength(src, font=f_src)
        f_num = font(FONT_B, 27)
        while (d.textlength(num, font=f_num) + sw > bw - 16
               and f_num.size > 20):
            f_num = font(FONT_B, f_num.size - 1)
        d.text((x + 6, y + 8), num, font=f_num, fill=RED)
        d.text((x + bw - sw - 5, y + 10), src, font=f_src, fill=GREY)
        text_block(d, x + 6, y + 38, label, f_lab, bw - 12, leading=12,
                   max_lines=2)
    return y + h + 8


def draw_features(d, y):
    h = 272
    gap = 8
    pw = (W - 2 * MARGIN - gap * 2) // 3
    f_kick = font(FONT_B, 10)
    f_head = font(FONT_B, 19)
    f_body = font(FONT_R, 11)
    f_foot = font(FONT_B, 9)
    for i, feat in enumerate(FEATURES):
        x = MARGIN + i * (pw + gap)
        d.rectangle([x, y, x + pw, y + h], fill=WHITE, outline=RULE, width=1)
        SCENES[feat["scene"]](d, x + 1, y + 1, pw - 2, 138)
        ty = y + 146
        d.text((x + 8, ty), feat["kicker"], font=f_kick, fill=RED)
        ty += 14
        ty = text_block(d, x + 8, ty, feat["title"], f_head, pw - 16,
                        leading=21, max_lines=2)
        ty += 2
        ty = text_block(d, x + 8, ty, feat["body"], f_body, pw - 16,
                        leading=14, max_lines=4)
        foot = feat["date"] + "  -  " + feat["source"]
        d.text((x + 8, y + h - 16), foot, font=f_foot, fill=GREY)
    return y + h + 8


def draw_regions(d, y):
    top = y
    n = len(REGIONS)
    gap = 6
    cw = (W - 2 * MARGIN - gap * (n - 1)) // n
    f_name = font(FONT_B, 12)
    f_head = font(FONT_B, 12)
    f_body = font(FONT_R, 10)
    f_foot = font(FONT_B, 8)
    banner_h = 42
    name_h = 20
    grid_h = 474
    for i, (name, colour, items) in enumerate(REGIONS):
        x = MARGIN + i * (cw + gap)
        BANNERS[name](d, x, y, cw, banner_h)
        d.rectangle([x, y + banner_h, x + cw, y + banner_h + name_h],
                    fill=colour)
        nw = d.textlength(name, font=f_name)
        d.text((x + (cw - nw) / 2, y + banner_h + 3), name, font=f_name,
               fill=WHITE)
        iy = y + banner_h + name_h + 6
        spot_room = 30 if name in SPOTS else 0
        item_h = (grid_h - banner_h - name_h - 6 - spot_room) // len(items)
        for j, (head, body, src) in enumerate(items):
            by = iy + j * item_h
            if j:
                d.line([x + 2, by - 3, x + cw - 2, by - 3], fill=(210, 204, 190),
                       width=1)
            hy = text_block(d, x + 2, by, head, f_head, cw - 4, leading=14,
                            max_lines=2)
            by2 = text_block(d, x + 2, hy + 1, body, f_body, cw - 4,
                             leading=12, max_lines=3)
            foot = "20 NOV - " + src
            d.text((x + 2, by + item_h - 13), foot, font=f_foot, fill=GREY)
        if name in SPOTS:
            SPOTS[name](d, x + cw - 34, y + grid_h - 29, 28)
    return top + grid_h + 8


def draw_datecheck(d, y):
    h = 44
    d.rectangle([MARGIN, y, W - MARGIN, y + h], fill=(232, 226, 208),
                outline=RULE, width=1)
    f = font(FONT_R, 11)
    text_block(d, MARGIN + 8, y + 5, DATE_CHECK, f, W - 2 * MARGIN - 16,
               leading=14, max_lines=3)
    return y + h


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = draw_masthead(d)
    y = draw_strip(d, y)
    y = draw_features(d, y)
    y = draw_regions(d, y)
    y = draw_datecheck(d, y)
    f_foot = font(FONT_R, 9)
    note = ("Drawn and written by an AI agent for the make.fun "
            "news-image-20261120 bounty. All figures attributed to the sources named.")
    nw = d.textlength(note, font=f_foot)
    d.text(((W - nw) / 2, H - 14), note, font=f_foot, fill=GREY)
    grain(img)
    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print("wrote", OUT, img.size, size, "bytes")
    return size


if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news image (1024x576, BREAKING NEWS style).

Everything here is drawn fresh with PIL only. No external images, no network.
"""
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1024, 576

DARK_RED = (122, 10, 10)
RED = (158, 20, 20)
WHITE = (255, 255, 255)
CREAM = (255, 244, 224)
YELLOW = (255, 194, 26)
BLACK = (10, 4, 4)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def vgrad(size, top, bottom):
    w, h = size
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        col = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = col
    return img


def flame_layer(cx, base_y, scale):
    """A stylised flame cluster on its own RGBA layer."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - 150 * scale, base_y - 210 * scale,
               cx + 150 * scale, base_y + 30 * scale],
              fill=(255, 90, 0, 90))
    for dx, dy, rx, ry, col in [
        (-70, -40, 95, 90, (255, 60, 0, 235)),
        (60, -55, 100, 100, (255, 80, 0, 235)),
        (0, -110, 110, 130, (255, 120, 0, 240)),
        (-35, -150, 70, 95, (255, 170, 0, 245)),
        (35, -165, 65, 90, (255, 190, 0, 245)),
        (0, -195, 55, 90, (255, 220, 60, 250)),
    ]:
        d.ellipse([cx + dx * scale - rx * scale, base_y + dy * scale - ry * scale,
                   cx + dx * scale + rx * scale, base_y + dy * scale + ry * scale],
                  fill=col)
    for dx, hgt, wd in [(-55, 70, 26), (-12, 95, 30), (38, 80, 24), (75, 55, 20)]:
        tip_x = cx + dx * scale
        tip_y = base_y - (205 + hgt) * scale
        d.polygon([(tip_x - wd * scale, base_y - 150 * scale),
                   (tip_x, tip_y),
                   (tip_x + wd * scale, base_y - 150 * scale)],
                  fill=(255, 150, 0, 245))
    # a few red outer licks for depth
    for dx, hgt, wd in [(-95, 45, 22), (95, 40, 20)]:
        tip_x = cx + dx * scale
        tip_y = base_y - (150 + hgt) * scale
        d.polygon([(tip_x - wd * scale, base_y - 110 * scale),
                   (tip_x, tip_y),
                   (tip_x + wd * scale, base_y - 110 * scale)],
                  fill=(255, 60, 0, 235))
    return layer


def smoke_layer():
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    puffs = [(250, 100, 80), (330, 82, 95), (430, 95, 85), (520, 80, 95),
             (620, 98, 80), (700, 85, 90), (180, 125, 70), (790, 115, 75)]
    for x, y, r in puffs:
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=(60, 55, 55, 150))
        d.ellipse([x - r * 0.6, y - r * 0.5, x + r * 0.6, y + r * 0.5],
                  fill=(90, 82, 80, 130))
    return layer.filter(ImageFilter.GaussianBlur(14))


def skyline(draw, base_y, colour):
    random.seed(11)
    x = 0
    while x < W:
        bw = random.randint(34, 78)
        bh = random.randint(24, 68)
        draw.rectangle([x, base_y - bh, x + bw, base_y], fill=colour)
        for _ in range(bh // 14):
            wx = x + random.randint(4, max(5, bw - 8))
            wy = base_y - random.randint(8, max(9, bh - 6))
            draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 200, 90))
        x += bw + random.randint(2, 10)


def main():
    img = Image.new("RGB", (W, H), DARK_RED)
    draw = ImageDraw.Draw(img)

    # ---- header band: 0-64 --------------------------------------------
    draw.rectangle([0, 0, W, 64], fill=(70, 4, 4))
    draw.rectangle([0, 64, W, 68], fill=YELLOW)
    f_head = font(FONT_BOLD, 42)
    draw.text((24, 10), "BREAKING NEWS", font=f_head, fill=WHITE)
    f_date = font(FONT_BOLD, 20)
    date_txt = "THURSDAY 26 NOVEMBER 2026"
    dw = draw.textlength(date_txt, font=f_date)
    draw.ellipse([W - 24 - dw - 26, 24, W - 24 - dw - 12, 38], fill=(255, 40, 40))
    draw.text((W - 24 - dw, 20), date_txt, font=f_date, fill=YELLOW)

    # ---- hero scene: 68-250 -------------------------------------------
    hero = vgrad((W, 182), (16, 8, 14), (120, 30, 8))
    img.paste(hero, (0, 68))
    draw = ImageDraw.Draw(img)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([320, 50, 740, 280], fill=(255, 110, 0, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)
    img.paste(Image.alpha_composite(img.convert("RGBA"), smoke_layer()).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)
    flames = flame_layer(512, 238, 0.72).filter(ImageFilter.GaussianBlur(1.2))
    img.paste(Image.alpha_composite(img.convert("RGBA"), flames).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)
    skyline(draw, 240, (24, 6, 6))
    draw.rectangle([0, 240, W, 250], fill=(30, 8, 8))
    draw.rectangle([0, 244, W, 246], fill=YELLOW)

    # overturned tanker silhouette in front of the flames
    tx, ty = 438, 216
    draw.rounded_rectangle([tx, ty, tx + 140, ty + 20], radius=9, fill=(12, 3, 3))
    draw.rectangle([tx + 140, ty + 4, tx + 170, ty + 20], fill=(12, 3, 3))
    draw.rectangle([tx + 148, ty + 8, tx + 164, ty + 15], fill=(255, 200, 90))
    for wx in (tx + 20, tx + 108):
        draw.ellipse([wx, ty + 18, wx + 15, ty + 33], fill=(5, 2, 2))
    draw.ellipse([tx + 156, ty + 18, tx + 171, ty + 33], fill=(5, 2, 2))

    # location chip
    f_chip = font(FONT_BOLD, 17)
    chip = "CAIRO  •  GIZA RING ROAD"
    cw = draw.textlength(chip, font=f_chip) + 28
    draw.rounded_rectangle([24, 84, 24 + cw, 84 + 32], radius=6, fill=(0, 0, 0))
    draw.text((24 + 14, 90), chip, font=f_chip, fill=YELLOW)

    # ---- headline band: 250-326 ---------------------------------------
    draw.rectangle([0, 250, W, 326], fill=RED)
    draw.rectangle([0, 326, W, 330], fill=YELLOW)
    f_hl = font(FONT_BOLD, 44)
    draw.text((24, 256), "CAIRO TANKER FIRE KILLS 31", font=f_hl, fill=WHITE)
    f_sub = font(FONT_REG, 17)
    draw.text((26, 302),
              "Fuel tanker overturns and explodes on the Giza Ring Road — 27 vehicles charred",
              font=f_sub, fill=CREAM)

    # ---- stories grid: 340-508, 2 cols x 3 rows -----------------------
    stories = [
        ("KYIV  •  UKRAINE",
         "Missiles hit Kyiv overnight — 7 wounded. Ukraine says its “Blysk” laser "
         "downed a Russian drone, a first in combat."),
        ("RAS TANURA  •  SAUDI ARABIA",
         "Houthis claim a strike on Aramco’s Ras Tanura refinery. "
         "Oil climbs above $95 a barrel."),
        ("KUWAIT",
         "Drone attack kills two Italian technicians. Italy and Kuwait blame Iran, "
         "which denies it."),
        ("NEW YORK  •  USA",
         "The 100th Macy’s Thanksgiving Day Parade is postponed to Saturday by a "
         "storm — a first in 100 years."),
        ("SPACE  •  FCC",
         "The FCC authorises SpaceX’s “Starmind” — approval for one million orbital "
         "data-centre satellites."),
    ]
    f_kick = font(FONT_BOLD, 15)
    f_body = font(FONT_REG, 15)
    grid_left, grid_top = 24, 340
    col_w = (W - 48 - 28) // 2
    row_pitch = 57
    positions = [(grid_left, grid_top),
                 (grid_left, grid_top + row_pitch),
                 (grid_left, grid_top + 2 * row_pitch),
                 (grid_left + col_w + 28, grid_top),
                 (grid_left + col_w + 28, grid_top + row_pitch)]
    for (kick, body), (sx, sy) in zip(stories, positions):
        draw.rectangle([sx, sy, sx + 6, sy + 12], fill=YELLOW)
        draw.text((sx + 12, sy - 3), kick, font=f_kick, fill=YELLOW)
        lines = wrap(draw, body, f_body, col_w - 12)
        for i, ln in enumerate(lines[:2]):
            draw.text((sx + 12, sy + 17 + i * 19), ln, font=f_body, fill=WHITE)
    # sixth cell: paper flag box
    bx, by = grid_left + col_w + 28, grid_top + 2 * row_pitch
    draw.rectangle([bx, by, bx + col_w, by + 50], outline=YELLOW, width=2)
    f_box = font(FONT_BOLD, 16)
    draw.text((bx + 14, by + 7), "THE WORLD TODAY", font=f_box, fill=WHITE)
    f_box2 = font(FONT_REG, 14)
    draw.text((bx + 14, by + 30), "Six stories from Thursday 26 November 2026",
              font=f_box2, fill=CREAM)

    # ---- ticker strip: 512-576 ----------------------------------------
    draw.rectangle([0, 512, W, H], fill=BLACK)
    draw.rectangle([0, 512, W, 514], fill=YELLOW)
    f_tick = font(FONT_BOLD, 18)
    ticker = ("US TARIFFS ON 14 PARTNERS   •   UK NET MIGRATION 77,000   •   "
              "ECB PICKS HERNANDEZ DE COS   •   DR CONGO EBOLA PASSES 12,000   •   "
              "DIESEL TANKER CAPSIZES OFF IBIZA, 1 DEAD")
    tw = draw.textlength(ticker, font=f_tick)
    if tw <= W - 48:
        draw.text((24, 530), ticker, font=f_tick, fill=WHITE)
    else:
        mid = ticker.find("•", len(ticker) // 2)
        part1, part2 = ticker[:mid].strip(), ticker[mid + 1:].strip()
        for i, part in enumerate((part1, part2)):
            pw = draw.textlength(part, font=f_tick)
            draw.text(((W - pw) / 2, 520 + i * 24), part, font=f_tick, fill=WHITE)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()

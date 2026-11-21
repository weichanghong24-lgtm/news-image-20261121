#!/usr/bin/env python3
"""Render the 21 November 2026 world-news poster (1024x1024 PNG).

Fresh generator written for the make.fun news-image-20261121 bounty.
News verified from reporting published 21 Nov 2026 (One Turn day brief,
NYT, AP, Xinhua, SCMP, The Peninsula). Run: python3 build_image.py entry.png
"""
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (246, 241, 231)      # paper
INK = (26, 26, 26)        # near-black
RED = (163, 22, 33)       # accent red
GREY = (90, 86, 78)
RULE = (26, 26, 26)
LIGHT = (233, 226, 210)   # panel fill

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=6):
    """Draw wrapped paragraph; return y after last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def main(out_path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 40  # margin
    x0, x1 = mx, W - mx

    # ---- Masthead ----
    y = 34
    d.line([(x0, y), (x1, y)], fill=RULE, width=4)
    y += 14
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF, 58)
    d.text(((W - d.textlength(title, font=tf)) / 2, y), title, font=tf, fill=INK)
    y += 72
    sub = "Saturday, 21 November 2026  ·  The day's world news in one image"
    sf = font(SERIF_R, 24)
    d.text(((W - d.textlength(sub, font=sf)) / 2, y), sub, font=sf, fill=GREY)
    y += 40
    d.line([(x0, y), (x1, y)], fill=RULE, width=4)
    y += 18

    # ---- Lead story: markets ----
    lead_top = y
    d.rectangle([x0, y, x1, y + 196], fill=INK)
    ly = y + 16
    kf = font(SANS_B, 20)
    d.text((x0 + 22, ly), "LEAD  ·  MARKETS", font=kf, fill=(232, 180, 60))
    ly += 34
    hf = font(SERIF, 40)
    d.text((x0 + 22, ly), "AI sell-off sweeps world markets", font=hf, fill=(250, 248, 242))
    ly += 56
    bf = font(SANS, 22)
    lead_body = ("Fears that heavy AI spending will not pay off drove a broad sell-off. "
                 "The S&P 500 fell 3.7% on Friday and Japan's Nikkei fell 5.06%, "
                 "with the rout spreading across Asia and Europe.")
    for line in wrap(d, lead_body, bf, x1 - x0 - 44):
        d.text((x0 + 22, ly), line, font=bf, fill=(225, 222, 214))
        ly += 30
    y = lead_top + 196 + 20

    # ---- 2x2 grid ----
    stories = [
        ("MEXICO", "Cartel boss captured",
         "Troops seized Fausto Isidro Meza Flores, known as \u201cEl Chapo "
         "Isidro\u201d, in Guasave, Sinaloa. The FBI most-wanted fugitive's "
         "arrest was followed by violence."),
        ("UKRAINE", "Missile hits Zelenskyy's hometown",
         "A Russian missile struck central Kryvyi Rih, killing two and "
         "wounding 60. Russia fired 3 missiles and 148 drones overnight."),
        ("CLIMATE  ·  COP31", "Talks run past deadline",
         "The climate summit in Antalya, Turkey, overran its Friday deadline "
         "as talks stalled over fossil fuels and the fight over energy "
         "resources."),
        ("IRAN", "Trump weighs new strikes",
         "President Trump is weighing another round of extensive strikes as "
         "Israel presses for quick action. He also said Iran wants a deal but "
         "rejects US terms."),
    ]
    col_w = (x1 - x0 - 24) // 2
    row_h = 178
    gy = y
    for i, (kick, head, body) in enumerate(stories):
        cx = x0 + (i % 2) * (col_w + 24)
        cy = gy + (i // 2) * (row_h + 16)
        d.rectangle([cx, cy, cx + col_w, cy + row_h], outline=RULE, width=2)
        d.rectangle([cx, cy, cx + col_w, cy + 34], fill=LIGHT)
        d.text((cx + 14, cy + 7), kick, font=font(SANS_B, 17), fill=RED)
        hy = cy + 46
        for line in wrap(d, head, font(SERIF, 24), col_w - 28):
            d.text((cx + 14, hy), line, font=font(SERIF, 24), fill=INK)
            hy += 30
        by = hy + 6
        for line in wrap(d, body, font(SANS, 18), col_w - 28):
            d.text((cx + 14, by), line, font=font(SANS, 18), fill=INK)
            by += 23
    y = gy + 2 * row_h + 16 + 12

    # ---- UK-EU strip ----
    d.line([(x0, y), (x1, y)], fill=RULE, width=2)
    y += 10
    d.text((x0, y), "BRITAIN & EUROPE", font=font(SANS_B, 18), fill=RED)
    y += 26
    y = para(d, x0, y, x1 - x0,
             "UK and EU strike landmark deal to rebuild ties: agri-food trade "
             "eased, carbon markets linked, youth mobility restored.",
             font(SERIF, 24), leading=2)
    y += 8
    d.line([(x0, y), (x1, y)], fill=RULE, width=2)
    y += 12

    # ---- Also band ----
    d.text((x0, y), "ALSO", font=font(SANS_B, 18), fill=RED)
    y += 26
    also = ("M7.2 quake hits Indonesia's Maluku  ·  Brazil trial: dengue cases "
            "down 69%  ·  BepiColombo reaches Mercury orbit after 8 years  ·  "
            "Trump threatens \u201ctremendous tax\u201d on US firms building data "
            "centres abroad")
    y = para(d, x0, y, x1 - x0, also, font(SANS, 18), fill=INK, leading=4)
    y += 6

    # ---- Footer ----
    d.line([(x0, H - 52), (x1, H - 52)], fill=RULE, width=2)
    foot = "Sources: One Turn day brief · NYT · AP · Xinhua · SCMP · The Peninsula — 21 Nov 2026"
    ff = font(SANS, 16)
    d.text(((W - d.textlength(foot, font=ff)) / 2, H - 40), foot, font=ff, fill=GREY)

    img.save(out_path, "PNG")
    print(f"wrote {out_path}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "entry.png")

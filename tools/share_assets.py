#!/usr/bin/env python3
"""Sharing assets: the social preview image (site/share.png, 1200x630) and one QR code per electorate page
(site/data/qr/<slug>.svg) for the printable one-pager. Run by tools/build_site.py; safe to run alone.
Design follows site/redesign/tokens.css: ink background, paper text, one magenta signal, the ballot-tick mark.
Fonts: the site uses Archivo/Public Sans from Google Fonts; those files are not available offline here, so the image
uses the system's DejaVu Sans Bold (closest open fallback). Swap FONT below if an Archivo TTF is added to the repo."""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
BASE_URL = 'https://not-simon.github.io/Politicsnz/'
INK, PAPER, SIGNAL, MUTED = (24, 26, 31), (250, 250, 251), (214, 36, 110), (160, 164, 173)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_R = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def share_image():
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), INK); d = ImageDraw.Draw(im)
    # ballot-tick mark (circle + tick), as in the brand mark
    cx, cy, r = 150, 150, 70
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=PAPER, width=12)
    d.line([(cx - 36, cy + 4), (cx - 4, cy + 36), (cx + 92, cy - 62)], fill=SIGNAL, width=22, joint='curve')
    big = ImageFont.truetype(FONT, 92); mid = ImageFont.truetype(FONT, 40); small = ImageFont.truetype(FONT_R, 30); micro = ImageFont.truetype(FONT_R, 24)
    d.text((260, 92), 'Ballot Book', font=big, fill=PAPER)
    d.text((262, 200), 'NZ election 2026', font=mid, fill=SIGNAL)
    d.text((80, 300), 'Independent and non-partisan.', font=mid, fill=PAPER)
    d.text((80, 352), 'It will never tell you how to vote.', font=mid, fill=PAPER)
    lines = ['How to vote and who is standing where you live · every party, policy and promise', 'Polls, the electorate map since 2011 and results on the night · 7 November 2026']
    for i, t in enumerate(lines): d.text((80, 440 + i * 42), t, font=small, fill=MUTED)
    d.text((80, 560), 'not-simon.github.io/Politicsnz', font=micro, fill=PAPER)
    d.rectangle((0, H - 10, W, H), fill=SIGNAL)
    im.save(SITE / 'share.png', optimize=True)
    return SITE / 'share.png'

def qr_codes():
    try: import qrcode, qrcode.image.svg
    except ImportError: print('qrcode not installed; skipping QR codes', file=sys.stderr); return 0
    e = json.load(open(ROOT / 'data' / 'electorates' / '2026.json')); E = e['electorates'] if isinstance(e, dict) else e
    out = SITE / 'data' / 'qr'; out.mkdir(parents=True, exist_ok=True); n = 0
    for x in E:
        url = f'{BASE_URL}#/vote/electorate/{x["slug"]}'
        img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2)
        img.save(out / f'{x["slug"]}.svg'); n += 1
    qrcode.make(BASE_URL, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2).save(out / 'site.svg')
    return n

if __name__ == '__main__':
    p = share_image(); n = qr_codes()
    print(f'{p} written; {n} electorate QR codes in site/data/qr/')

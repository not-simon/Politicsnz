#!/usr/bin/env python3
"""Download a Wikipedia lead image (Commons) to <dir>/photo.jpg (<=400px) and print licence metadata JSON.
Usage: python3 tools/people_others_photo.py <File name> <dest dir>   (does nothing if photo.jpg exists)"""
import sys, json, io, re, time, requests, html
from PIL import Image
UA = {"User-Agent": "PoliticsNZResearch/1.0 (personal research)"}
fname, dest = sys.argv[1], sys.argv[2]
def strip(s): return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
j = None
for a in range(15):
    try:
        r0 = requests.get("https://commons.wikimedia.org/w/api.php", params={"action": "query", "titles": "File:" + fname,
            "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 400, "format": "json", "formatversion": 2},
            headers=UA, timeout=60)
        if r0.status_code == 429: time.sleep(20 + 10 * a); continue
        j = r0.json(); break
    except Exception: time.sleep(5 + 5 * a)
if not j: sys.exit("meta fail")
pg = j["query"]["pages"][0]
if "imageinfo" not in pg:  # maybe local enwiki file
    j = requests.get("https://en.wikipedia.org/w/api.php", params={"action": "query", "titles": "File:" + fname,
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 400, "format": "json", "formatversion": 2}, headers=UA, timeout=60).json()
    pg = j["query"]["pages"][0]
ii = pg["imageinfo"][0]; em = ii.get("extmetadata", {})
meta = {"photo": "photo.jpg", "photo_source": ii["descriptionurl"],
        "photo_credit": strip(em.get("Artist", {}).get("value")) or strip(em.get("Credit", {}).get("value")),
        "photo_license": strip(em.get("LicenseShortName", {}).get("value"))}
import os
out = os.path.join(dest, "photo.jpg")
if os.path.exists(out): meta["skipped"] = "photo exists"; print(json.dumps(meta)); sys.exit()
url = ii.get("thumburl") or ii["url"]
for a in range(15):
    try:
        r = requests.get(url, headers=UA, timeout=60)
        if r.status_code == 200: break
    except Exception: pass
    time.sleep(10 + 10 * a)
im = Image.open(io.BytesIO(r.content)).convert("RGB"); im.thumbnail((400, 400)); im.save(out, "JPEG", quality=82)
print(json.dumps(meta, ensure_ascii=False))

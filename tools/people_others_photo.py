#!/usr/bin/env python3
"""Download a Wikipedia lead image (Commons) to <dir>/photo.jpg (<=400px) and print licence metadata JSON.
Usage: python3 tools/people_others_photo.py <File name> <dest dir>   (does nothing if photo.jpg exists)
Uses the Commons file description page HTML (the MediaWiki API was rate-limited) and upload.wikimedia.org thumbnails.
The raw HTML is saved to raw/people/others/commons/ for the record."""
import sys, json, io, re, time, os, html, urllib.parse, requests
from PIL import Image
UA = {"User-Agent": "PoliticsNZResearch/1.0 (personal research)"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fname, dest = sys.argv[1].replace(" ", "_"), sys.argv[2]
def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
class R:
    def __init__(s, code, content, ctype): s.status_code, s.content, s.headers = code, content, {"content-type": ctype}
    @property
    def text(s): return s.content.decode("utf-8", "replace")
def get(url, tries=6):
    """curl is used because python-requests is throttled (429) by upload.wikimedia.org from this host."""
    import subprocess, tempfile
    for a in range(tries):
        with tempfile.NamedTemporaryFile() as tf:
            pr = subprocess.run(["curl", "-sS", "-L", "--max-time", "60", "-A", UA["User-Agent"], "-o", tf.name,
                                 "-w", "%{http_code} %{content_type}", url], capture_output=True, text=True)
            parts = (pr.stdout or "0 ").split(" ", 1)
            code = int(parts[0] or 0); ctype = parts[1] if len(parts) > 1 else ""
            if code in (200, 404): return R(code, open(tf.name, "rb").read(), ctype)
        time.sleep(15 + 15 * a)
    return None
page = None
for base in ("https://commons.wikimedia.org/wiki/File:", "https://en.wikipedia.org/wiki/File:"):
    url = base + urllib.parse.quote(fname)
    r = get(url)
    if r is not None and r.status_code == 200 and 'fullImageLink' in r.text: page = (url, r.text); break
if not page: sys.exit("file page fail")
desc, h = page
os.makedirs(os.path.join(ROOT, "raw/people/others/commons"), exist_ok=True)
open(os.path.join(ROOT, "raw/people/others/commons", re.sub(r"[^\w.-]", "_", fname) + ".html"), "w").write(h)
m = re.search(r'class="fullImageLink"[^>]*>\s*<a href="([^"]+)"', h)
orig = html.unescape(m.group(1)); orig = "https:" + orig if orig.startswith("//") else orig
au = re.search(r'id="fileinfotpl(?:_|&#95;)aut"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', h, re.S)
cr = re.search(r'id="fileinfotpl(?:_|&#95;)credit"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', h, re.S)
lic = re.search(r'class="licensetpl(?:_|&#95;)short"[^>]*>(.*?)</span>', h, re.S)
credit = strip(au.group(1)) if au else (strip(cr.group(1)) if cr else "")
credit = re.sub(r"\s*\(talk.*?\)", "", credit)[:200]
meta = {"photo": "photo.jpg", "photo_source": desc, "photo_credit": credit,
        "photo_license": strip(lic.group(1)) if lic else "see source"}
out = os.path.join(dest, "photo.jpg")
if os.path.exists(out): meta["skipped"] = "photo exists"; print(json.dumps(meta)); sys.exit()
p = urllib.parse.urlparse(orig).path  # /wikipedia/commons/a/ab/Name.jpg
parts = p.split("/"); name = parts[-1]
thumb = "https://upload.wikimedia.org" + "/".join(parts[:3]) + "/thumb/" + "/".join(parts[3:]) + "/500px-" + name
r = get(thumb, 3)
if r is None or r.status_code != 200 or not r.headers.get("content-type", "").startswith("image"):
    r = get(orig, 4)
if r is None or r.status_code != 200: sys.exit("image fail")
im = Image.open(io.BytesIO(r.content)).convert("RGB"); im.thumbnail((400, 400)); im.save(out, "JPEG", quality=82)
print(json.dumps(meta, ensure_ascii=False))

#!/usr/bin/env python3
"""Fetch Wikipedia pages for the elections area into raw/elections/.
Saves <Title>.wikitext (index.php?action=raw) and, with --html, <Title>.html (REST API rendered HTML).
Usage: python3 tools/elections_fetch.py [--html] [--force] "Page title" ...
"""
import sys, json, os, re, time, datetime, urllib.parse, requests
UA = {"User-Agent": "PoliticsNZResearch/1.0 (personal research)"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw", "elections")
os.makedirs(OUT, exist_ok=True)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
HTML, FORCE = "--html" in sys.argv, "--force" in sys.argv
def fn(t): return re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_")
def get(url):
    for attempt in range(6):
        r = requests.get(url, headers=UA, timeout=90)
        if r.status_code == 200: return r
        print("  retry", r.status_code, url); time.sleep(10 * (attempt + 1))
    return None
for title in args:
    base = os.path.join(OUT, fn(title))
    q = urllib.parse.quote(title.replace(" ", "_"))
    if FORCE or not os.path.exists(base + ".wikitext"):
        r = get(f"https://en.wikipedia.org/w/index.php?title={q}&action=raw")
        if r is None: print("FAIL", title); continue
        txt = r.text
        m = re.match(r"#REDIRECT\s*\[\[([^\]#]+)", txt, re.I)
        if m:
            print("  redirect ->", m.group(1)); q = urllib.parse.quote(m.group(1).replace(" ", "_"))
            txt = get(f"https://en.wikipedia.org/w/index.php?title={q}&action=raw").text
        open(base + ".wikitext", "w").write(txt)
        json.dump({"title": title, "url": "https://en.wikipedia.org/wiki/" + q,
                   "retrieved": datetime.date.today().isoformat()}, open(base + ".meta.json", "w"))
        print("OK wikitext", title, len(txt)); time.sleep(1)
    if HTML and (FORCE or not os.path.exists(base + ".html")):
        r = get(f"https://en.wikipedia.org/api/rest_v1/page/html/{q}")
        if r is None: print("FAIL html", title); continue
        open(base + ".html", "w").write(r.text); print("OK html", title, len(r.text)); time.sleep(1)

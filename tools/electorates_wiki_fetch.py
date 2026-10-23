#!/usr/bin/env python3
"""Fetch Wikipedia wikitext (index.php?action=raw) for electorate pages into raw/electorates/wiki/.
Usage: python3 tools/electorates_wiki_fetch.py "Title" ..."""
import sys, os, re, time, json, datetime, urllib.parse, requests
UA = {"User-Agent": "PoliticsNZResearch/1.0 (personal research)"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw", "electorates", "wiki")
os.makedirs(OUT, exist_ok=True)
def fn(t): return re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_")
def get(title):
    for a in range(5):
        r = requests.get("https://en.wikipedia.org/w/index.php", params={"title": title, "action": "raw"}, headers=UA, timeout=60)
        if r.status_code == 200: return r.text
        if r.status_code == 404: return None
        time.sleep(15 * (a + 1))
    return None
for t in sys.argv[1:]:
    p = os.path.join(OUT, fn(t) + ".wikitext")
    if os.path.exists(p): continue
    txt, title = get(t), t
    for _ in range(3):
        m = txt and re.match(r"#REDIRECT\s*\[\[([^\]#]+)", txt, re.I)
        if not m: break
        title = m.group(1); txt = get(title)
    if not txt: print("FAIL", t); continue
    open(p, "w").write(txt)
    json.dump({"title": title, "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
               "retrieved": datetime.date.today().isoformat()}, open(p[:-9] + ".meta.json", "w"))
    print("OK", t, "->", title, len(txt)); time.sleep(3)

#!/usr/bin/env python3
"""Batch-fetch wikitext + lead image for many Wikipedia titles (50/request), then plain-text extracts one at a time
with 429 back-off. Writes raw/people/others/wiki/<name>.{wikitext,txt,meta.json} like people_others_fetch.py.
Usage: python3 tools/people_others_batchfetch.py titles.txt"""
import sys, json, os, re, time, requests
UA = {"User-Agent": "PoliticsNZResearch/1.0 (personal research)"}
API = "https://en.wikipedia.org/w/api.php"
OUT = os.path.join(os.path.dirname(__file__), "..", "raw", "people", "others", "wiki")
def fn(t): return re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_")
def get(params):
    for a in range(30):
        try:
            r = requests.get(API, params={**params, "format": "json", "formatversion": 2}, headers=UA, timeout=90)
            if r.status_code == 429:
                w = int(r.headers.get("retry-after", "20") or 20); time.sleep(max(w, 15)); continue
            return r.json()
        except Exception as e:
            time.sleep(10)
    return None
titles = [l.strip() for l in open(sys.argv[1]) if l.strip()]
todo = [t for t in titles if not os.path.exists(os.path.join(OUT, fn(t)) + ".meta.json")]
print("todo", len(todo), flush=True)
for i in range(0, len(todo), 40):
    chunk = todo[i:i+40]
    j = get({"action": "query", "titles": "|".join(chunk), "prop": "revisions|pageimages|pageprops", "rvprop": "content|ids",
             "rvslots": "main", "piprop": "original|name", "redirects": 1})
    if not j: print("batch fail"); continue
    back = {}
    for n in j["query"].get("normalized", []) + j["query"].get("redirects", []):
        back[n["to"]] = back.get(n["from"], n["from"])
    for pg in j["query"]["pages"]:
        if "revisions" not in pg: print("MISSING", pg.get("title")); continue
        orig = back.get(pg["title"], pg["title"]); orig = back.get(orig, orig)
        base = os.path.join(OUT, fn(orig))
        rv = pg["revisions"][0]
        open(base + ".wikitext", "w").write(rv["slots"]["main"]["content"])
        json.dump({"title": pg["title"], "revid": rv["revid"], "url": "https://en.wikipedia.org/wiki/" + pg["title"].replace(" ", "_"),
                   "pageimage": pg.get("pageimage"), "original": pg.get("original"),
                   "wikibase_item": pg.get("pageprops", {}).get("wikibase_item")}, open(base + ".meta.json.tmp", "w"), indent=1)
        print("wt", orig, "->", pg["title"], flush=True)
    time.sleep(3)
for t in todo:
    base = os.path.join(OUT, fn(t))
    if not os.path.exists(base + ".meta.json.tmp"): continue
    m = json.load(open(base + ".meta.json.tmp"))
    j = get({"action": "query", "titles": m["title"], "prop": "extracts", "explaintext": 1})
    if not j: print("extract fail", t); continue
    open(base + ".txt", "w").write(j["query"]["pages"][0].get("extract", ""))
    os.rename(base + ".meta.json.tmp", base + ".meta.json"); print("OK", t, flush=True)
    time.sleep(4)

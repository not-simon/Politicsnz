#!/usr/bin/env python3
"""Fetch Wikipedia wikitext + plain-text extract + lead image info for person/parliament pages
into raw/people/others/. Usage: python3 tools/people_others_fetch.py "Title" ... [--force]"""
import sys, json, os, re, time, requests
UA = {"User-Agent": "PoliticsNZResearch/1.0 (personal research)"}
API = "https://en.wikipedia.org/w/api.php"
OUT = os.path.join(os.path.dirname(__file__), "..", "raw", "people", "others")
os.makedirs(OUT, exist_ok=True)
def fn(t): return re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_")
def get(params):
    for a in range(5):
        try:
            r = requests.get(API, params={**params, "format": "json", "formatversion": 2}, headers=UA, timeout=90)
            return r.json()
        except Exception as e:
            print("retry", e, file=sys.stderr); time.sleep(4 * (a + 1))
for title in [a for a in sys.argv[1:] if not a.startswith("--")]:
    base = os.path.join(OUT, fn(title))
    if os.path.exists(base + ".meta.json") and "--force" not in sys.argv:
        print("cached", title); continue
    j = get({"action": "parse", "page": title, "prop": "wikitext|revid", "redirects": 1})
    if not j or "error" in j: print("ERR", title, j and j["error"].get("info")); continue
    p = j["parse"]
    q = get({"action": "query", "titles": p["title"], "prop": "extracts|pageimages|pageprops", "explaintext": 1,
             "piprop": "original|name", "redirects": 1})
    pg = q["query"]["pages"][0]
    open(base + ".wikitext", "w").write(p["wikitext"])
    open(base + ".txt", "w").write(pg.get("extract", ""))
    json.dump({"title": p["title"], "revid": p["revid"], "url": "https://en.wikipedia.org/wiki/" + p["title"].replace(" ", "_"),
               "pageimage": pg.get("pageimage"), "original": pg.get("original"),
               "wikibase_item": pg.get("pageprops", {}).get("wikibase_item")}, open(base + ".meta.json", "w"), indent=1)
    print("OK", title, "->", p["title"], len(p["wikitext"]), pg.get("pageimage"))
    time.sleep(1)

#!/usr/bin/env python3
"""Fetch Wikipedia plain-text extracts for ACT / NZ First track-record research into raw/record/act-nzf/.
Usage: python3 tools/record_act_nzf_wiki.py "Page title" ..."""
import sys, json, os, re, time, requests
UA = {"User-Agent": "PoliticsNZResearch/1.0 (personal research)"}
API = "https://en.wikipedia.org/w/api.php"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw", "record", "act-nzf")
os.makedirs(OUT, exist_ok=True)
def fn(t): return re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_")
for title in sys.argv[1:]:
    base = os.path.join(OUT, fn(title))
    if os.path.exists(base + ".wikitext"): print("cached", title); continue
    j = None
    for attempt in range(6):
        try:
            r = requests.get(API, params={"action": "parse", "page": title, "prop": "wikitext|revid", "format": "json",
                                          "redirects": 1, "formatversion": 2}, headers=UA, timeout=90)
            j = r.json(); break
        except Exception as e:
            time.sleep(10 * (attempt + 1))
    if j is None: print("FAIL", title); continue
    time.sleep(4)
    if "error" in j: print("ERR", title, j["error"].get("info")); continue
    p = j["parse"]
    open(base + ".wikitext", "w").write(p["wikitext"])
    json.dump({"title": p["title"], "revid": p["revid"], "url": "https://en.wikipedia.org/wiki/" + p["title"].replace(" ", "_")}, open(base + ".meta.json", "w"))
    print("OK", title, "->", p["title"], len(p["wikitext"]))

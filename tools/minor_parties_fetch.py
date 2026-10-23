#!/usr/bin/env python3
"""Fetch Wikipedia articles (plain-text extract + wikitext + revid) for minor NZ parties.
Usage: python3 -I tools/minor_parties_fetch.py "Title 1" "Title 2" ...
Writes raw/minor-parties/wiki/<safe-title>.{txt,wikitext,meta.json}."""
import sys, json, os, re, time, urllib.request, urllib.parse, urllib.error
API = "https://en.wikipedia.org/w/api.php"
UA = {"User-Agent": "PoliticsNZResearch/1.0 (personal research)"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw", "minor-parties", "wiki")
os.makedirs(OUT, exist_ok=True)

def get(params):
    params.update({"format": "json", "formatversion": "2"})
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers=UA)
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(15 * (attempt + 1))
    raise RuntimeError("rate limited")

def fetch(title):
    d = get({"action": "query", "prop": "extracts|revisions", "explaintext": 1, "rvprop": "ids|content",
             "rvslots": "main", "titles": title, "redirects": 1})
    pages = d["query"]["pages"]
    p = pages[0]
    if p.get("missing"):
        print("MISSING", title); return
    safe = re.sub(r"[^A-Za-z0-9]+", "_", p["title"]).strip("_")
    rev = p["revisions"][0]
    open(os.path.join(OUT, safe + ".txt"), "w").write(p.get("extract", ""))
    open(os.path.join(OUT, safe + ".wikitext"), "w").write(rev["slots"]["main"]["content"])
    json.dump({"requested": title, "title": p["title"], "revid": rev["revid"],
               "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(p["title"].replace(" ", "_"))},
              open(os.path.join(OUT, safe + ".meta.json"), "w"))
    print("OK", title, "->", p["title"], len(p.get("extract", "")))

for title in sys.argv[1:]:
    time.sleep(1.5)
    done = {json.load(open(os.path.join(OUT, f))).get("requested") for f in os.listdir(OUT) if f.endswith(".meta.json")}
    if title in done:
        continue
    try:
        fetch(title)
    except Exception as e:
        print("FAIL", title, e)


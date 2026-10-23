#!/usr/bin/env python3
"""Fetch Wikipedia articles for minor NZ parties (wikitext via ?action=raw, rendered HTML -> plain text).
The api.php endpoint was rate-limiting (429) during this run, so the /wiki/ endpoints are used.
Usage: python3 -I tools/minor_parties_fetch.py "Title 1" "Title 2" ...
Writes raw/minor-parties/wiki/<Safe_Title>.{wikitext,html,txt,meta.json}. Skips titles already fetched."""
import sys, json, os, re, time, urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
UA = {"User-Agent": "PoliticsNZResearch/1.0 (personal research)"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw", "minor-parties", "wiki")
os.makedirs(OUT, exist_ok=True)


def get(url):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8"), r.geturl()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, None
            if e.code != 429:
                raise
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("rate limited")


def fetch(title):
    safe = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
    if os.path.exists(os.path.join(OUT, safe + ".html")):
        return
    base = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))
    raw, _ = get(base + "?action=raw")
    if raw is None:
        print("MISSING", title)
        return
    m = re.match(r"#REDIRECT\s*\[\[([^\]#|]+)", raw, re.I)
    if m:
        print("REDIRECT", title, "->", m.group(1))
        return fetch(m.group(1).strip())
    html, _ = get(base)
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("div", class_="mw-parser-output") or soup
    for bad in body.select("style, script, .reference, .mw-editsection, .navbox, .reflist, .metadata"):
        bad.decompose()
    text = re.sub(r"\n{3,}", "\n\n", body.get_text("\n"))
    open(os.path.join(OUT, safe + ".wikitext"), "w").write(raw)
    open(os.path.join(OUT, safe + ".html"), "w").write(html)
    open(os.path.join(OUT, safe + ".txt"), "w").write(text)
    rev = re.search(r'"wgRevisionId":(\d+)', html)
    json.dump({"title": title, "revid": int(rev.group(1)) if rev else None, "url": base,
               "retrieved": time.strftime("%Y-%m-%d")}, open(os.path.join(OUT, safe + ".meta.json"), "w"))
    print("OK", title, len(raw), flush=True)


for t in sys.argv[1:]:
    try:
        fetch(t)
        time.sleep(1)
    except Exception as e:
        print("FAIL", t, e, flush=True)

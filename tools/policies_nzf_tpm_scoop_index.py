#!/usr/bin/env python3
"""Crawl info.scoop.co.nz organisation pages for NZ First and Te Pati Maori and list their press releases.
Usage: python3 -I tools/policies_nzf_tpm_scoop_index.py  -> writes raw/party-docs/<party>/scoop_index.json"""
import json, re, subprocess, sys, time
from bs4 import BeautifulSoup
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36"
ORGS = {"nz-first": "New_Zealand_First_Party", "te-pati-maori": "Te_Pati_Maori"}
def get(url):
    return subprocess.run(["curl", "-sS", "-L", "-A", UA, "--max-time", "40", url], capture_output=True).stdout.decode("utf-8", "replace")
for party, org in ORGS.items():
    seen, out = set(), []
    for page in range(1, 40):
        url = f"https://info.scoop.co.nz/{org}" + ("" if page == 1 else f"/{page}")
        s = BeautifulSoup(get(url), "html.parser")
        # story list lives before the sidebar; take story links whose text isn't 'More >>'
        main = s.find_all("a", href=re.compile(r"scoop\.co\.nz/stories/"))
        new = 0
        for a in main:
            t = a.get_text(" ", strip=True); h = a["href"]
            if t.startswith("More") or h in seen: continue
            m = re.search(r"/stories/([A-Z]{2})(\d{2})(\d{2})/", h)
            if not m: continue
            # sidebar (latest headlines) items are truncated with '...' and appear on every page
            if t.endswith("...") : continue
            seen.add(h); out.append({"title": t, "url": h, "yymm": m.group(2)+m.group(3)}); new += 1
        yymms = [o["yymm"] for o in out]
        print(party, page, new, min(yymms) if yymms else None, file=sys.stderr)
        if new == 0 or (yymms and min(yymms) < "2601"): break
        time.sleep(1)
    json.dump(out, open(f"raw/party-docs/{party}/scoop_index.json", "w"), indent=1, ensure_ascii=False)

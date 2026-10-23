#!/usr/bin/env python3
"""Build data/polls-2026.json from raw/elections/Opinion_polling_for_the_2026_New_Zealand_general_election.html"""
import json, os, re, sys
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elections_common import RAW, ROOT
SRC = os.path.join(RAW, "Opinion_polling_for_the_2026_New_Zealand_general_election.html")
COLS = {"NAT": "national", "LAB": "labour", "GRN": "green", "ACT": "act", "NZF": "nz-first", "TPM": "te-pati-maori", "OPP": "opportunity"}
soup = BeautifulSoup(open(SRC).read(), "lxml")
for s in soup.select("sup.reference"): s.decompose()
tables = soup.select("table.wikitable")
t = next(x for x in tables if x.find("th") and "Polling organisation" in x.get_text() and "NAT" in x.get_text())
hdr = [th.get_text(" ", strip=True) for th in t.find("tr").find_all("th")]
polls, events = [], []
def num(s):
    s = s.replace(",", "").strip()
    m = re.match(r"^<?\s*(\d+(?:\.\d+)?)", s)
    return float(m.group(1)) if m else None
for tr in t.find_all("tr")[1:]:
    cells = tr.find_all(["td", "th"])
    if not cells: continue
    if len(cells) == 2 and cells[1].has_attr("colspan"):
        events.append({"date": cells[0].get_text(" ", strip=True), "event": re.sub(r"\s+([.,])", r"\1", cells[1].get_text(" ", strip=True))}); continue
    if len(cells) < len(hdr) - 1: continue
    txt = [c.get_text(" ", strip=True) for c in cells]
    if txt[1] in ("Polling organisation",): continue
    row = dict(zip(hdr, cells))
    dcell = cells[0]
    a = cells[1].find("a", href=True)
    p = {"date": txt[0], "end_date": dcell.get("data-sort-value") or None, "pollster": txt[1],
         "source_url": a["href"] if a and a["href"].startswith("http") else None,
         "sample_size": int(num(txt[2])) if txt[2] and num(txt[2]) else None, "results": {}}
    if "election result" in txt[1].lower():
        p["is_election_result"] = True
    for h, c in zip(hdr, cells):
        key = h.split("[")[0].strip()
        if key in COLS:
            v = num(c.get_text(" ", strip=True)); 
            if v is not None: p["results"][COLS[key]] = v
        elif key == "Others":
            v = num(c.get_text(" ", strip=True)); p["others"] = v
            note = c.find(class_="reference")
    if p["results"]: polls.append(p)
# Others footnotes (efn) are rendered as notes; keep raw text of the 'Others' footnotes not attempted.
out = {"title": "Opinion polls (party vote) for the 2026 New Zealand general election, since the 14 Oct 2023 election",
       "source": "https://en.wikipedia.org/wiki/Opinion_polling_for_the_2026_New_Zealand_general_election",
       "retrieved": json.load(open(SRC.replace(".html", ".meta.json"))).get("retrieved"),
       "parties": COLS, "notes": "Percentages as published. 'end_date' is the sort date used by Wikipedia (last fieldwork day or release date). Rows are newest first. 'others' = combined minor parties where listed. Poll sources: each row's source_url as linked on Wikipedia.",
       "count": len([p for p in polls if not p.get("is_election_result")]), "polls": polls, "events": events}
json.dump(out, open(os.path.join(ROOT, "data", "polls-2026.json"), "w"), ensure_ascii=False, indent=1)
print(out["count"], "polls;", len(events), "events; pollsters:", sorted({p["pollster"] for p in polls}))

#!/usr/bin/env python3
"""Extract party-vote results for 2011-2023 from the Wikipedia election-article HTML already in raw/elections/
(summary tables cite electionresults.govt.nz official results). Writes raw/minor-parties/results.json and prints
minor-party rows plus the 'wasted vote' (party votes for parties winning no seats).
Usage: python3 -I tools/minor_parties_results.py"""
import json, os, re
from bs4 import BeautifulSoup
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SLUG = {"National": "national", "Labour": "labour", "Green": "green", "NZ First": "nz-first", "ACT": "act",
        "Māori Party": "te-pati-maori", "Te Pāti Māori": "te-pati-maori", "Mana": "mana", "United Future": "united-future",
        "Conservative": "conservative", "New Conservative": "conservative", "Legalise Cannabis": "legalise-cannabis",
        "Democrats": "social-credit", "Social Credit": "social-credit", "Libertarianz": "libertarianz", "Alliance": "alliance",
        "Internet Mana": "internet-party", "Internet": "internet-party", "Ban 1080": "ban-1080", "Civilian": "civilian",
        "Independent Coalition": "nz-independent-coalition", "Focus": "focus-nz", "Opportunities": "opportunity",
        "Opportunities (TOP)": "opportunity", "People's Party": "nz-peoples-party", "Outdoors": "nz-outdoors-freedom",
        "Advance NZ": "advance-nz", "ONE": "newzeal", "NewZeal": "newzeal", "Vision NZ": "vision-nz", "TEA": "nz-tea-party",
        "Sustainable NZ": "sustainable-nz", "Heartland": "heartland", "NZ Loyal": "nz-loyal", "Freedoms NZ": "freedoms-nz",
        "DemocracyNZ": "democracynz", "Animal Justice": "animal-justice", "Women's Rights": "womens-rights",
        "Leighton Baker Party": "leighton-baker", "New Nation": "new-nation"}
MAJOR = {"national", "labour", "green", "act", "nz-first", "te-pati-maori"}

def num(s):
    s = re.sub(r"\[.*?\]", "", s).replace(",", "").strip()
    try: return float(s)
    except ValueError: return None

out = {}
for y in [2011, 2014, 2017, 2020, 2023]:
    s = BeautifulSoup(open(f"{ROOT}/raw/elections/{y}_New_Zealand_general_election.html").read(), "html.parser")
    t = next(t for t in s.find_all("table") if t.find("caption") and "Summary" in t.find("caption").get_text())
    rows, total = [], None
    for tr in t.find_all("tr"):
        c = [x.get_text(" ", strip=True) for x in tr.find_all(["td", "th"])]
        if len(c) > 3 and c[0] == "" and c[1] not in ("Unregistered parties", "Unregistered Parties", "Independent"):
            name = re.sub(r"\s*\[.*?\]", "", c[1]).strip()
            seats = num(c[-2]) if y < 2020 else num(c[-2])
            rows.append({"name": name, "slug": SLUG.get(name), "party_votes": num(c[2]), "party_vote_pct": num(c[3]),
                         "total_seats": int(seats or 0)})
        if c and c[0] == "Total":
            total = num(c[1])
        if c and c[0] == "Valid votes":
            valid = num(c[1])
    wasted = sum(r["party_votes"] or 0 for r in rows if r["total_seats"] == 0)
    out[y] = {"parties": rows, "total_party_votes_cast": total, "valid_party_votes": valid,
              "wasted_votes": wasted, "wasted_pct_of_total": round(100 * wasted / total, 2),
              "wasted_pct_of_valid": round(100 * wasted / valid, 2),
              "source": f"https://en.wikipedia.org/wiki/{y}_New_Zealand_general_election (summary table citing electionresults.govt.nz)"}
json.dump(out, open(f"{ROOT}/raw/minor-parties/results.json", "w"), indent=1, ensure_ascii=False)
for y, d in out.items():
    minor = [r for r in d["parties"] if r["slug"] not in MAJOR]
    print(y, "wasted", d["wasted_votes"], d["wasted_pct_of_total"], d["wasted_pct_of_valid"], "| minor total %",
          round(sum(r["party_vote_pct"] or 0 for r in minor), 2), "| n parties", len(d["parties"]))
    for r in d["parties"]:
        print("   ", r)

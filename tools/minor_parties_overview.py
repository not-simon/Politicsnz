#!/usr/bin/env python3
"""Print the overview table + summary statistics used in parties/MINOR_PARTIES.md from raw/minor-parties/results.json.
Usage: python3 -I tools/minor_parties_overview.py"""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
R = json.load(open(os.path.join(ROOT, "raw/minor-parties/results.json")))
YEARS = ["2011", "2014", "2017", "2020", "2023"]
MAJOR = {"national", "labour", "green", "act", "nz-first", "te-pati-maori"}
STATUS = {"united-future": "Dissolved 2017 (dereg. Feb 2018)", "mana": "Deregistered 2021", "conservative": "**Contesting 2026** (as Conservative Party NZ)",
 "legalise-cannabis": "**Contesting 2026**", "social-credit": "Deregistered Feb 2023", "libertarianz": "Deregistered Jan 2014", "alliance": "**Contesting 2026** (re-registered Aug 2026)",
 "internet-party": "Deregistered Jun 2018 (dormant)", "ban-1080": "Deregistered Feb 2018", "civilian": "Deregistered May 2015", "nz-independent-coalition": "Deregistered May 2016",
 "focus-nz": "Deregistered Feb 2016", "opportunity": "**Contesting 2026** (polling ~5–8%)", "nz-peoples-party": "Deregistered Apr 2019", "nz-outdoors-freedom": "**Contesting 2026**",
 "advance-nz": "Deregistered Aug 2021", "newzeal": "Deregistered Mar 2026 (aligned with NZ First)", "vision-nz": "**Contesting 2026**", "nz-tea-party": "Deregistered Sep 2022",
 "sustainable-nz": "Deregistered Dec 2021", "heartland": "Deregistered Jun 2023", "nz-loyal": "**Contesting 2026** (re-registered Aug 2026)", "freedoms-nz": "Deregistered May 2025",
 "democracynz": "Deregistered Feb 2024", "animal-justice": "**Contesting 2026**", "womens-rights": "**Contesting 2026**", "leighton-baker": "Deregistered May 2024", "new-nation": "Deregistered Jan 2025"}
NAME = {}
cell = {}
for y in YEARS:
    for r in R[y]["parties"]:
        s = r["slug"]
        if s in MAJOR: continue
        NAME.setdefault(s, r["name"])
        if r["party_vote_pct"] is None:
            cell[(s, y)] = "e/o"
        else:
            cell[(s, y)] = f"{r['party_vote_pct']:.2f}" + (f" (**{r['total_seats']}**)" if r["total_seats"] else "")
order = sorted(NAME, key=lambda s: -max(float(cell.get((s, y), "0").split()[0]) if cell.get((s, y), "0") not in ("e/o",) else 0 for y in YEARS))
print("| Party | " + " | ".join(YEARS) + " | Status Oct 2026 |")
print("|---|" + "---|" * (len(YEARS) + 1))
for s in order:
    print(f"| [{NAME[s]}]({s}/README.md) | " + " | ".join(cell.get((s, y), "–") for y in YEARS) + f" | {STATUS.get(s, '')} |")
print()
for y in YEARS:
    ps = R[y]["parties"]
    tot = sum(p["party_vote_pct"] or 0 for p in ps)
    minor = [p for p in ps if p["slug"] not in MAJOR]
    enp = 1 / sum(((p["party_vote_pct"] or 0) / tot) ** 2 for p in ps)
    seated = [p["name"] for p in ps if p["total_seats"]]
    below5_seated = [p["name"] for p in ps if p["total_seats"] and (p["party_vote_pct"] or 0) < 5]
    print(y, "| lists:", sum(1 for p in ps if p["party_votes"]), "| in parl:", len(seated), "| minor(non-big6) %:", round(sum(p["party_vote_pct"] or 0 for p in minor), 2),
          "| wasted %total:", R[y]["wasted_pct_of_total"], "| ENP(votes):", round(enp, 2), "| seats via electorate below 5%:", below5_seated,
          "| >=1% outside parl:", [p["name"] for p in ps if not p["total_seats"] and (p["party_vote_pct"] or 0) >= 1])

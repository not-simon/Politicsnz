#!/usr/bin/env python3
"""Validate data/elections/*.json, data/parliaments/*.json and data/polls-2026.json.
Checks seat arithmetic, electorate counts, overhang, composition totals and slug consistency.
Exit code 1 if any check fails. Usage: python3 tools/elections_validate.py"""
import json, os, re, sys, glob, unicodedata
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elections_common import PARTY
KNOWN = set(PARTY.values())
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
errors, warns = [], []
def err(m): errors.append(m)
def chk_party(slug, where):
    if slug not in KNOWN: err(f"{where}: unknown party slug {slug!r}")

for f in sorted(glob.glob(os.path.join(ROOT, "data", "elections", "*.json"))):
    d = json.load(open(f)); y = d["year"]; w = f"elections/{y}"
    if d.get("results", 1) is None:  # upcoming
        for p in d.get("registered_parties_party_vote", []): chk_party(p["party"], w)
        continue
    tot = sum(p["total_seats"] for p in d["parties"])
    if tot != d["total_seats"]: err(f"{w}: party seats sum {tot} != total_seats {d['total_seats']}")
    if d["overhang"] != d["total_seats"] - 120: err(f"{w}: overhang {d['overhang']} != total-120")
    for p in d["parties"]:
        chk_party(p["party"], w)
        if p["electorate_seats"] + p["list_seats"] != p["total_seats"]:
            err(f"{w}: {p['party']} electorate+list != total")
    if sum(p["list_seats"] for p in d["parties"]) + len(d["electorates"]) != d["total_seats"]:
        err(f"{w}: list seats + electorates != total seats")
    won = {}
    for e in d["electorates"]:
        chk_party(e["party"], w + "/" + e["name"])
        if e.get("runner_up_party"): chk_party(e["runner_up_party"], w + "/" + e["name"])
        won[e["party"]] = won.get(e["party"], 0) + 1
        if not e["winner"] or e["majority"] is None: err(f"{w}: incomplete electorate {e['name']}")
    for p in d["parties"]:
        if won.get(p["party"], 0) != p["electorate_seats"]:
            err(f"{w}: {p['party']} won {won.get(p['party'],0)} electorates but electorate_seats={p['electorate_seats']}")
    pct = sum(p["party_vote_pct"] or 0 for p in d["parties"])
    if not 99.5 <= pct <= 100.5: warns.append(f"{w}: party vote % sums to {pct:.2f}")
    if len({e["name"] for e in d["electorates"]}) != len(d["electorates"]): err(f"{w}: duplicate electorate names")

name_slug = {}
for f in sorted(glob.glob(os.path.join(ROOT, "data", "parliaments", "*.json"))):
    d = json.load(open(f)); n = d["parliament"]; w = f"parliaments/{n}"
    for k in ("composition_start", "composition_now_or_end", "composition_at_election"):
        for p in d[k]: chk_party(p, w + "/" + k)
    if sum(d["composition_now_or_end"].values()) != d["total_now_or_end"]: err(f"{w}: end composition sum mismatch")
    if sum(d["composition_start"].values()) != d["total_start"]: err(f"{w}: start composition sum mismatch")
    el = json.load(open(os.path.join(ROOT, "data", "elections", f"{d['election_year']}.json")))
    if sum(d["composition_start"].values()) != el["total_seats"]:
        err(f"{w}: start composition {sum(d['composition_start'].values())} != election total {el['total_seats']}")
    elec = {p["party"]: p["total_seats"] for p in el["parties"] if p["total_seats"]}
    if d["composition_start"] != {k: v for k, v in elec.items()}:
        warns.append(f"{w}: composition_start {d['composition_start']} differs from election result {elec}")
    live = 0
    for m in d["members"]:
        if not SLUG.match(m["slug"]): err(f"{w}: bad slug {m['slug']!r}")
        chk_party(m["party"], w + "/" + m["name"])
        for pc in m["party_changes"]: chk_party(pc["to"], w + "/" + m["name"])
        if m["name"] in name_slug and name_slug[m["name"]] != m["slug"]:
            err(f"slug inconsistency for {m['name']}: {name_slug[m['name']]} vs {m['slug']}")
        name_slug[m["name"]] = m["slug"]
        if m["left"] is None: live += 1
        if m["left"] and m["entered"] and m["left"] < m["entered"]: err(f"{w}: {m['name']} left before entering")
    if live != d["total_now_or_end"]: err(f"{w}: live members {live} != total_now_or_end")
    if live > el["total_seats"]: err(f"{w}: more sitting members than seats")
# slug clash: two different names -> same slug
inv = {}
for nm, s in name_slug.items(): inv.setdefault(s, set()).add(nm)
for s, nms in inv.items():
    if len(nms) > 1: warns.append(f"slug {s} used for several names: {sorted(nms)}")

pf = os.path.join(ROOT, "data", "polls-2026.json")
if os.path.exists(pf):
    d = json.load(open(pf))
    for p in d["polls"]:
        for k, v in p["results"].items():
            chk_party(k, "polls")
            if not 0 <= v <= 100: err(f"polls: bad value {k}={v} in {p['date']}")
        s = sum(p["results"].values()) + (p.get("others") or 0)
        if s > 103: warns.append(f"polls: {p['date']} {p['pollster']} sums to {s:.1f}")

for m in warns: print("WARN", m)
for m in errors: print("ERROR", m)
print(f"{len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)

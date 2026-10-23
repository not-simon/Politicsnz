#!/usr/bin/env python3
"""Fill the generated blocks in elections/<year>.md and elections/trends.md from data/.
Blocks: <!-- GENERATED:<name> START --> ... <!-- GENERATED:<name> END -->  (narrative outside blocks is hand-written)."""
import json, os, re, sys, glob, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elections_common import ROOT, person_slug
D = lambda *p: os.path.join(ROOT, *p)
NAME = {"national": "National", "labour": "Labour", "green": "Green", "act": "ACT", "nz-first": "NZ First",
        "te-pati-maori": "Te Pāti Māori / Māori Party", "mana": "Mana", "united-future": "United Future", "independent": "Independent",
        "conservative": "Conservative / New Conservative", "opportunity": "TOP", "internet-mana": "Internet MANA",
        "progressive": "Progressive", "legalise-cannabis": "Legalise Cannabis", "internet-party": "Internet Party", "nz-loyal": "NZ Loyal"}
def nm(s): return NAME.get(s, s)
def fmt(n): return f"{n:,}" if isinstance(n, int) else ("–" if n is None else str(n))
def load(y): return json.load(open(D("data", "elections", f"{y}.json")))
YEARS = [2008, 2011, 2014, 2017, 2020, 2023]
PARL = {2011: 50, 2014: 51, 2017: 52, 2020: 53, 2023: 54}

def results_block(y):
    d = load(y); prev = load(y - 3) if y - 3 in YEARS else None
    pp = {p["party"]: p for p in prev["parties"]} if prev else {}
    L = [f"**Election day:** {d['date']} · **Turnout:** {d['turnout_pct']}% of {fmt(d['enrolled'])} enrolled ({fmt(d['votes_cast'])} votes cast) · "
         f"**House:** {d['total_seats']} seats ({d['overhang']} overhang) · **Electorates:** {d['electorates_count']} · **List seats:** {d['list_seats_count']}", "",
         "| Party | Party votes | Party vote % | ± pp | Electorate seats | List seats | Total seats | ± seats |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for p in sorted(d["parties"], key=lambda p: (-(p["total_seats"]), -(p["party_vote_pct"] or 0))):
        if p["party"] == "independent": continue
        q = pp.get(p["party"]); dp = ds = ""
        if q and p["party_vote_pct"] is not None and q.get("party_vote_pct") is not None:
            dp = f"{p['party_vote_pct'] - q['party_vote_pct']:+.2f}"; ds = f"{p['total_seats'] - q['total_seats']:+d}"
        elif prev: dp, ds = "new", ""
        L.append(f"| {p['name']} (`{p['party']}`) | {fmt(p['party_votes'])} | {p['party_vote_pct'] if p['party_vote_pct'] is not None else '–'} | {dp} | {p['electorate_seats']} | {p['list_seats']} | **{p['total_seats']}** | {ds} |")
    L += ["", f"Party votes for parties that won no seats (the 'wasted' vote): **{fmt(d['wasted_party_votes'])} ({d['wasted_party_vote_pct']}% of valid party votes)**.", ""]
    if d.get("notes"): L += [f"> {n}" for n in d["notes"]] + [""]
    g = d["government"]
    L += [f"**Government formed:** {g['name']} – PM {g['pm']} – {', '.join(nm(x) for x in g['parties'])} ({g['arrangement']})"
          + (f"; support: {', '.join(nm(s['party']) + ' (' + s['arrangement'] + ')' for s in g['support'])}" if g["support"] else "")
          + f"; sworn in {g['formed']}.", "", g["notes"], ""]
    return "\n".join(L)

def electorates_block(y):
    d = load(y)
    L = ["| Electorate | Winner | Party | Majority | Runner-up | Runner-up party | Change |", "|---|---|---|---:|---|---|---|"]
    for e in d["electorates"]:
        ch = ""
        if e.get("incumbent_party") and e["incumbent_party"] != e["party"]: ch = f"**{nm(e['party'])} gain from {nm(e['incumbent_party'])}**"
        elif e["result"] == "new": ch = "new seat"
        L.append(f"| {e['name']}{' (Māori)' if e['type']=='maori' else ''} | {e['winner']} | {nm(e['party'])} | {fmt(e['majority'])} | {e['runner_up']} | {nm(e['runner_up_party']) if e['runner_up_party'] else ''} | {ch} |")
    tight = sorted([e for e in d["electorates"] if e["majority"] is not None], key=lambda e: e["majority"])[:10]
    L += ["", "**Ten most marginal electorates:** " + "; ".join(f"{e['name']} ({e['winner']}, {nm(e['party'])}, {fmt(e['majority'])})" for e in tight), ""]
    gains = [e for e in d["electorates"] if e.get("incumbent_party") and e["incumbent_party"] != e["party"]]
    L += [f"**Seats that changed party ({len(gains)}):** " + ("; ".join(f"{e['name']} ({nm(e['incumbent_party'])} → {nm(e['party'])})" for e in gains) or "none"), ""]
    return "\n".join(L)

def parliament_block(y):
    n = PARL[y]; p = json.load(open(D("data", "parliaments", f"{n}.json")))
    c = lambda comp: ", ".join(f"{nm(k)} {v}" for k, v in comp.items())
    L = [f"**{n}th Parliament** ({p['start']} – {p['end'] or 'present'}): start {c(p['composition_start'])} (= {p['total_start']}); "
         f"at end/dissolution {c(p['composition_now_or_end'])} (= {p['total_now_or_end']}). Full membership: [`data/parliaments/{n}.json`](../data/parliaments/{n}.json).", "",
         "| Date | Change |", "|---|---|"]
    for ch in p["changes"]: L.append(f"| {ch['date']} | {ch['description'].split(': ', 1)[-1] if ch['description'].startswith(ch['date']) else ch['description']} |")
    return "\n".join(L) + "\n"

def trends_blocks():
    out = {}
    ds = {y: load(y) for y in YEARS}
    main = ["national", "labour", "green", "act", "nz-first", "te-pati-maori", "opportunity", "conservative", "united-future", "mana", "internet-mana", "legalise-cannabis", "nz-loyal"]
    L = ["| Party | " + " | ".join(str(y) for y in YEARS) + " |", "|---|" + "---:|" * len(YEARS)]
    for s in main:
        row = []
        for y in YEARS:
            p = next((p for p in ds[y]["parties"] if p["party"] == s), None)
            row.append(f"{p['party_vote_pct']:.2f}" if p and p["party_vote_pct"] is not None else "–")
        L.append(f"| {nm(s)} | " + " | ".join(row) + " |")
    out["vote-share"] = "\n".join(L) + "\n"
    L = ["| Party | " + " | ".join(str(y) for y in YEARS) + " |", "|---|" + "---:|" * len(YEARS)]
    for s in main[:10]:
        row = []
        for y in YEARS:
            p = next((p for p in ds[y]["parties"] if p["party"] == s), None)
            row.append(f"{p['total_seats']} ({p['electorate_seats']}+{p['list_seats']})" if p and p["total_seats"] else ("0" if p else "–"))
        L.append(f"| {nm(s)} | " + " | ".join(row) + " |")
    L.append("| **Total** | " + " | ".join(str(ds[y]["total_seats"]) for y in YEARS) + " |")
    out["seats"] = "\n".join(L) + "\n\nFormat: total (electorate + list). 2023 includes the Port Waikato by-election seat.\n"
    L = ["| Year | Enrolled | Votes cast | Turnout % | Overhang | Parties winning seats | Parties on ballot (party vote) | 'Wasted' party vote % |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for y in YEARS:
        d = ds[y]
        L.append(f"| {y} | {fmt(d['enrolled'])} | {fmt(d['votes_cast'])} | {d['turnout_pct']} | {d['overhang']} | {sum(1 for p in d['parties'] if p['total_seats'])} | {sum(1 for p in d['parties'] if p['party_votes'])} | {d['wasted_party_vote_pct']} |")
    out["turnout"] = "\n".join(L) + "\n"
    # Māori electorates
    L = ["| Electorate | " + " | ".join(str(y) for y in YEARS) + " |", "|---|" + "---|" * len(YEARS)]
    maori = sorted({e["name"] for y in YEARS for e in ds[y]["electorates"] if e["type"] == "maori"})
    for m in maori:
        row = []
        for y in YEARS:
            e = next((e for e in ds[y]["electorates"] if e["name"] == m), None)
            row.append(f"{nm(e['party']).split(' /')[0]} – {e['winner']} ({fmt(e['majority'])})" if e else "–")
        L.append(f"| {m} | " + " | ".join(row) + " |")
    tally = []
    for y in YEARS:
        c = {}
        for e in ds[y]["electorates"]:
            if e["type"] == "maori": c[nm(e["party"]).split(" /")[0]] = c.get(nm(e["party"]).split(" /")[0], 0) + 1
        tally.append(", ".join(f"{k} {v}" for k, v in sorted(c.items(), key=lambda x: -x[1])))
    L.append("| **Tally** | " + " | ".join(tally) + " |")
    out["maori"] = "\n".join(L) + "\n"
    # electorate deals
    L = ["| Year | Epsom winner (majority) | Ōhāriu/Ohariu winner (majority) | Party vote of the winner's party | Seats the deal delivered |", "|---|---|---|---|---|"]
    for y in YEARS:
        d = ds[y]
        ep = next(e for e in d["electorates"] if e["name"] == "Epsom")
        oh = next((e for e in d["electorates"] if person_slug(e["name"]).startswith("ohariu")), None)
        pv = {p["party"]: p for p in d["parties"]}
        L.append(f"| {y} | {ep['winner']} ({nm(ep['party'])}, {fmt(ep['majority'])}) | {oh['winner'] + ' (' + nm(oh['party']) + ', ' + fmt(oh['majority']) + ')' if oh else '–'} | ACT {pv['act']['party_vote_pct']}%" + (f"; United Future {pv['united-future']['party_vote_pct']}%" if 'united-future' in pv else "") + f" | ACT {pv['act']['total_seats']}" + (f", UF {pv['united-future']['total_seats']}" if 'united-future' in pv else "") + " |")
    out["deals"] = "\n".join(L) + "\n"
    # swing between two main parties
    L = ["| Election | National % | Labour % | Nat–Lab gap (pp) | Two-party combined % | Largest party | Govt formed by |", "|---|---:|---:|---:|---:|---|---|"]
    for y in YEARS:
        pv = {p["party"]: p["party_vote_pct"] for p in ds[y]["parties"]}
        big = "National" if pv["national"] > pv["labour"] else "Labour"
        L.append(f"| {y} | {pv['national']} | {pv['labour']} | {pv['national'] - pv['labour']:+.2f} | {pv['national'] + pv['labour']:.2f} | {big} | {', '.join(nm(x) for x in ds[y]['government']['parties'])} |")
    out["two-party"] = "\n".join(L) + "\n"
    # polls by quarter
    polls = json.load(open(D("data", "polls-2026.json")))["polls"]
    q = {}
    for p in polls:
        if p.get("is_election_result") or not p.get("end_date"): continue
        y, m = int(p["end_date"][:4]), int(p["end_date"][5:7])
        key = f"{y} Q{(m - 1)//3 + 1}"
        q.setdefault(key, []).append(p)
    parties = ["national", "labour", "green", "act", "nz-first", "te-pati-maori", "opportunity"]
    L = ["| Quarter | Polls | " + " | ".join(nm(s).split(' /')[0] for s in parties) + " | Nat+ACT+NZF | Lab+Grn+TPM |", "|---|---:|" + "---:|" * (len(parties) + 2)]
    for k in sorted(q):
        ps = q[k]; avg = {}
        for s in parties:
            v = [p["results"][s] for p in ps if s in p["results"]]
            avg[s] = statistics.mean(v) if v else None
        right = sum(avg[s] for s in ("national", "act", "nz-first") if avg[s] is not None)
        left = sum(avg[s] for s in ("labour", "green", "te-pati-maori") if avg[s] is not None)
        L.append(f"| {k} | {len(ps)} | " + " | ".join(f"{avg[s]:.1f}" if avg[s] is not None else "–" for s in parties) + f" | {right:.1f} | {left:.1f} |")
    out["polls"] = "\n".join(L) + "\n\nSimple unweighted mean of all published polls whose fieldwork ended in the quarter (from `data/polls-2026.json`); not a forecast.\n"
    return out

def latest_polls(n):
    polls = [p for p in json.load(open(D("data", "polls-2026.json")))["polls"] if not p.get("is_election_result")][:n]
    parties = ["national", "labour", "green", "act", "nz-first", "te-pati-maori", "opportunity"]
    L = ["| Fieldwork | Pollster | n | " + " | ".join(nm(s).split(' /')[0] for s in parties) + " |", "|---|---|---:|" + "---:|" * len(parties)]
    for p in polls:
        L.append(f"| {p['date']} | [{p['pollster']}]({p['source_url']}) | {fmt(p['sample_size'])} | " + " | ".join(str(p['results'].get(s, '–')) for s in parties) + " |")
    return "\n".join(L) + "\n"

def parties_2026():
    d = json.load(open(D("data", "elections", "2026.json")))
    L = ["| Party | Leader(s) | 2023 seats | Seats at dissolution | Status |", "|---|---|---:|---:|---|"]
    for p in d["registered_parties_party_vote"]:
        L.append(f"| {p['name']} (`{p['party']}`) | {p['leader']} | {p.get('seats_2023', 0)} | {p.get('seats_at_dissolution', 0)} | {p['status']}{' – ' + p['note'] if p.get('note') else ''} |")
    return "\n".join(L) + "\n"

def fill(path, blocks):
    s = open(path).read()
    for k, v in blocks.items():
        pat = re.compile(r"(<!-- GENERATED:%s START -->\n).*?(<!-- GENERATED:%s END -->)" % (re.escape(k), re.escape(k)), re.S)
        if not pat.search(s): print("missing block", k, "in", path); continue
        s = pat.sub(lambda m: m.group(1) + v.rstrip() + "\n" + m.group(2), s)
    open(path, "w").write(s)

if __name__ == "__main__":
    for y in PARL:
        f = D("elections", f"{y}.md")
        if os.path.exists(f):
            fill(f, {"results": results_block(y), "electorates": electorates_block(y), "parliament": parliament_block(y)})
    tb = trends_blocks()
    if os.path.exists(D("elections", "trends.md")): fill(D("elections", "trends.md"), tb)
    if os.path.exists(D("elections", "2026.md")):
        fill(D("elections", "2026.md"), {"polls": tb["polls"], "latest-polls": latest_polls(12), "parties-2026": parties_2026()})
    print("ok")

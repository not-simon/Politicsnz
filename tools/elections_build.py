#!/usr/bin/env python3
"""Build data/elections/{2008..2023}.json from raw/elections (Wikipedia wikitext + rendered HTML).
Run: python3 -I tools/elections_build.py   (from repo root; -I is fine, path inserted below)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elections_common import RAW, ROOT, party_slug
from elections_parse import summary_table, electorates_from_wikitext

MAORI = {"Te Tai Tokerau", "Tāmaki Makaurau", "Hauraki-Waikato", "Waiariki", "Ikaroa-Rāwhiti", "Te Tai Hauāuru", "Te Tai Tonga"}
W = "https://en.wikipedia.org/wiki/"
YEARS = {
 2008: dict(date="2008-11-08", parliament=49, page="2008_New_Zealand_general_election", el="2008_New_Zealand_general_election",
   official="https://archive.electionresults.govt.nz/electionresults_2008/e9/html/statistics.html",
   government={"formed": "2008-11-19", "pm": "John Key", "parties": ["national"], "arrangement": "minority government with confidence & supply",
     "support": [{"party": "act", "arrangement": "confidence & supply"}, {"party": "united-future", "arrangement": "confidence & supply"},
                 {"party": "te-pati-maori", "arrangement": "confidence & supply"}],
     "name": "Fifth National Government",
     "notes": "John Key sworn in as Prime Minister 19 Nov 2008. National governed as a minority government with confidence-and-supply agreements with ACT, United Future and the Māori Party (69 of 122 seats). The Greens signed a separate, narrower memorandum of understanding in 2009. Labour's Helen Clark conceded on election night and stood down as Labour leader."},
   sources_extra=[W + "Fifth_National_Government_of_New_Zealand"]),
 2011: dict(date="2011-11-26", parliament=50, page="2011_New_Zealand_general_election", el="2011_New_Zealand_general_election",
   official="https://archive.electionresults.govt.nz/electionresults_2011/e9/html/statistics.html",
   government={"formed": "2011-12-14", "pm": "John Key", "parties": ["national"], "arrangement": "minority government with confidence & supply",
     "support": [{"party": "act", "arrangement": "confidence & supply"}, {"party": "united-future", "arrangement": "confidence & supply"},
                 {"party": "te-pati-maori", "arrangement": "confidence & supply"}],
     "name": "Fifth National Government (second term)",
     "notes": "National (59 seats) renewed confidence-and-supply agreements with ACT (1), United Future (1) and the Māori Party (3): 64 of 121 seats. New ministry appointed at Government House 14 Dec 2011. The election was held alongside a referendum on retaining MMP (MMP retained, 57.8%)."},
   sources_extra=[W + "Fifth_National_Government_of_New_Zealand", "https://gg.govt.nz/node/542"]),
 2014: dict(date="2014-09-20", parliament=51, page="2014_New_Zealand_general_election", el="2014_New_Zealand_general_election",
   official="https://archive.electionresults.govt.nz/electionresults_2014/e9/html/statistics.html",
   government={"formed": "2014-10-08", "pm": "John Key (to 12 Dec 2016), then Bill English", "parties": ["national"], "arrangement": "minority government with confidence & supply",
     "support": [{"party": "act", "arrangement": "confidence & supply"}, {"party": "united-future", "arrangement": "confidence & supply"},
                 {"party": "te-pati-maori", "arrangement": "confidence & supply"}],
     "name": "Fifth National Government (third term)",
     "notes": "National won 61 of 121 seats on election night but lost one seat (to the Greens) on the official count, leaving 60. It re-signed confidence-and-supply agreements with ACT, United Future (29 Sep 2014) and the Māori Party (5 Oct 2014). Ministry sworn in 8 Oct 2014. John Key resigned in Dec 2016; Bill English became PM on 12 Dec 2016."},
   sources_extra=[W + "Fifth_National_Government_of_New_Zealand", "https://www.rnz.co.nz/news/political/256425/new-government-sworn-in"]),
 2017: dict(date="2017-09-23", parliament=52, page="Results_of_the_2017_New_Zealand_general_election", el="Results_of_the_2017_New_Zealand_general_election",
   official="https://archive.electionresults.govt.nz/electionresults_2017/statistics/overall-results-summary.html",
   government={"formed": "2017-10-26", "pm": "Jacinda Ardern", "parties": ["labour", "nz-first"], "arrangement": "coalition (minority) with confidence & supply",
     "support": [{"party": "green", "arrangement": "confidence & supply"}],
     "name": "Sixth Labour Government",
     "notes": "National won the most seats (56) but no majority. Winston Peters announced on 19 Oct 2017 that NZ First (9) would form a coalition with Labour (46); the Greens (8) signed a confidence-and-supply agreement the same day (63 of 120 seats). Sworn in 26 Oct 2017. Peters became Deputy PM."},
   sources_extra=[W + "Sixth_Labour_Government_of_New_Zealand", W + "2017_New_Zealand_general_election"]),
 2020: dict(date="2020-10-17", parliament=53, page="Results_of_the_2020_New_Zealand_general_election", el="Results_of_the_2020_New_Zealand_general_election",
   official="https://www.electionresults.govt.nz/electionresults_2020/",
   government={"formed": "2020-11-06", "pm": "Jacinda Ardern (to 25 Jan 2023), then Chris Hipkins", "parties": ["labour"], "arrangement": "single-party majority government",
     "support": [{"party": "green", "arrangement": "cooperation agreement"}],
     "name": "Sixth Labour Government (second term)",
     "notes": "Labour won 65 of 120 seats, the first single-party majority under MMP. It nonetheless signed a 'cooperation agreement' with the Greens (31 Oct 2020) under which Green co-leaders James Shaw and Marama Davidson became ministers outside Cabinet; the Greens were not bound on confidence and supply beyond the agreement. Sworn in 6 Nov 2020. Ardern resigned in Jan 2023; Chris Hipkins became PM on 25 Jan 2023. Election held with the cannabis and End of Life Choice referendums; it was delayed from 19 Sep to 17 Oct because of COVID-19."},
   sources_extra=[W + "Sixth_Labour_Government_of_New_Zealand", W + "2020_New_Zealand_general_election"]),
 2023: dict(date="2023-10-14", parliament=54, page="2023_New_Zealand_general_election", el="2023_New_Zealand_general_election",
   official="https://www.electionresults.govt.nz/electionresults_2023/",
   government={"formed": "2023-11-27", "pm": "Christopher Luxon", "parties": ["national", "act", "nz-first"], "arrangement": "coalition",
     "support": [],
     "name": "Sixth National Government",
     "notes": "First three-party coalition under MMP. Separate coalition agreements National–ACT and National–NZ First were signed on 24 Nov 2023; ministers sworn in 27 Nov 2023. Deputy PM rotates: Winston Peters (NZ First) to 31 May 2025, then David Seymour (ACT). Government holds 68 of 123 seats (49+11+8) after the Port Waikato by-election."},
   sources_extra=[W + "Sixth_National_Government_of_New_Zealand", W + "2023_Port_Waikato_by-election"]),
}

def build(year):
    c = YEARS[year]
    rows, meta = summary_table(os.path.join(RAW, c["page"] + ".html"))
    els = electorates_from_wikitext(os.path.join(RAW, c["el"] + ".wikitext"))
    for e in els:
        e["type"] = "maori" if e["name"] in MAORI else "general"
    notes = []
    parties = []
    for r in rows:
        p = {"party": r["party"], "name": r["display"], "party_votes": r["party_votes"], "party_vote_pct": r["party_vote_pct"],
             "electorate_seats": r["electorate_seats"], "list_seats": r["list_seats"], "total_seats": r["total_seats"],
             "electorate_votes": r["electorate_votes"], "electorate_votes_pct": r["electorate_votes_pct"]}
        parties.append(p)
    total = sum(p["total_seats"] for p in parties)
    assert total == meta["total_seats"], (year, total, meta["total_seats"])
    out = {"year": year, "date": c["date"], "parliament": c["parliament"], "turnout_pct": meta["turnout_pct"],
           "turnout_basis": "votes cast (incl. informal and disallowed) as % of enrolled electors",
           "enrolled": meta["enrolled"], "votes_cast": meta["votes_cast"],
           "valid_party_votes": meta["valid_party_votes"], "informal_party_votes": meta.get("informal_party_votes"),
           "disallowed_party_votes": meta.get("disallowed_party_votes"),
           "electorates_count": len(els), "list_seats_count": None, "overhang": None, "total_seats": total}
    if year == 2023:
        # Port Waikato: general-election electorate vote cancelled after ACT candidate Neil Christensen died (9 Oct 2023);
        # by-election 25 Nov 2023 won by National's Andrew Bayly (already elected from the list) -> Nancy Lu enters from list.
        nat = next(p for p in parties if p["party"] == "national")
        nat["electorate_seats"] += 1; nat["total_seats"] += 1
        nat["note"] = "Official count gave 48 seats (43 electorate + 5 list). Winning the Port Waikato by-election (25 Nov 2023) added a 49th seat (an extra overhang seat): 44 electorate + 5 list."
        els.append({"name": "Port Waikato", "winner": "Andrew Bayly", "party": "national", "majority": 11432,
                    "runner_up": "Casey Costello", "runner_up_party": "nz-first", "third": None, "third_party": None,
                    "result": "hold", "incumbent": "Andrew Bayly", "incumbent_party": "national", "type": "general",
                    "note": "Electorate vote cancelled at the general election after the death of ACT candidate Neil Christensen; filled at the 2023 Port Waikato by-election, 25 Nov 2023 (turnout c. 35.7%). Majority per RNZ final results."})
        els.sort(key=lambda e: (e["type"] == "maori", e["name"]))
        out["total_seats"] = total + 1
        out["total_seats_at_official_count"] = total
        out["electorates_count"] = len(els)
        notes.append("Official results (3 Nov 2023) were adjusted by judicial recounts later in Nov 2023; figures here follow the post-recount table on Wikipedia (e.g. National 1,085,851 / 38.08%). Some contemporaneous reports quote the pre-recount 1,085,016 / 38.06%.")
        notes.append("Te Pāti Māori won 6 electorates but its 3.08% party vote entitled it to 4 seats: 2 overhang seats (122). Port Waikato by-election added a third overhang seat (123).")
    out["list_seats_count"] = sum(p["list_seats"] for p in parties)
    out["overhang"] = out["total_seats"] - 120
    qual = {p["party"] for p in parties if p["total_seats"] > 0}
    wasted = sum(p["party_votes"] or 0 for p in parties if p["party"] not in qual)
    out["wasted_party_votes"] = wasted
    out["wasted_party_vote_pct"] = round(100 * wasted / meta["valid_party_votes"], 2)
    if meta.get("below_threshold_votes") and abs(meta["below_threshold_votes"] - wasted) > 5:
        notes.append(f"Wikipedia's 'below threshold' figure is {meta['below_threshold_votes']}; computed sum of party votes for parties winning no seats is {wasted}.")
    out["parties"] = parties
    out["government"] = c["government"]
    out["electorates"] = els
    out["notes"] = notes
    out["sources"] = [W + c["page"], W + c["el"] if c["el"] != c["page"] else None, c["official"] + " (official Electoral Commission results; blocked by Cloudflare from this environment, values taken via Wikipedia which cites it)"] + c["sources_extra"]
    out["sources"] = [s for s in out["sources"] if s]
    return out

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "data", "elections"), exist_ok=True)
    for y in YEARS:
        d = build(y)
        json.dump(d, open(os.path.join(ROOT, "data", "elections", f"{y}.json"), "w"), ensure_ascii=False, indent=1)
        print(y, d["total_seats"], d["overhang"], d["turnout_pct"], len(d["parties"]), len(d["electorates"]), d["wasted_party_vote_pct"])

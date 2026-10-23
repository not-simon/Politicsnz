#!/usr/bin/env python3
"""Build data/parliaments/{50..54}.json.
Start-of-term membership = electorate winners (data/elections/<year>.json) + successful list MPs (Wikipedia
'List results' table); then mid-term changes from the parliament article's 'Changes' table (51st-54th) or the
manual list below (50th), plus manual party-affiliation changes not captured in those tables."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elections_common import RAW, ROOT, person_slug, existing_person_slugs
from elections_parse import list_mps_from_wikitext, changes_table

W = "https://en.wikipedia.org/wiki/"
P = {
 50: dict(year=2011, start="2011-12-20", end="2014-08-14", art="50th_New_Zealand_Parliament", listsrc="2011_New_Zealand_general_election"),
 51: dict(year=2014, start="2014-10-20", end="2017-08-18", art="51st_New_Zealand_Parliament", listsrc="2014_New_Zealand_general_election"),
 52: dict(year=2017, start="2017-11-07", end="2020-09-06", art="52nd_New_Zealand_Parliament", listsrc="Results_of_the_2017_New_Zealand_general_election"),
 53: dict(year=2020, start="2020-11-25", end="2023-09-08", art="53rd_New_Zealand_Parliament", listsrc="Results_of_the_2020_New_Zealand_general_election"),
 54: dict(year=2023, start="2023-12-05", end="2026-10-01", art="54th_New_Zealand_Parliament", listsrc="2023_New_Zealand_general_election"),
}
# 50th Parliament has no structured changes table on Wikipedia: transcribed from its "Summary of changes during term"
# list, with dates from each MP's Wikipedia article (infobox term dates / text).
MANUAL_CHANGES = {
 50: [
  {"seat": "List", "incumbent_party": "nz-first", "incumbent": "Brendan Horan", "date_vacated": "2012-12-04", "reason": "Expelled from the NZ First caucus (allegations about his late mother's finances); sat as an independent, later launched the NZ Independent Coalition (Jan 2014)", "replacement_party": "independent", "replacement": "Brendan Horan", "date_entered": "2012-12-04", "change": "Independent gain; NZ First loss", "src": W + "Brendan_Horan"},
  {"seat": "List", "incumbent_party": "national", "incumbent": "Lockwood Smith", "date_vacated": "2013-02-14", "reason": "Resigned (former Speaker) to become High Commissioner to the United Kingdom", "replacement_party": "national", "replacement": "Aaron Gilmore", "date_entered": "2013-02-15", "change": "List", "src": W + "Lockwood_Smith"},
  {"seat": "List", "incumbent_party": "labour", "incumbent": "Charles Chauvel", "date_vacated": "2013-03-11", "reason": "Resigned to work for the UN Development Programme", "replacement_party": "labour", "replacement": "Carol Beaumont", "date_entered": "2013-03-12", "change": "List", "src": W + "Charles_Chauvel_(politician)"},
  {"seat": "Ikaroa-Rāwhiti", "incumbent_party": "labour", "incumbent": "Parekura Horomia", "date_vacated": "2013-04-29", "reason": "Died", "replacement_party": "labour", "replacement": "Meka Whaitiri", "date_entered": "2013-06-29", "change": "Labour hold (2013 Ikaroa-Rāwhiti by-election)", "src": W + "2013_Ikaroa-Rāwhiti_by-election"},
  {"seat": "List", "incumbent_party": "national", "incumbent": "Aaron Gilmore", "date_vacated": "2013-05-27", "reason": "Resigned after the Hanmer Springs restaurant controversy", "replacement_party": "national", "replacement": "Claudette Hauiti", "date_entered": "2013-05-28", "change": "List", "src": W + "Aaron_Gilmore"},
  {"seat": "List", "incumbent_party": "national", "incumbent": "Jackie Blue", "date_vacated": "2013-05", "reason": "Resigned to become EEO Commissioner at the Human Rights Commission", "replacement_party": "national", "replacement": "Paul Foster-Bell", "date_entered": "2013-05-28", "change": "List", "src": W + "Paul_Foster-Bell"},
  {"seat": "Ōhāriu", "incumbent_party": "united-future", "incumbent": "Peter Dunne", "date_vacated": "2013-05-31", "reason": "United Future deregistered by the Electoral Commission at its own request (membership below 500); Dunne treated as an independent until re-registration on 13 Aug 2013", "replacement_party": "independent", "replacement": "Peter Dunne", "date_entered": "2013-05-31", "change": "Independent (temporary)", "src": W + "Peter_Dunne"},
  {"seat": "Ōhāriu", "incumbent_party": "independent", "incumbent": "Peter Dunne", "date_vacated": "2013-08-13", "reason": "United Future re-registered", "replacement_party": "united-future", "replacement": "Peter Dunne", "date_entered": "2013-08-13", "change": "United Future restored", "src": W + "Peter_Dunne"},
  {"seat": "Christchurch East", "incumbent_party": "labour", "incumbent": "Lianne Dalziel", "date_vacated": "2013-10-11", "reason": "Resigned after being elected Mayor of Christchurch", "replacement_party": "labour", "replacement": "Poto Williams", "date_entered": "2013-11-30", "change": "Labour hold (2013 Christchurch East by-election)", "src": W + "2013_Christchurch_East_by-election"},
  {"seat": "List", "incumbent_party": "national", "incumbent": "Katrina Shanks", "date_vacated": "2014-01-21", "reason": "Resigned (to become chief executive of Funeral Directors Association)", "replacement_party": "national", "replacement": "Jo Hayes", "date_entered": "2014-01-22", "change": "List", "src": W + "Katrina_Shanks"},
  {"seat": "List", "incumbent_party": "labour", "incumbent": "Shane Jones", "date_vacated": "2014-05-22", "reason": "Resigned to become Pacific economic ambassador", "replacement_party": "labour", "replacement": "Kelvin Davis", "date_entered": "2014-05-23", "change": "List", "src": W + "Kelvin_Davis_(politician)"},
  {"seat": "Epsom", "incumbent_party": "act", "incumbent": "John Banks", "date_vacated": "2014-06-08", "reason": "Resigned after being convicted of filing a false electoral return (conviction later quashed on appeal, 2015); no by-election as general election was within 6 months", "replacement": None, "replacement_party": None, "date_entered": None, "change": "None", "src": W + "John_Banks_(New_Zealand_politician)"},
 ],
}
EXTRA_CHANGES = {  # party-affiliation changes not in the Wikipedia changes tables
 52: [],
 54: [
  {"seat": "Te Tai Tokerau", "incumbent_party": "te-pati-maori", "incumbent": "Mariameno Kapa-Kingi", "date_vacated": "2026-05-11", "reason": "Left Te Pāti Māori and announced the new Te Tai Tokerau Party (registered Aug 2026); sat as an independent MP for the rest of the term", "replacement_party": "independent", "replacement": "Mariameno Kapa-Kingi", "date_entered": "2026-05-11", "change": "Independent gain; Te Pāti Māori loss", "src": W + "Te_Tai_Tokerau_Party"},
 ],
}
NOTES = {
 "Mariameno Kapa-Kingi": "Suspended by Te Pāti Māori 23 Oct 2025 and expelled 10 Nov 2025. Wikipedia's 54th Parliament changes table records her return to the party on 5 Dec 2025 (after she sought a High Court injunction, filed 4 Dec 2025); her own article says the High Court ruled the expulsion unlawful on 10 Mar 2026. Sources therefore differ on when she was formally reinstated. She left on 11 May 2026 to found the Te Tai Tokerau Party.",
 "Tākuta Ferris": "Expelled from Te Pāti Māori 10 Nov 2025; independent thereafter. Announced (21 Mar 2026) he would contest Te Tai Tonga as an independent in 2026.",
 "Jami-Lee Ross": "Left National 19 Oct 2018 amid a dispute with leader Simon Bridges; sat as an independent. In 2020 he co-led the new Advance New Zealand party (outside Parliament's party recognition) and lost Botany at the 2020 election.",
 "Meka Whaitiri": "Resigned from Labour 3 May 2023 and joined Te Pāti Māori; under the waka-jumping rules she remained recorded as an independent in Parliament for the rest of the term. Lost Ikaroa-Rāwhiti for Te Pāti Māori in 2023? -> No: see 2023 results (Cushla Tangaere-Manuel, Labour, won).",
 "Elizabeth Kerekere": "Resigned from the Green Party 5 May 2023 after a bullying complaint process; independent for the rest of the term.",
 "Gaurav Sharma": "Expelled from Labour 23 Aug 2022 after publicly alleging bullying in Parliament; resigned his seat 18 Oct 2022 to force the Hamilton West by-election, which he contested and lost.",
 "Darleen Tana": "Resigned from the Green Party 8 Jul 2024 amid allegations of migrant exploitation at her husband's business; expelled from Parliament 22 Oct 2024 under the Electoral (Integrity) Amendment Act 2018 (first use of the 'waka-jumping' law).",
 "Brendan Horan": "Expelled from the NZ First caucus 4 Dec 2012; sat as an independent; founded the NZ Independent Coalition (launched Jan 2014), which won no seats in 2014.",
 "Peter Dunne": "United Future was deregistered 31 May 2013 and re-registered 13 Aug 2013; Dunne was treated as an independent in the interim.",
 "Andrew Bayly": "Elected as a National list MP at the 2023 general election; won the Port Waikato by-election (25 Nov 2023) and became the electorate MP; Nancy Lu entered from the list.",
 "Winston Peters": None, "Jacinda Ardern": None,
}
NOTES["Meka Whaitiri"] = "Resigned from Labour 3 May 2023 to join Te Pāti Māori; recorded as an independent MP for the rest of the 53rd Parliament (she stood for Te Pāti Māori in Ikaroa-Rāwhiti in 2023 and lost to Labour's Cushla Tangaere-Manuel)."

ALIASES = {"Anahila Kanongata'a-Suisuiki": "anahila-kanongataa", "Chlöe Swarbrick": "chloe-swarbrick",
           "Harete Hipango": "harete-hipango-brownlie",  # same person; NZ First 2026 candidate (Whanganui)
           "Kahurangi Carter": "kahu-carter", "Neru Leavasa": "anae-neru-leavasa"}

def norm(n): return person_slug(n)

def build(n):
    c = P[n]
    el = json.load(open(os.path.join(ROOT, "data", "elections", f"{c['year']}.json")))
    existing = existing_person_slugs()
    members = {}
    order = []
    def add(name, party, seat, typ, entered, notes=""):
        k = norm(name)
        slug = ALIASES.get(name, k)
        m = {"name": name, "slug": slug, "party": party, "seat": seat, "type": typ, "entered": entered,
             "left": None, "left_reason": None, "party_changes": [], "notes": notes,
             "repo_folder": f"parties/{existing[slug]}/people/{slug}" if slug in existing else None}
        members.setdefault(k, []).append(m); order.append(m); return m
    for e in el["electorates"]:
        if c["year"] == 2023 and e["name"] == "Port Waikato":
            continue  # handled via Andrew Bayly list->electorate below
        add(e["winner"], e["party"], e["name"], "electorate", el["date"])
    lists = list_mps_from_wikitext(os.path.join(RAW, c["listsrc"] + ".wikitext"))
    for party, names in lists.items():
        for nm, rank in names:
            m = add(nm, party, None, "list", el["date"]); m["list_rank"] = rank
    def cur(name):
        k = norm(name)
        if k not in members:
            # try loose match on surname + first initial
            cands = [kk for kk in members if kk.split("-")[-1] == k.split("-")[-1] and kk[0] == k[0]]
            if len(cands) == 1: k = cands[0]
            else: raise KeyError(f"{n}: member not found: {name} {cands}")
        live = [m for m in members[k] if m["left"] is None]
        return live[-1] if live else members[k][-1]
    composition_at_election = {}
    for m in order:
        composition_at_election[m["party"]] = composition_at_election.get(m["party"], 0) + 1
    ch = MANUAL_CHANGES.get(n) or changes_table(os.path.join(RAW, c["art"] + ".wikitext"))
    ch = ch + EXTRA_CHANGES.get(n, [])
    ch = sorted(ch, key=lambda r: (r["date_vacated"] or "", 0 if r["seat"] != "List" else 1))
    changes = []
    if n == 54:
        b = cur("Andrew Bayly"); b["party_changes"] = []
        b["seat"] = "Port Waikato"; b["type"] = "list, then electorate (Port Waikato by-election 2023-11-25)"
        changes.append({"date": "2023-11-25", "description": "2023 Port Waikato by-election (delayed after ACT candidate Neil Christensen died during the campaign): National list MP Andrew Bayly won the seat (majority 11,432 over NZ First's Casey Costello), creating a third overhang seat (123 seats)."})
    for r in ch:
        inc, rep = r["incumbent"], r["replacement"]
        desc = f"{r['date_vacated']}: {inc} ({r['incumbent_party']}, {r['seat']}) – {r['reason']}"
        if rep and norm(rep) == norm(inc):
            m = cur(inc)
            m["party_changes"].append({"date": r["date_entered"], "from": r["incumbent_party"], "to": r["replacement_party"], "reason": r["reason"]})
            m["party_now_or_end"] = r["replacement_party"]
            desc += f" → now {r['replacement_party']}"
        elif r.get("italic_note") or "elected to electorate" in (r["reason"] or "").lower():
            # list MP who won a by-election: list place passes to next on list
            if not (n == 54 and inc == "Andrew Bayly"):
                pass
            add(rep, r["replacement_party"], None, "list", r["date_entered"], notes=f"Entered from the list replacing {inc}, who had won an electorate by-election.")
            desc += f" → list place filled by {rep} ({r['date_entered']})"
        else:
            m = cur(inc)
            m["left"] = r["date_vacated"]; m["left_reason"] = r["reason"]
            if rep:
                existing_m = None
                k = norm(rep)
                if k in members and any(x["left"] is None for x in members[k]):
                    existing_m = cur(rep)   # sitting list MP winning a by-election
                if existing_m:
                    existing_m["seat"] = r["seat"]; existing_m["type"] = f"list, then electorate ({r['seat']} by-election {r['date_entered']})"
                    desc += f" → by-election won by sitting list MP {rep} ({r['replacement_party']}) on {r['date_entered']}"
                else:
                    typ = "list" if r["seat"] == "List" else "electorate"
                    add(rep, r["replacement_party"], None if typ == "list" else r["seat"], typ, r["date_entered"],
                        notes="Entered at a by-election." if typ == "electorate" else f"Entered from the list replacing {inc}.")
                    desc += f" → replaced by {rep} ({r['replacement_party']}) on {r['date_entered']} [{r.get('change') or ''}]"
            else:
                desc += " → seat left vacant (no by-election required within 6 months of a general election)"
        changes.append({"date": r["date_vacated"], "description": desc.strip(), **({"source": r["src"]} if r.get("src") else {})})
    for m in order:
        if m["name"] in NOTES and NOTES[m["name"]]:
            m["notes"] = (m["notes"] + " " + NOTES[m["name"]]).strip()
        m.setdefault("party_now_or_end", m["party_changes"][-1]["to"] if m["party_changes"] else m["party"])
    def comp(ms):
        d = {}
        for m in ms: d[m["party_now_or_end"]] = d.get(m["party_now_or_end"], 0) + 1
        return dict(sorted(d.items(), key=lambda x: -x[1]))
    cdate = "2023-12-14" if n == 54 else c["start"]
    start_members = [m for m in order if m["entered"] <= cdate and (m["left"] is None or m["left"] > cdate)]
    # composition at start uses party at the time (party changes happen after start in every case here)
    cs = {}
    for m in start_members: cs[m["party"]] = cs.get(m["party"], 0) + 1
    end_members = [m for m in order if m["left"] is None]
    out = {"parliament": n, "election_year": c["year"], "start": c["start"], "end": c["end"],
           "end_note": "Date of dissolution." + (" Election day 7 Nov 2026." if n == 54 else ""),
           "composition_at_election": dict(sorted(composition_at_election.items(), key=lambda x: -x[1])),
           "composition_start": dict(sorted(cs.items(), key=lambda x: -x[1])),
           "composition_start_date": cdate,
           "composition_start_note": ("Counted on 14 Dec 2023, once the Port Waikato by-election result had flowed through (Nancy Lu sworn in from National's list); this matches the 123-seat House." if n == 54 else "Counted at the start of term (first sitting)."),
           "composition_now_or_end": comp(end_members),
           "total_start": len(start_members), "total_now_or_end": len(end_members),
           "members": order, "changes": changes,
           "sources": [W + c["art"], W + c["listsrc"], W + str(c["year"]) + "_New_Zealand_general_election"] + sorted({r["src"] for r in ch if r.get("src")})}
    return out

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "data", "parliaments"), exist_ok=True)
    for n in P:
        d = build(n)
        json.dump(d, open(os.path.join(ROOT, "data", "parliaments", f"{n}.json"), "w"), ensure_ascii=False, indent=1)
        print(n, d["total_start"], d["composition_start"], "->", d["total_now_or_end"], d["composition_now_or_end"], len(d["members"]))

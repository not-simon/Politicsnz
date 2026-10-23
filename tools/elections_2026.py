#!/usr/bin/env python3
"""Build data/elections/2026.json (upcoming election) from Wikipedia + policy.nz raw data."""
import json, os, sys, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elections_common import ROOT, person_slug
W = "https://en.wikipedia.org/wiki/"
e23 = json.load(open(os.path.join(ROOT, "data", "elections", "2023.json")))
pnz = []
for f in sorted(glob.glob(os.path.join(ROOT, "raw", "policy.nz", "electorates", "*-electorate.json"))):
    e = json.load(open(f))["election"]
    pnz.append({"name": e["title"].replace(" electorate", ""), "slug": os.path.basename(f).replace("-electorate.json", ""),
                "candidates_listed_on_policy_nz": len(e.get("candidates") or [])})
MAORI = {"Te Tai Tokerau", "Tāmaki Makaurau", "Hauraki-Waikato", "Waiariki", "Ikaroa-Rāwhiti", "Te Tai Hauāuru", "Te Tai Tonga"}
# policy.nz uses 'Mt'/'Kapiti' spellings; normalise for comparison with 2023 names
def key(n): return person_slug(n.replace("Mt ", "Mount "))
names26 = {key(e["name"]): e["name"] for e in pnz}
names23 = {key(e["name"]): e["name"] for e in e23["electorates"]}
new = sorted(names26[k] for k in names26 if k not in names23)
gone = sorted(names23[k] for k in names23 if k not in names26)
out = {
 "year": 2026, "date": "2026-11-07", "parliament": 55, "results": None,
 "status": "upcoming (data as of 23 Oct 2026; advance voting opens 26 Oct)",
 "seats": {"electorates": 71, "general_electorates": 64, "north_island_general": 48, "south_island_general": 16,
           "maori_electorates": 7, "list_seats": 49, "total_before_overhang": 120,
           "note": "After the 2023 Census the Representation Commission cut North Island general electorates from 49 to 48 (list seats up from 48 to 49). Draft boundaries 25 Mar 2025; final boundaries 8 Aug 2025."},
 "key_dates": [
  {"date": "2026-01-21", "event": "PM Christopher Luxon announces the election date (7 Nov 2026)"},
  {"date": "2026-08-06", "event": "Last day for registration of parties and logos; last day for Māori voters to change roll type"},
  {"date": "2026-08-07", "event": "Regulated election advertising period begins"},
  {"date": "2026-09-07", "event": "Candidate nominations open"},
  {"date": "2026-10-01", "event": "54th Parliament dissolved"},
  {"date": "2026-10-04", "event": "Writ day; official campaign, radio/TV advertising begins; last day to enrol ordinarily (later enrolments cast special votes)"},
  {"date": "2026-10-08", "event": "Nominations close (12 noon)"},
  {"date": "2026-10-21", "event": "Overseas voting begins"},
  {"date": "2026-10-25", "event": "Last day to enrol to vote (enrolment closes 13 days before polling day under the Electoral Amendment Act 2025)"},
  {"date": "2026-10-26", "event": "Advance voting begins (Labour Day)"},
  {"date": "2026-11-06", "event": "Advance and overseas voting ends; regulated advertising period ends"},
  {"date": "2026-11-07", "event": "Election day: polls open 9am-7pm; preliminary results from 7pm"},
  {"date": "2026-11-27", "event": "Official results declared"},
  {"date": "2026-12-03", "event": "Writ returned (subject to judicial recounts)"},
 ],
 "registered_parties_party_vote": [
  {"party": "national", "name": "National", "leader": "Christopher Luxon", "seats_2023": 48, "seats_at_dissolution": 48, "status": "government (coalition)"},
  {"party": "labour", "name": "Labour", "leader": "Chris Hipkins", "seats_2023": 34, "seats_at_dissolution": 34, "status": "opposition"},
  {"party": "green", "name": "Green", "leader": "Marama Davidson & Chlöe Swarbrick (co-leaders)", "seats_2023": 15, "seats_at_dissolution": 15, "status": "opposition"},
  {"party": "act", "name": "ACT", "leader": "David Seymour", "seats_2023": 11, "seats_at_dissolution": 11, "status": "government (coalition)"},
  {"party": "nz-first", "name": "NZ First", "leader": "Winston Peters", "seats_2023": 8, "seats_at_dissolution": 8, "status": "government (coalition)"},
  {"party": "te-pati-maori", "name": "Te Pāti Māori", "leader": "Debbie Ngarewa-Packer & Rawiri Waititi (co-leaders)", "seats_2023": 6, "seats_at_dissolution": 4, "status": "opposition"},
  {"party": "opportunity", "name": "The Opportunity Party (TOP)", "leader": "Qiulae Wong", "seats_2023": 0, "status": "extra-parliamentary"},
  {"party": "nz-loyal", "name": "New Zealand Loyal", "leader": "Kelvyn Alp", "seats_2023": 0, "status": "extra-parliamentary", "note": "Deregistered 26 Jul 2024 (non-renewal); listed again among the parties contesting the 2026 party vote (Wikipedia; policy.nz)"},
  {"party": "legalise-cannabis", "name": "Aotearoa Legalise Cannabis Party", "leader": "Maki Herbert & Michael Appleby", "seats_2023": 0, "status": "extra-parliamentary"},
  {"party": "nz-outdoors-freedom", "name": "NZ Outdoors & Freedom Party", "leader": "Sue Grey", "seats_2023": 0, "status": "extra-parliamentary", "note": "Part of the Freedoms NZ umbrella in 2023"},
  {"party": "vision-nz", "name": "Vision NZ", "leader": "Hannah Tamaki", "seats_2023": 0, "status": "extra-parliamentary", "note": "Part of the Freedoms NZ umbrella in 2023"},
  {"party": "animal-justice", "name": "Animal Justice Party", "leader": "Robert McNeil & Dannette Wereta", "seats_2023": 0, "status": "extra-parliamentary"},
  {"party": "conservative", "name": "Conservative Party NZ", "leader": "Helen Houghton", "seats_2023": 0, "status": "extra-parliamentary", "note": "Founded 2011 (Conservative Party), renamed New Conservative 2017, now Conservative Party NZ; 0.16% in 2023"},
  {"party": "womens-rights", "name": "Women's Rights Party", "leader": "Jill Ovens & Dawn Trenberth", "seats_2023": 0, "status": "extra-parliamentary"},
  {"party": "alliance", "name": "Alliance", "leader": "Victor Billot", "seats_2023": 0, "status": "extra-parliamentary"},
  {"party": "free-palestine", "name": "Free Palestine Party", "leader": "Paul Hopkinson", "seats_2023": 0, "status": "new (2026)"},
  {"party": "te-tai-tokerau-party", "name": "Te Tai Tokerau Party", "leader": "Mariameno Kapa-Kingi", "seats_2023": 0, "seats_at_dissolution": 0, "status": "new (2026); leader sat as an independent MP at dissolution"},
 ],
 "registered_parties_count": 17,
 "deregistered_since_2023": [
  {"name": "DemocracyNZ", "date": "2024-02-15"}, {"name": "Leighton Baker Party", "date": "2024-05-27"},
  {"name": "New Zealand Loyal", "date": "2024-07-26", "note": "later re-registered; contesting 2026"},
  {"name": "Democratic Alliance", "date": "2024-11-27"}, {"name": "New Nation Party", "date": "2025-01-29"},
  {"name": "Freedoms New Zealand", "date": "2025-05-01"}, {"name": "NewZeal", "date": "2026-03-31"}],
 "candidates": {
  "electorate_candidacies_policy_nz": sum(e["candidates_listed_on_policy_nz"] for e in pnz),
  "note": "Count of electorate candidacies listed on policy.nz (raw/policy.nz/electorates). The official Electoral Commission candidate totals (published after nominations closed 8 Oct 2026, with party lists) could not be fetched from elections.nz/electionresults.govt.nz from this environment (Incapsula/Cloudflare block), so this number is unverified. Wikipedia's 'Candidates ... by electorate' page was incomplete at retrieval (379 entries).",
  "by_electorate": pnz},
 "electorate_changes": {
  "new_or_renamed_2026": new, "abolished_or_renamed_from_2023": gone,
  "details": [
   "West Auckland: New Lynn, Kelston and Te Atatū reconfigured into Waitākere, Glendene and Henderson.",
   "South Auckland: Panmure-Ōtāhuhu becomes Ōtāhuhu (loses Panmure).",
   "Bay of Plenty: Tauranga and Bay of Plenty substantially redrawn; Bay of Plenty renamed Mount Maunganui.",
   "East Coast renamed East Cape.",
   "Lower North Island: Ōtaki, Mana and Ōhāriu reconfigured into Kenepuru and Kāpiti.",
   "Wellington: Wellington Central and Rongotai substantially redrawn and renamed Wellington North and Wellington Bays.",
   "Māori electorates stay at seven (boundaries adjusted)."],
 },
 "electoral_law_changes": [
  "Electoral Amendment Act 2025 (passed 16 Dec 2025): enrolment closes 13 days before polling day (no election-day enrolment); prisoners barred from voting; donation disclosure threshold raised from $5,000 to $6,000; ban on distributing food and most drinks near polling places.",
  "Electoral Commission defaults to emailing EasyVote information where it has a voter's email (announced 15 Jul 2026)."],
 "incumbent_government": {"pm": "Christopher Luxon", "parties": ["national", "act", "nz-first"], "arrangement": "coalition", "seats_at_dissolution": 67, "house_at_dissolution": 122},
 "mps_retiring": [
  {"name": "Duncan Webb", "party": "labour", "seat": "Christchurch Central", "announced": "2025-10-21"},
  {"name": "Paulo Garcia", "party": "national", "seat": "New Lynn", "announced": "2025-12-16"},
  {"name": "Maureen Pugh", "party": "national", "seat": "West Coast-Tasman", "announced": "2026-01-23"},
  {"name": "Celia Wade-Brown", "party": "green", "seat": "List", "announced": "2026-01-28"},
  {"name": "Judith Collins", "party": "national", "seat": "Papakura", "announced": "2026-01-28", "note": "resigned from Parliament 14 May 2026 to become President of the Law Commission"},
  {"name": "Shane Reti", "party": "national", "seat": "Whangārei", "announced": "2026-03-10"},
  {"name": "Brooke van Velden", "party": "act", "seat": "Tāmaki", "announced": "2026-03-24"},
  {"name": "Greg O'Connor", "party": "labour", "seat": "Ōhāriu", "announced": "2026-06-08", "note": "electorate abolished; did not seek a list place"},
  {"name": "Andrew Bayly", "party": "national", "seat": "Port Waikato", "announced": "2026-06-20"},
  {"name": "Chris Penk", "party": "national", "seat": "Kaipara ki Mahurangi", "announced": "2026-08-12", "note": "after an unsuccessful leadership move against Luxon cost him his portfolios"}],
 "mps_list_only": ["Megan Woods (labour)", "Nicola Willis (national)", "Deborah Russell (labour)", "Gerry Brownlee (national)", "Nancy Lu (national)"],
 "sources": [W + "2026_New_Zealand_general_election", "https://vote.nz/2026-general-election/about/overview/key-dates",
             W + "Party_lists_in_the_2026_New_Zealand_general_election", W + "Candidates_in_the_2026_New_Zealand_general_election_by_electorate",
             "https://policy.nz/2026", W + "Te_Tai_Tokerau_Party"],
}
json.dump(out, open(os.path.join(ROOT, "data", "elections", "2026.json"), "w"), ensure_ascii=False, indent=1)
print("new:", new); print("gone:", gone); print(out["candidates"]["electorate_candidacies_policy_nz"])

#!/usr/bin/env python3
"""Write README.md for the unregistered, electorate-only groups contesting the 2026 election
(folders created from policy.nz candidate data). Facts come from policy.nz electorate files and Wikipedia's
'Candidates in the 2026 New Zealand general election by electorate' / 'List of political parties in New Zealand'.
Usage: python3 -I tools/minor_parties_small_readmes.py"""
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
W_CAND = "https://en.wikipedia.org/wiki/Candidates_in_the_2026_New_Zealand_general_election_by_electorate"
W_LIST = "https://en.wikipedia.org/wiki/List_of_political_parties_in_New_Zealand"
W_2026 = "https://en.wikipedia.org/wiki/2026_New_Zealand_general_election"
PNZ = "https://policy.nz (downloaded electorate files in `raw/policy.nz/electorates/`)"
GROUPS = {
 "progressive-aotearoa-new-zealand": dict(name="Progressive Party of Aotearoa New Zealand (Progressive Aotearoa, PPANZ)",
   leader="Bruce Dyer", founded="2020",
   about="An unregistered party based on Prabhat Ranjan Sarkar's Progressive Utilization Theory (economic democracy; turning large businesses into co-operatives). It stood two electorate candidates in 2020 (Dyer won 50 votes in Nelson) and Dyer alone in 2023. In August 2026 it announced three candidates. Not to be confused with Jim Anderton's former Progressive Party.",
   cands=[("Bruce Dyer","Nelson","bruce-dyer"),("Michael Walker","Kāpiti","michael-walker"),("Kevin Rooke","West Coast-Tasman","kevin-rooke")],
   extra_src=["https://en.wikipedia.org/wiki/Progressive_Party_of_Aotearoa_New_Zealand", "https://www.progressiveparty.co.nz/ (party website, as listed by candidates on policy.nz; not fetched)"]),
 "money-free-party": dict(name="Money Free Party NZ", leader="Richard Osmaston (founder)", founded="2014",
   about="Part of the international Money Free movement, which advocates a resource-based economy in which all work is voluntary (inspired by Jacque Fresco's Venus Project). Never registered: it could not verify 500 members for 2014. Results: five electorate candidates in 2014; four in 2017 (293 votes in total); two in 2020 and two in 2023. Osmaston is a frequent mayoral candidate.",
   cands=[("Liam Anderson","Wellington Bays","liam-anderson"),("Richard Francis Osmaston","West Coast-Tasman","richard-francis-osmaston"),("Luke Beharrell","Whangārei","luke-beharrell")],
   extra_src=["https://en.wikipedia.org/wiki/Money_Free_movement"]),
 "nap": dict(name="Not A Party (NAP)", leader="Bob Wessex", founded="c. 2015 (earliest website post)",
   about="An unregistered 'anti-voting' group (Wikipedia lists its ideology as anti-voting; its website includes posts such as 'Democracy is the worst form of government'). Candidate Richard Goode contested Mana in 2023.",
   cands=[("Richard Goode","Kāpiti","richard-goode"),("Bob Wessex","Kenepuru","bob-wessex")],
   extra_src=["https://www.nap.org.nz/people/ (party website, as cited by Wikipedia; not fetched)"]),
 "peoples-party-new-zealand": dict(name="People's Party New Zealand", leader="not stated in our sources", founded="unknown",
   about="Two electorate candidates in South Auckland seats. A 'People's Party NZ Inc.' was originally allocated $78,887 of broadcasting money by the Electoral Commission on 7 May 2026, but its amended allocation was $0 because it did not become a registered party. Our sources do not establish whether it is connected to the earlier New Zealand People's Party (2015–19, see ../nz-peoples-party/).",
   cands=[("Alani Fisher Taione","Māngere","alani-fisher-taione"),("Eseta Haunga","Ōtāhuhu","eseta-haunga")], extra_src=[W_2026]),
 "balance-new-zealand": dict(name="Balance New Zealand", leader="—", founded="unknown",
   about="A single-candidate label in 2026.", cands=[("Juan Charles Coffey","Whanganui","juan-charles-coffey")], extra_src=[]),
 "build-the-nation": dict(name="Build the Nation", leader="—", founded="unknown",
   about="A single-candidate label in 2026 (Wikipedia lists Richard McIntosh under 'Build the Nation'; policy.nz lists him as an independent).",
   cands=[("Richard McIntosh","Northland","richard-mcintosh")], extra_src=[]),
 "nz-economic-euthenics-party": dict(name="(NZ) Economic Euthenics", leader="Tubby Hansen", founded="—",
   about="The label used by perennial Christchurch candidate Tubby Hansen, who contested Wigram in 2023.",
   cands=[("Tubby Hansen","Christchurch Central","tubby-hansen")], extra_src=[]),
 "independent-taranaki": dict(name="Independent Taranaki", leader="—", founded="—",
   about="A single-candidate label in 2026 (policy.nz lists the candidate as an independent).",
   cands=[("Rusty Kane","New Plymouth","rusty-kane")], extra_src=[]),
 "jobseeker-party": dict(name="Jobseeker Party", leader="—", founded="unknown", about="A single-candidate label in 2026.",
   cands=[("Kelso Papali'i","Henderson","kelso-papalii")], extra_src=[]),
 "new-world-order-mccann-party": dict(name="New World Order McCann Party", leader="—", founded="—",
   about="A single-candidate label in 2026; Wikipedia links it to the long-running joke 'New World Order Party' label.",
   cands=[("Nathan Lee Couper","Hamilton West","nathan-lee-couper")], extra_src=[]),
 "socialist-equality-group": dict(name="Socialist Equality Group", leader="—", founded="unknown", about="A single-candidate label in 2026.",
   cands=[("Tom Petterson","Hutt South","tom-petterson")], extra_src=[]),
 "te-pati-hira": dict(name="Te Pāti Hira", leader="—", founded="unknown", about="A single-candidate label in 2026.",
   cands=[("Jared Warren Gardner","Wairarapa","jared-warren-gardner")], extra_src=[]),
 "your-pic-party": dict(name="Your PIC Party", leader="—", founded="unknown", about="A single-candidate label in 2026.",
   cands=[("Karl Barkley","Te Tai Tokerau","karl-barkley")], extra_src=[]),
}
for slug, g in GROUPS.items():
    d = os.path.join(ROOT, "parties", slug)
    os.makedirs(d, exist_ok=True)
    rows = "\n".join(f"| [{n}](people/{s}/) | {e} |" if os.path.isdir(os.path.join(d, "people", s)) else f"| {n} | {e} |" for n, e, s in g["cands"])
    srcs = [PNZ, W_CAND, W_LIST] + g["extra_src"]
    md = f"""# {g['name']}

| | |
|---|---|
| **Status (Oct 2026)** | **Unregistered** — electorate candidate(s) only; cannot contest the party vote or have a list |
| **Leader** | {g['leader']} |
| **Founded** | {g['founded']} |
| **Seats** | None |

## About

{g['about']}

Wikipedia notes that a candidate standing under a party name "is not necessarily an indication that the party exists
beyond that single candidate". We found no independent coverage of this group's programme beyond what is listed here;
where the candidate supplied a statement to policy.nz it appears in their person profile.

## 2026 electorate candidates

| Candidate | Electorate |
|---|---|
{rows}

## Election results

No previous results recorded in our sources unless stated above. 2026 results: pending (election 7 November 2026).

## Sources

""" + "\n".join(f"{i}. {s}" for i, s in enumerate(srcs, 1)) + "\n"
    open(os.path.join(d, "README.md"), "w").write(md)
    print("wrote", slug)

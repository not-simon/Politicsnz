#!/usr/bin/env python3
"""Build parties/<party>/people/README.md index for every party except National and Labour.
Groups: Current MPs (54th Parliament) / 2026 candidates / Former MPs. Reads each <slug>/person.json."""
import json, os, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from people_others_build import PNAME, STATUS
CUR = {"current-mp", "current-mp-standing-2026", "current-mp-retiring"}
def cell(s): return (s or "").replace("|", "/").replace("\n", " ")
n_total = 0
for pdir in sorted((ROOT / "parties").iterdir()):
    if pdir.name in ("national", "labour") or not (pdir / "people").is_dir(): continue
    people = []
    for d in sorted((pdir / "people").iterdir()):
        if not (d / "person.json").exists(): continue
        p = json.loads((d / "person.json").read_text()); p["_dir"] = d.name; people.append(p)
    if not people: continue
    n_total += len(people)
    groups = {"Current MPs (54th Parliament)": [], "2026 candidates": [], "Former MPs": [], "Other": []}
    for p in people:
        st = p.get("status", "candidate-2026")
        if st in CUR: groups["Current MPs (54th Parliament)"].append(p)
        elif st == "candidate-2026": groups["2026 candidates"].append(p)
        elif p.get("parliaments") or st in ("former-mp", "deceased"): groups["Former MPs"].append(p)
        else: groups["Other"].append(p)
    def key(p): return (p.get("list_rank_2026") or 999, p.get("name", ""))
    L = [f"# {PNAME.get(pdir.name, pdir.name)} — people", "",
         f"Profiles of {len(people)} people associated with {PNAME.get(pdir.name, pdir.name)}: MPs who served in the 50th–54th Parliaments (2011–2026) "
         "and every 2026 candidate listed on policy.nz. Status is as of 23 October 2026 (election day 7 November 2026). "
         "Each person sits under their current or most recent party. Click a name for the full profile.", ""]
    for g, ps in groups.items():
        if not ps: continue
        ps.sort(key=key if g != "Former MPs" else (lambda p: p.get("name", "")))
        L += [f"## {g} ({len(ps)})", "", "| | Name | Status | 2026 electorate | 2026 list # | Roles / notes |", "|---|---|---|---|---|---|"]
        for p in ps:
            img = f'<img src="{p["_dir"]}/photo.jpg" width="48">' if (pdir / "people" / p["_dir"] / "photo.jpg").exists() else ""
            roles = "; ".join(p.get("roles", [])[:3])
            if not roles and p.get("questionnaire_2026", {}).get("Before politics"): roles = "Before politics: " + p["questionnaire_2026"]["Before politics"]
            if g == "Former MPs" and p.get("status_detail"): roles = (roles + " — " if roles else "") + p["status_detail"].split(". ")[0]
            L.append(f"| {img} | [{cell(p.get('name'))}]({p['_dir']}/README.md) | {STATUS.get(p.get('status'), p.get('status'))} | "
                     f"{cell(p.get('electorate_2026') or '')} | {p.get('list_rank_2026') or ''} | {cell(roles)} |")
        L.append("")
    L += ["_Built by `tools/people_others_index.py` from each profile's `person.json`. Candidate details come from policy.nz; MP histories from Wikipedia and the sources cited in each profile._", ""]
    (pdir / "people" / "README.md").write_text("\n".join(L))
    print("index", pdir.name, len(people))
print("total", n_total)

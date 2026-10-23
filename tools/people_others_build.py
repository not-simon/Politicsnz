#!/usr/bin/env python3
"""Build person.json + README.md for non-National/Labour people from hand-written content files.
Content file: raw/people/others/content/<slug>.md  =  '---json\n{person fields incl. "folder"}\n---\n<markdown sections>'
- Merges fields into existing person.json (keeps policy.nz fields such as questionnaire_2026, photo_* if photo exists).
- Downloads Wikipedia lead image if no photo.jpg (fields photo_file) via tools/people_others_photo.py.
- README = title, photo, quick facts, content sections, existing GENERATED:2026-candidacy block (verbatim), Sources.
Usage: python3 tools/people_others_build.py [slug ...]"""
import json, os, re, sys, glob, subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
C = ROOT / "raw/people/others/content"
START, END = "<!-- GENERATED:2026-candidacy START -->", "<!-- GENERATED:2026-candidacy END -->"
STATUS = {"current-mp": "Current MP", "candidate-2026": "2026 candidate", "current-mp-standing-2026": "MP (54th Parliament), standing in 2026",
          "current-mp-retiring": "MP (54th Parliament), retiring at 2026 election", "former-mp": "Former MP", "deceased": "Deceased",
          "party-official": "Party official"}
PNAME = {"green": "Green Party", "act": "ACT New Zealand", "nz-first": "New Zealand First", "te-pati-maori": "Te Pāti Māori",
         "opportunity": "The Opportunity Party (TOP)", "independent": "Independent", "united-future": "United Future", "mana": "Mana Movement",
         "advance-nz": "Advance New Zealand", "te-tai-tokerau-party": "Te Tai Tokerau Party", "national": "National", "labour": "Labour",
         "nz-independent-coalition": "NZ Independent Coalition", "conservative": "Conservative Party", "vision-nz": "Vision NZ",
         "nz-loyal": "New Zealand Loyal", "alliance": "Alliance", "free-palestine": "Free Palestine", "womens-rights": "Women's Rights Party",
         "nz-outdoors-freedom": "NZ Outdoors & Freedom Party", "legalise-cannabis": "Aotearoa Legalise Cannabis Party",
         "animal-justice": "Animal Justice Party", "newzeal": "NewZeal", "freedoms-nz": "Freedoms NZ", "internet-party": "Internet Party",
         "mana-movement": "Mana Movement", "democracynz": "DemocracyNZ", "values": "Values Party", "māori-party": "Māori Party"}
def pn(p): return PNAME.get(p, p)
def build(f):
    raw = f.read_text(); m = re.match(r"---json\n(.*?)\n---\n(.*)", raw, re.S)
    meta, body = json.loads(m.group(1)), m.group(2).strip()
    folder = meta.pop("folder"); slug = meta["slug"]; photo_file = meta.pop("photo_file", None)
    d = ROOT / "parties" / folder / "people" / slug; d.mkdir(parents=True, exist_ok=True)
    pj = d / "person.json"; ex = json.loads(pj.read_text()) if pj.exists() else {}
    if photo_file and not (d / "photo.jpg").exists() and PHOTOS:
        out = subprocess.run([sys.executable, str(ROOT / "tools/people_others_photo.py"), photo_file, str(d)], capture_output=True, text=True)
        if out.returncode == 0: meta.update({k: v for k, v in json.loads(out.stdout).items() if k != "skipped"})
        else: print("PHOTO FAIL", slug, out.stderr[-300:], file=sys.stderr)
    elif (d / "photo.jpg").exists() and not ex.get("photo_source") and photo_file:
        pass
    srcs = list(dict.fromkeys(meta.pop("sources", []) + ex.get("sources", [])))
    merged = {**ex, **meta}; merged["sources"] = srcs
    if (d / "photo.jpg").exists(): merged.setdefault("photo", "photo.jpg")
    pj.write_text(json.dumps(merged, ensure_ascii=False, indent=1))
    rd = d / "README.md"; old = rd.read_text() if rd.exists() else ""
    gm = re.search(re.escape(START) + ".*?" + re.escape(END), old, re.S)
    L = [f"# {merged['name']}", ""]
    if (d / "photo.jpg").exists():
        L += [f'<img src="photo.jpg" width="200" align="right" alt="{merged["name"]}">', ""]
    q = [("Party (current/most recent)", pn(merged["party"])), ("Status", STATUS.get(merged["status"], merged["status"]))]
    if merged.get("party_history"):
        q.append(("Party history", "; ".join(f"{pn(h['party'])} ({h.get('from','')}–{h.get('to') or 'present'})" for h in merged["party_history"])))
    if merged.get("parliaments"): q.append(("Parliaments (50th–54th)", ", ".join(map(str, merged["parliaments"]))))
    if merged.get("first_elected"): q.append(("First elected", str(merged["first_elected"])))
    if merged.get("electorates"): q.append(("Electorates held", ", ".join(merged["electorates"])))
    if merged.get("roles"): q.append(("Key roles", "<br>".join(merged["roles"])))
    if merged.get("born"): q.append(("Born", merged["born"]))
    if merged.get("died"): q.append(("Died", merged["died"]))
    if merged.get("electorate_2026") or merged.get("list_rank_2026"):
        q.append(("2026 election", ", ".join(x for x in [merged.get("electorate_2026") and f"contesting {merged['electorate_2026']}",
                  merged.get("list_rank_2026") and f"list #{merged['list_rank_2026']}"] if x)))
    if merged.get("wikipedia"): q.append(("Wikipedia", f"[{merged['wikipedia'].rsplit('/',1)[-1].replace('_',' ')}]({merged['wikipedia']})"))
    L += ["| | |", "|---|---|"] + [f"| **{k}** | {v} |" for k, v in q] + [""]
    if merged.get("photo_source") and "policy.nz" not in merged.get("photo_credit", "") :
        L += [f"<sub>Photo: {merged.get('photo_credit') or 'unknown'} — {merged.get('photo_license') or 'see source'} — [source]({merged['photo_source']})</sub>", ""]
    elif merged.get("photo_source"):
        L += [f"<sub>Photo: {merged.get('photo_credit')} — [source]({merged['photo_source']})</sub>", ""]
    L += [body, ""]
    if gm: L += [gm.group(0), ""]
    L += ["## Sources", ""] + [f"- {s}" for s in srcs] + [""]
    rd.write_text("\n".join(L))
    return folder, slug
PHOTOS = "--photos" in sys.argv
targets = [a for a in sys.argv[1:] if not a.startswith("--")]
for f in sorted(C.glob("*.md")):
    if targets and f.stem not in targets: continue
    print("built", *build(f))

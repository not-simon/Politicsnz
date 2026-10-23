#!/usr/bin/env python3
"""Build promise-reliability scorecards for ACT and NZ First from data/promises/<party>.json
and write them into parties/<party>/track-record.md between
<!-- GENERATED:scorecard START --> and <!-- GENERATED:scorecard END --> markers.
Usage: python3 tools/record_act_nzf_scorecard.py   (prints the tables; rewrites the marked blocks if present)"""
import json, os, re
from collections import Counter, OrderedDict
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
STATUSES = ["kept", "partially-kept", "broken", "abandoned", "in-progress", "not-yet-due"]
def term(entry):
    if entry["status"] == "not-yet-due":
        return "2026"
    if entry["made"].lower().startswith("long-standing"):
        return "long-standing"
    years = [int(y) for y in re.findall(r"(?<!\d)(?:19|20)\d\d(?!\d)", entry["made"])]
    y = max(years) if "coalition agreement" in entry["made"] else min(years)
    for start, label in [(2026, "2026"), (2023, "2023"), (2020, "2020"), (2017, "2017"), (2014, "2014"), (2011, "2011")]:
        if y >= start:
            return label
    return "2011"
def table(party):
    data = json.load(open(os.path.join(ROOT, "data", "promises", party + ".json")))
    groups = OrderedDict()
    for t in ["2011", "2014", "2017", "2020", "2023", "long-standing", "2026"]:
        groups[t] = Counter()
    for e in data:
        groups[term(e)][e["status"]] += 1
    tot = Counter()
    lines = ["| Promises made at | " + " | ".join(STATUSES) + " | Total | Reliability* |",
             "|---|" + "---|" * (len(STATUSES) + 2)]
    def rel(c):
        resolved = c["kept"] + c["partially-kept"] + c["broken"] + c["abandoned"]
        if not resolved:
            return "–"
        return "%d%%" % round(100 * (c["kept"] + 0.5 * c["partially-kept"]) / resolved)
    for t, c in groups.items():
        if not sum(c.values()):
            continue
        tot.update(c)
        label = t if t in ("long-standing",) else ("%s (upcoming)" % t if t == "2026" else "%s election/term" % t)
        lines.append("| %s | " % label + " | ".join(str(c[s]) for s in STATUSES) + " | %d | %s |" % (sum(c.values()), rel(c)))
    lines.append("| **All** | " + " | ".join("**%d**" % tot[s] for s in STATUSES) + " | **%d** | **%s** |" % (sum(tot.values()), rel(tot)))
    lines.append("")
    lines.append("\\*Reliability = (kept + ½ × partially-kept) ÷ (kept + partially-kept + broken + abandoned). In-progress and not-yet-due items are excluded. "
                 "This is a rough indicator over a curated sample of headline promises, not a full audit of every manifesto line.")
    return "\n".join(lines), tot
if __name__ == "__main__":
    for party in ["act", "nz-first"]:
        md, tot = table(party)
        print("##", party); print(md); print()
        path = os.path.join(ROOT, "parties", party, "track-record.md")
        if os.path.exists(path):
            s = open(path).read()
            new = re.sub(r"(<!-- GENERATED:scorecard START -->\n).*?(\n<!-- GENERATED:scorecard END -->)",
                         lambda m: m.group(1) + md + m.group(2), s, flags=re.S)
            if new != s:
                open(path, "w").write(new); print("updated", path)

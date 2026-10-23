#!/usr/bin/env python3
"""Extract (party, wiki-link) MP pairs from cached 50th-54th Parliament wikitext (seating plans, member tables, changes)."""
import re, json, glob, os, collections
D = os.path.join(os.path.dirname(__file__), "..", "raw", "people", "others")
out = collections.defaultdict(lambda: collections.defaultdict(set))
for n, f in [(50,"50th"),(51,"51st"),(52,"52nd"),(53,"53rd"),(54,"54th")]:
    t = open(f"{D}/{f}_New_Zealand_Parliament.wikitext").read()
    for m in re.finditer(r"\{\{[Pp]arty colou?r cell\|([^}]+)\}\}\s*'*\[\[([^|\]]+)", t):
        out[m.group(2).strip()][n].add(m.group(1).strip())
    for m in re.finditer(r"\{\{Party name with colou?r\|([^}]+)\}\}\s*\n\|\s*'*\[\[([^|\]]+)", t):
        out[m.group(2).strip()][n].add(m.group(1).strip())
    # member tables: party color cell row, then link lines
    for row in t.split("\n|-"):
        pm = re.search(r"\{\{[Pp]arty colou?r cell\|([^}]+)\}\}", row)
        if not pm: continue
        for lm in re.finditer(r"^\|\s*\[\[([^|\]]+)", row, re.M):
            if not lm.group(1).startswith(("File:", "Image:")):
                out[lm.group(1).strip()][n].add(pm.group(1).strip()); break
res = {k: {str(n): sorted(v) for n, v in d.items()} for k, d in out.items()}
json.dump(res, open(f"{D}/members_extracted.json", "w"), indent=1, ensure_ascii=False)
print(len(res))

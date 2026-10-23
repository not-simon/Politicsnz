#!/usr/bin/env python3
"""Parse Wikipedia 'Party lists in the 2026 New Zealand general election' into raw/people/others/lists2026.json"""
import re, json, os
D = os.path.join(os.path.dirname(__file__), "..", "raw", "people", "others")
t = open(f"{D}/Party_lists_in_the_2026_New_Zealand_general_election.wikitext").read()
out = []; party = None
for line in t.split("\n"):
    m = re.match(r"^===\s*(.+?)\s*===", line)
    if m: party = m.group(1); continue
    if "NZ party list candidate" in line:
        line = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", lambda m: "[[" + m.group(1) + "\x00" + m.group(2) + "]]", line)
        f = {}
        for kv in line.split("|"):
            if "=" in kv:
                k, v = kv.split("=", 1); f[k.strip()] = v.strip().rstrip("}").strip()
        full = f.get("fullname", "")
        lm = re.search(r"\[\[([^\x00\]]+)(?:\x00([^\]]+))?\]\]", full)
        name = (lm.group(2) or lm.group(1)) if lm else re.sub(r"<.*", "", full).strip()
        out.append({"party": party, "rank": f.get("rank"), "name": name, "wiki": lm.group(1) if lm else None,
                    "contesting": re.sub(r"\[\[(?:[^\x00\]]+\x00)?([^\]]+)\]\]", r"\1", f.get("contesting", "")),
                    "incumbency": f.get("incumbency"), "previousparty": f.get("previousparty")})
json.dump(out, open(f"{D}/lists2026.json", "w"), indent=1, ensure_ascii=False)
print(len(out))

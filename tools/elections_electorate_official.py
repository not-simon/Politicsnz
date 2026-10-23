#!/usr/bin/env python3
"""Parse official electorate results (candidate votes, majority, party votes) from Wikipedia electorate articles
(raw/elections/electorates/*.wikitext; their MMP election boxes cite the Electoral Commission's official count pages).
Writes raw/elections/electorates_official.json: {year: {electorate: {...}}}."""
import os, re, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mwparserfromhell as mw
from elections_common import RAW, clean, party_slug
YEARS = {2008, 2011, 2014, 2017, 2020, 2023}
def num(v):
    v = clean(v).replace(",", "").strip()
    m = re.match(r"^\d+", v); return int(m.group()) if m else None
out = {}
for f in sorted(glob.glob(os.path.join(RAW, "electorates", "*.wikitext"))):
    meta = json.load(open(f.replace(".wikitext", ".meta.json")))
    txt = open(f).read()
    txt = re.sub(r"<ref[^>/]*/>", "", txt); txt = re.sub(r"<ref[^>]*>.*?</ref>", "", txt, flags=re.S)
    txt = re.sub(r"<!--.*?-->", "", txt, flags=re.S)
    parts = re.split(r"\{\{\s*MMP election box begin", txt)
    for p in parts[1:]:
        head = p[:600]
        m = re.search(r"\[\[(\d{4}) New Zealand general election(?:\|(\d{4}) general election)?", head)
        if not m: continue
        year = int(m.group(2) or m.group(1))   # display text wins (some articles mislink the year)
        if year not in YEARS: continue
        tm = re.search(r"general election\]\]\s*:\s*(\[\[[^\]]*\]\]|[^\n}|<\[]+)", head)
        el = clean(tm.group(1)).strip() if tm else meta["title"].replace(" (New Zealand electorate)", "")
        end = re.search(r"\{\{\s*Election box end|\{\{\s*MMP election box end|\n==", p)
        body = p[: end.start()] if end else p
        code = mw.parse("{{X" + body)
        cands, maj, partyv = [], None, {}
        for t in code.filter_templates(recursive=False):
            n = str(t.name).strip().lower()
            g = lambda k: str(t.get(k).value) if t.has(k) else ""
            if not n.startswith("mmp election box"): continue
            kind = n.replace("mmp election box", "").strip()
            if kind.startswith("majority"):
                maj = num(g("votes")); continue
            if kind in ("informal vote", "total vote", "turnout"): continue
            pname = clean(g("party"))
            try: ps = party_slug(pname) if pname else ("independent" if "independent" in kind else None)
            except KeyError: ps = pname
            cand = clean(g("candidate"))
            v = num(g("votes")) if t.has("votes") else None
            if cand and v is not None: cands.append({"candidate": cand, "party": ps, "votes": v, "kind": kind})
            pv = num(g("party votes")) if t.has("party votes") else None
            if pv is not None and ps: partyv[ps] = partyv.get(ps, 0) + pv
        cands.sort(key=lambda c: -c["votes"])
        out.setdefault(year, {})[el] = {"article": meta["url"], "majority": maj, "candidates": cands, "party_votes": partyv,
                                        "computed_majority": cands[0]["votes"] - cands[1]["votes"] if len(cands) > 1 else None}
json.dump(out, open(os.path.join(RAW, "electorates_official.json"), "w"), ensure_ascii=False, indent=1)
for y in sorted(out): print(y, len(out[y]))

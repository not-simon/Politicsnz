#!/usr/bin/env python3
"""Probe Wikipedia for articles on never-MP 2026 Labour candidates (cached).
Writes raw/people/labour/work/cand_wiki.json: {slug: {title, first_para}}."""
import json, os, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import people_labour_wiki as W
ROOT = pathlib.Path(__file__).resolve().parent.parent
roster = {e['slug'] for e in json.load(open(ROOT/'raw/people/labour/work/roster_final.json'))}
out = {}
for slug in sorted(os.listdir(ROOT/'parties/labour/people')):
    if slug in roster or slug == 'README.md':
        continue
    pj = json.load(open(ROOT/'parties/labour/people'/slug/'person.json'))
    name = pj['name']
    hits = []
    for t in [name, name + ' (politician)', name + ' (New Zealand politician)']:
        r = W.raw(t)
        wt = r['wikitext']
        if wt and re.search(r'New Zealand|Aotearoa', wt[:6000]) and not wt.lower().startswith('{{disambig'):
            hits.append((r['title'], len(wt)))
    out[slug] = {'name': name, 'hits': hits}
    print(slug, hits, flush=True)
json.dump(out, open(ROOT/'raw/people/labour/work/cand_wiki.json', 'w'), indent=1, ensure_ascii=False)

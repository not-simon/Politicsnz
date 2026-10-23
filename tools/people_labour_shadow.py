#!/usr/bin/env python3
"""Parse the current Labour shadow cabinet table from Wikipedia 'Shadow Cabinet of Chris Hipkins'
-> raw/people/labour/work/shadow_current.json {slug: {rank, portfolios}}"""
import json, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from people_labour_wiki import raw, ROOT
from people_labour_parse import clean
from people_labour_build import slugify
wt = raw('Shadow Cabinet of Chris Hipkins')['wikitext']
tab = wt[wt.find('{|'):]; tab = tab[:tab.find('\n|}')]
out = {}
for row in tab.split('\n|-')[1:]:
    cells = [c for c in re.split(r'\n\|\s*|\|\|', row) if c.strip()]
    rank = next((c.strip() for c in cells if c.strip().isdigit()), None)
    m = re.search(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]\s*\|\|(.*)', row, re.S)
    if not m: continue
    name = re.sub(r'\s*\(.*?\)', '', m.group(2) or m.group(1))
    ports = [clean(p) for p in re.split(r'<br\s*/?>|\n', m.group(3)) if clean(p)]
    slug = {'anahila-kanongataa-suisuiki': 'anahila-kanongataa', 'neru-leavasa': 'anae-neru-leavasa'}.get(slugify(name), slugify(name))
    out[slug] = {'name': name, 'rank': int(rank) if rank else None, 'portfolios': ports}
(ROOT / 'raw/people/labour/work/shadow_current.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
for k, v in out.items(): print(v['rank'], k, '; '.join(v['portfolios']))

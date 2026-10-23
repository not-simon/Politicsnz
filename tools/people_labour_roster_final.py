#!/usr/bin/env python3
"""Step 2: turn roster.json into roster_final.json [{title, slug, labour_parls}], mapping to existing folders."""
import json, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from people_labour_build import slugify, PEOPLE
from people_labour_wiki import ROOT
W = ROOT / 'raw' / 'people' / 'labour' / 'work'
r = json.loads((W / 'roster.json').read_text())
EXCLUDE = {'Kate Wilkinson (politician)'}  # National MP; false positive from a succession box
OVERRIDE = {"Anahila Kanongata'a-Suisuiki": 'anahila-kanongataa', 'Neru Leavasa': 'anae-neru-leavasa'}
existing = {d.name for d in PEOPLE.iterdir() if d.is_dir()}
out = []
for t, v in sorted(r.items()):
    if t in EXCLUDE: continue
    s = OVERRIDE.get(t) or slugify(re.sub(r'\s*\(.*?\)', '', t))
    out.append({'title': t, 'slug': s, 'labour_parls': v['labour_parls'], 'existing_folder': s in existing})
(W / 'roster_final.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(out), 'MPs;', sum(e['existing_folder'] for e in out), 'with existing 2026-candidate folders')
mp_slugs = {e['slug'] for e in out}
print('2026 candidates never MPs:', len(existing - mp_slugs), sorted(existing - mp_slugs))

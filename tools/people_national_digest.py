#!/usr/bin/env python3
"""Research digest: infobox offices, conscience votes, official 2026 rank and article text (citations shortened to domains)."""
import json, os, re, subprocess, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
d = json.load(open(os.path.join(ROOT, 'raw', 'people', 'national', 'derived.json')))
rk = json.load(open(os.path.join(ROOT, 'raw', 'people', 'national', 'ec', 'national-list-2026.json')))
maxc = int(os.environ.get('MAXC', '18000'))
for s in sys.argv[1:]:
    v = d.get(s, {})
    print(f"##### {s} born={v.get('born')} {v.get('birth_place')} died={v.get('died')} rank2026={rk.get(s)} parl={v.get('parliaments_50_54')}")
    for o in v.get('offices', []): print('  OFF', o['office'] or o['constituency'], '|', o['term_start'], '-', o['term_end'], '|', o['majority'] or '')
    print('  VOTES', v.get('votes'))
    t = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'tools', 'people_national_read.py'), s], capture_output=True, text=True).stdout
    t = re.sub(r'⟨https?://(www\.)?([^/⟩]*)[^⟩]*⟩', r'⟨\2⟩', t)
    print(t[:maxc])

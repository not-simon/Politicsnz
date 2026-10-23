#!/usr/bin/env python3
"""Step 1: candidate roster of Labour MPs in the 50th-54th Parliaments.
Collect person links from the Members/changes sections of each Parliament article, fetch each
linked article, and keep those whose 'New Zealand Parliament' table has a Labour row for 50th-54th."""
import json, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from people_labour_wiki import raw, ROOT
from people_labour_parse import parlbox
OUT = ROOT / 'raw' / 'people' / 'labour' / 'work'
ORD = {50: '50th', 51: '51st', 52: '52nd', 53: '53rd', 54: '54th'}
links = {}
SKIP = re.compile(r'(Parliament|Party|party|election|electorate|Government|Cabinet|Minister|Speaker|List of|Leader|Whip|Category|File:|Image:|New Zealand$|Labour$|National$|Green|ACT|Māori|Mana|United Future|Coalition|House|Wikipedia|Template|\(New Zealand\)|by-election|Committee|Act \d|Bill)')
for n, o in ORD.items():
    t = raw(f'{o} New Zealand Parliament')['wikitext']
    a = t.find('==Members') if '==Members' in t else t.find('== Members')
    b = t.find('== Seating plan')
    sect = t[a:b]
    for m in re.finditer(r'\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]', sect):
        tt = m.group(1).strip()
        if SKIP.search(tt) or len(tt) < 4: continue
        links.setdefault(tt, set()).add(n)
print(len(links), 'candidate links', file=sys.stderr)
res = {}
for i, tt in enumerate(sorted(links)):
    w = raw(tt); wt = w['wikitext']
    if 'New Zealand Labour Party' not in wt and 'Labour' not in wt: continue
    rows = {}
    for r in parlbox(wt):
        tm = re.match(r'(\d+)', r.get('term', ''))
        if tm and int(tm.group(1)) in ORD:
            rows.setdefault(int(tm.group(1)), []).append(r.get('party'))
    for n, o in ORD.items():
        for m in re.finditer(r'\[\[%s New Zealand Parliament\|%s\]\]' % (o, o), wt):
            seg = wt[m.end(): m.end() + 600].split('|-')[0]
            if 'Labour' in seg: rows.setdefault(n, []).append('New Zealand Labour Party')
    lab = [n for n, ps in rows.items() if any(p and 'Labour' in p for p in ps)]
    if lab:
        res[tt] = {'parliaments_linked': sorted(links[tt]), 'rows': rows, 'labour_parls': sorted(lab)}
json.dump(res, open(OUT / 'roster.json', 'w'), ensure_ascii=False, indent=1)
print(len(res), 'labour MPs')

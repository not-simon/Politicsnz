#!/usr/bin/env python3
"""Render the promise-by-promise tables + scorecard of parties/national/track-record.md from
data/promises/national.json (between <!-- GENERATED:promises START/END --> markers).
Run after tools/record_national_build.py:  python3 -I tools/record_national_md.py"""
import json, os, re, collections
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
P = json.load(open(os.path.join(ROOT, 'data/promises/national.json')))
ICON = {'kept': '✅ kept', 'partially-kept': '🟡 partially kept', 'broken': '❌ broken', 'abandoned': '⛔ abandoned',
        'in-progress': '⏳ in progress', 'not-yet-due': '🗳️ not yet due'}

def term(m):
    if m.startswith('2026'): return '2026'
    for k, v in [('2008', 'A'), ('2011', 'B'), ('2013', 'C'), ('2014', 'C'), ('2017', 'D'), ('2019', 'D'), ('2020', 'D')]:
        if m.startswith(k): return v
    return 'E'
TITLES = {'A': 'Promises made in 2008 (Key government, 2008–11 and after)',
          'B': '2011 campaign (Key government, 2011–14)',
          'C': '2014 campaign (Key/English government, 2014–17)',
          'D': '2017 and 2020 campaigns (National lost office — untested)',
          'E': '2023 campaign and coalition agreements (Luxon government, 2023–26)',
          '2026': '2026 campaign (not yet due — for reference)'}

def link(u):
    if u.startswith('http'):
        host = re.sub(r'^https?://(www\.|amp\.)?', '', u).split('/')[0]
        return f'[{host}]({u})'
    return f'[{u}](../../{u})'

def cell(t): return t.replace('|', '\\|').replace('\n', ' ')

out = []
groups = collections.OrderedDict((k, []) for k in TITLES)
for p in P: groups[term(p['made'])].append(p)
for k, items in groups.items():
    out.append(f'### {TITLES[k]}\n')
    out.append('| # | Promise (when made) | Verdict | What happened / nuance | Sources |')
    out.append('|---|---|---|---|---|')
    for i, p in enumerate(items, 1):
        out.append(f"| {i} | {cell(p['promise'])} <br>*({cell(p['made'])}; {p['category']})* | {ICON[p['status']]} | {cell(p['detail'])} | "
                   + ' · '.join(link(u) for u in p['sources']) + ' |')
    out.append('')

# scorecard
def sc(items):
    c = collections.Counter(p['status'] for p in items)
    n = sum(c[s] for s in ('kept', 'partially-kept', 'broken', 'abandoned', 'in-progress'))
    r = sum(c[s] for s in ('kept', 'partially-kept', 'broken', 'abandoned'))
    return c, n, r
rows = []
for k, lab in [('A', '2008 (Key govt)'), ('B', '2011 (Key govt)'), ('C', '2014 (Key/English govt)'),
               ('A+B+C', '**Fifth National Govt total 2008–17**'), ('D', '2017 & 2020 (opposition, untested)'),
               ('E', '**2023 (Luxon govt) total**')]:
    items = [p for kk in k.split('+') for p in groups[kk]]
    c, n, r = sc(items)
    pct = lambda s: f"{100*c[s]/r:.0f}%" if r and s != 'in-progress' else '–'
    rows.append(f"| {lab} | {n} | {c['kept']} ({pct('kept')}) | {c['partially-kept']} ({pct('partially-kept')}) | {c['broken']} ({pct('broken')}) | {c['abandoned']} ({pct('abandoned')}) | {c['in-progress']} |")
score = ['| Term / campaign | Assessed | Kept | Partially kept | Broken | Abandoned | In progress |',
         '|---|---|---|---|---|---|---|'] + rows + ['',
         '*Percentages are of **resolved** promises (kept + partially kept + broken + abandoned); in-progress items are excluded from the denominator. 2026 promises (' + str(len(groups['2026'])) + ') are listed for reference only.*']

md_path = os.path.join(ROOT, 'parties/national/track-record.md')
md = open(md_path).read()
md = re.sub(r'<!-- GENERATED:scorecard START -->.*?<!-- GENERATED:scorecard END -->',
            '<!-- GENERATED:scorecard START -->\n' + '\n'.join(score) + '\n<!-- GENERATED:scorecard END -->', md, flags=re.S)
md = re.sub(r'<!-- GENERATED:promises START -->.*?<!-- GENERATED:promises END -->',
            '<!-- GENERATED:promises START -->\n' + '\n'.join(out) + '\n<!-- GENERATED:promises END -->', md, flags=re.S)
open(md_path, 'w').write(md)
print('\n'.join(score))

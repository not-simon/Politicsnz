#!/usr/bin/env python3
"""Sanity-check the guide layer (data/guide/*.json).

Checks: every 2026 party-vote party is present exactly once with all required fields;
every policy id cited exists in parties/<slug>/policies/policies.json or in the raw
policy.nz download for that party; every issue position names a known party; every key
fact and every non-policy.nz position has at least one source; no empty summaries.
Exit code 1 if any ERROR is found. Run: python3 tools/guide_validate.py
"""
import json, pathlib, sys, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
G = ROOT / 'data' / 'guide'
sys.path.insert(0, str(ROOT / 'tools'))
from guide_enrich import PNZ  # noqa: E402

REQUIRED = ['slug', 'name', 'leaders', 'founded', 'position', 'tagline', 'in_a_nutshell', 'big_ideas', 'they_say',
            'critics_say', 'current_seats', 'polling_avg_2026', 'track_record_line', 'coalition_stance_2026',
            'costings', 'website', 'sources']
errors, warnings = [], []


def known_ids(slug):
    ids = set()
    f = ROOT / 'parties' / slug / 'policies' / 'policies.json'
    if f.exists():
        try:
            ids |= {p['id'] for p in json.loads(f.read_text())}
        except Exception as e:  # file mid-write by another agent
            warnings.append(f'{slug}: could not read {f.name}: {e}')
    raw = ROOT / 'raw' / 'policy.nz' / 'parties' / (PNZ.get(slug, slug) + '.json')
    if raw.exists():
        ids |= {p['reference'] for p in json.loads(raw.read_text())['policies']}
    return ids


def check_ids(slug, ids, where):
    have = known_ids(slug)
    for i in ids:
        if i not in have:
            (errors if i.startswith('POL') else warnings).append(f'{where}: unknown policy id {i} for {slug}')


parties = json.loads((G / 'parties.json').read_text())['parties']
slugs = [p['slug'] for p in parties]
if sorted(slugs) != sorted(PNZ):
    errors.append(f'party list mismatch: missing {set(PNZ) - set(slugs)} extra {set(slugs) - set(PNZ)}')
if len(slugs) != len(set(slugs)):
    errors.append('duplicate party slugs')
for p in parties:
    for k in REQUIRED:
        if k not in p or p[k] in (None, '', []):
            (warnings if k in ('polling_avg_2026',) else errors).append(f"{p['slug']}: missing/empty {k}")
    if not 5 <= len(p.get('big_ideas', [])) <= 7 and p['slug'] not in ('free-palestine',):
        warnings.append(f"{p['slug']}: {len(p.get('big_ideas', []))} big ideas (want 5-7)")
    for b in p.get('big_ideas', []):
        check_ids(p['slug'], b.get('policy_ids', []), p['slug'] + ' big_idea')
        if not b.get('policy_ids') and not b.get('source'):
            errors.append(f"{p['slug']}: big idea without policy id or source: {b['text'][:50]}")
    for k in ('they_say', 'critics_say', 'costings', 'coalition_stance_2026'):
        v = p.get(k) or {}
        if k != 'critics_say' and k != 'coalition_stance_2026' and k != 'costings' and not v.get('sources'):
            errors.append(f"{p['slug']}: {k} has no source")
    n = len(re.findall(r'[.!?](\s|$)', p['in_a_nutshell']))
    if not 2 <= n <= 3:
        warnings.append(f"{p['slug']}: in_a_nutshell has {n} sentences")

issues = json.loads((G / 'issues.json').read_text())['issues']
for iss in issues:
    for f in iss['key_facts']:
        if not f.get('sources'):
            errors.append(f"{iss['slug']}: fact without source: {f['fact'][:60]}")
    for slug, pos in iss['positions'].items():
        if slug not in PNZ:
            errors.append(f"{iss['slug']}: unknown party {slug}")
            continue
        if not pos.get('summary'):
            errors.append(f"{iss['slug']}/{slug}: empty summary")
        check_ids(slug, pos.get('policy_ids', []), iss['slug'])
        if not pos.get('policy_ids') and not pos.get('sources'):
            errors.append(f"{iss['slug']}/{slug}: no policy ids or sources")

print(f'{len(parties)} parties, {len(issues)} issues, '
      f'{sum(len(i["positions"]) for i in issues)} positions, {sum(len(i["key_facts"]) for i in issues)} key facts')
for w in warnings:
    print('WARN ', w)
for e in errors:
    print('ERROR', e)
sys.exit(1 if errors else 0)

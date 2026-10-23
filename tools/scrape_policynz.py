#!/usr/bin/env python3
"""Download the structured 2026 election data embedded in policy.nz pages
(Next.js __NEXT_DATA__) into raw/policy.nz/. Parties, policies, list candidates,
electorate candidates. Re-runnable."""
import json, re, sys, time, urllib.request, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'raw' / 'policy.nz'
UA = {'User-Agent': 'Mozilla/5.0 (PoliticsNZ personal research archive)'}

def page(path):
    for attempt in range(4):
        try:
            req = urllib.request.Request('https://policy.nz' + path, headers=UA)
            h = urllib.request.urlopen(req, timeout=40).read().decode('utf-8')
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S)
            return json.loads(m.group(1))['props']['pageProps']
        except Exception as e:
            print('retry', path, e, file=sys.stderr); time.sleep(2 ** attempt)
    return None

def save(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1))

# 1. party vote election: all parties + all policies (embedded in any party page)
first = page('/2026/party-vote/parties/national-party')
el = first['election']
save(ROOT / 'party-vote-election.json', el)
for p in el['parties']:
    slug = p['party']['slug']
    pp = page(f'/2026/party-vote/parties/{slug}')
    save(ROOT / 'parties' / f'{slug}.json', {'party': p['party'], 'policies': p['policies'], 'partyList': pp.get('partyList') if pp else None})
    print('party', slug, len(p['policies']), len((pp or {}).get('partyList') or []))

# 2. electorates and their candidates
els = page('/2026/elections')
save(ROOT / 'elections-index.json', els['groupedElections'])
for e in els['groupedElections']['elections']:
    first_path = e['path']
    ep = page(first_path)
    if not ep: continue
    save(ROOT / 'electorates' / f"{e['slug']}.json", ep)
    print('electorate', e['slug'], list(ep.keys()))

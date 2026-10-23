#!/usr/bin/env python3
"""Write parties/national/people/README.md (index) from raw/people/national/index-build.json
(produced by tools/people_national_build.py)."""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PEOPLE = os.path.join(ROOT, 'parties', 'national', 'people')
ix = json.load(open(os.path.join(ROOT, 'raw', 'people', 'national', 'index-build.json')))
LBL = {'current-mp': 'Current MP', 'current-mp-standing-2026': 'MP, standing 2026', 'current-mp-retiring': 'MP, retiring 2026',
       'former-mp': 'Former MP', 'deceased': 'Deceased', 'candidate-2026': '2026 candidate'}
def esc(s): return str(s or '').replace('|', '\\|')
def photo(p):
    return f'<img src="{p["slug"]}/photo.jpg" width="48" alt="">' if os.path.exists(os.path.join(PEOPLE, p['slug'], 'photo.jpg')) else ''
def elec(p, current):
    if p.get('status') == 'candidate-2026' or current:
        e26 = p.get('electorate_2026')
        cur = [e['electorate'] for e in p.get('electorates', []) if not e.get('to')]
        if current:
            now = cur[0] if cur else 'List'
            return now + (f' (2026: {e26})' if e26 and e26 != now else '')
        return e26 or 'List only'
    es = []
    for e in sorted(p.get('electorates', []), key=lambda e: e.get('from') or ''):
        if e['electorate'] not in es: es.append(e['electorate'])
    return ', '.join(es) or 'List'
def roles(p, n=3):
    r = p.get('roles') or []
    if not r and (p.get('questionnaire_2026') or {}).get('Before politics'):
        return 'Before politics: ' + p['questionnaire_2026']['Before politics']
    return '; '.join(r[:n]) + (' …' if len(r) > n else '')
def row(p, current=False):
    st = LBL.get(p['status'], p['status'])
    if p['slug'] == 'agnes-loheni': st += ' (former MP 2019–20)'
    if p.get('party') not in (None, 'national'): st += f" — now {p['party'].replace('-', ' ').upper() if p['party'] in ('act',) else {'opportunity': 'TOP'}.get(p['party'], p['party'].replace('-', ' ').title().replace('Nz', 'NZ'))}"
    rk = p.get('list_rank_2026_official', '')
    return f"| {photo(p)} | [{esc(p['name'])}]({p['slug']}/) | {esc(st)} | {esc(elec(p, current))} | {rk} | {esc(roles(p))} |"
H = ['| Photo | Name | Status | Electorate | 2026 list # | Roles |', '|---|---|---|---|---|---|']
cur = [p for p in ix if p['status'].startswith('current-mp')]
cand = [p for p in ix if p['status'] == 'candidate-2026']
former = [p for p in ix if p['status'] in ('former-mp', 'deceased')]
cur.sort(key=lambda p: (p.get('list_rank_2026_official') or 999, p['name']))
cand.sort(key=lambda p: (p.get('list_rank_2026_official') or 999, p['name']))
former.sort(key=lambda p: p['name'].split()[-1] + p['name'])
L = ['# New Zealand National Party — people', '',
     'This index lists every National MP who sat at any time in the 50th–54th Parliaments (2011–2026), and every National candidate at the 7 November 2026 general election. Each person has a folder with `README.md` (profile), `person.json` (structured data) and, where available, `photo.jpg`. Status is as at **23 October 2026**.', '',
     f'**Counts:** {len(cur)} current MPs ({sum(p["status"]=="current-mp-standing-2026" for p in cur)} standing again, {sum(p["status"]=="current-mp-retiring" for p in cur)} retiring); '
     f'{len(cand)} 2026 candidates who are not sitting MPs (one, Agnes Loheni, is a former MP); {len(former)} former MPs from 2011–2026, {sum(p["status"]=="deceased" for p in former)} of them deceased. '
     f'{len(ix)} people in total.', '',
     '**List ranks:** the "2026 list #" column uses the Electoral Commission\'s official National Party list ([vote.nz](https://vote.nz/2026-general-election/voting-in-the-election/party-lists)). '
     'policy.nz (quoted in each profile\'s generated "2026 candidacy" section) numbers candidates from #14 down one place lower. Its list appears to still include Chris Penk at #14; he withdrew after the August 2026 leadership challenge. '
     'Example: Penny Simmonds is officially #14, but #15 on policy.nz. Jessica Rowe, who replaced Penk in Kaipara ki Mahurangi, is officially #68.', '',
     '**Moved to other parties:** some former National MPs now belong to other parties.',
     '- Parmjeet Parmar is an ACT MP: see [`../../act/people/parmjeet-parmar`](../../act/people/parmjeet-parmar/).',
     '- Alfred Ngaro and Harete Hipango are NZ First 2026 candidates: see [`../../nz-first/people/alfred-ngaro`](../../nz-first/people/alfred-ngaro/) and [`../../nz-first/people/harete-hipango-brownlie`](../../nz-first/people/harete-hipango-brownlie/).',
     '- Jami-Lee Ross was later an independent and Advance NZ co-leader; Matt King founded DemocracyNZ; Jackie Blue joined TOP in 2026.',
     '',
     'Their profiles stay in this folder because they served as National MPs.', '',
     '## Current MPs (54th Parliament)', '', 'Sorted by 2026 list rank, with unranked (retiring) MPs last.', ''] + H + [row(p, True) for p in cur] + \
    ['', '## 2026 candidates (not sitting MPs), by list rank', ''] + H + [row(p) for p in cand] + \
    ['', '## Former MPs who served 2011–2026', '', 'Includes MPs who left before or during the 50th–54th Parliaments. Sorted by surname.', ''] + H + [row(p) for p in former] + \
    ['', '---', '', 'Built by `tools/people_national_build.py` and `tools/people_national_index.py`, from Wikipedia (infobox and article text, with citations followed through), the Electoral Commission, policy.nz, national.org.nz candidate pages and the news sources cited in each profile. Photos are from Wikimedia Commons (licence recorded per person) or policy.nz candidate photos.', '']
open(os.path.join(PEOPLE, 'README.md'), 'w').write('\n'.join(L))
print(len(cur), len(cand), len(former))

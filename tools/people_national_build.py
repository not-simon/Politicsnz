#!/usr/bin/env python3
"""Build parties/national/people/<slug>/{person.json,README.md,photo.jpg} for National MPs (50th-54th
Parliaments) and 2026 candidates.
Inputs: raw/people/national/derived.json (tools/people_national_extract.py), raw/people/national/wiki/*.json,
        tools/people_national_content/<slug>.md  (hand-written: a JSON header, a line '---', then markdown sections
        '## Current status', '## Biography', '## Political career', '## Record & notable actions', '## Controversies').
Keeps existing policy.nz fields in person.json and the <!-- GENERATED:2026-candidacy --> block in README.md verbatim.
Never overwrites an existing photo.jpg."""
import json, os, re, sys, io, glob, datetime
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people_national_wiki import fetch_bytes
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
RAW = os.path.join(ROOT, 'raw', 'people', 'national')
PEOPLE = os.path.join(ROOT, 'parties', 'national', 'people')
CONTENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'people_national_content')
START, END = '<!-- GENERATED:2026-candidacy START -->', '<!-- GENERATED:2026-candidacy END -->'
PARL = {43: '1990-10-27', 44: '1993-11-06', 45: '1996-10-12', 46: '1999-11-27', 47: '2002-07-27', 48: '2005-09-17',
        49: '2008-11-08', 50: '2011-11-26', 51: '2014-09-20', 52: '2017-09-23', 53: '2020-10-17', 54: '2023-10-14', 55: '2026-11-07'}
MONTHS = {m: i for i, m in enumerate(['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
                                      'october', 'november', 'december'], 1)}
VOTE_LABEL = {'marriage_equality_2013_third_reading': ('Marriage (Definition of Marriage) Amendment Bill — third reading, 17 Apr 2013', 'https://en.wikipedia.org/wiki/Marriage_(Definition_of_Marriage)_Amendment_Act_2013'),
              'end_of_life_choice_2019_third_reading': ('End of Life Choice Bill — third reading, 13 Nov 2019', 'https://en.wikipedia.org/wiki/End_of_Life_Choice_Act_2019'),
              'abortion_legislation_2020_third_reading': ('Abortion Legislation Bill — third reading, 18 Mar 2020', 'https://en.wikipedia.org/wiki/Abortion_Legislation_Act_2020'),
              'conversion_practices_2022_third_reading': ('Conversion Practices Prohibition Legislation Bill — third reading, 15 Feb 2022', 'https://www.rnz.co.nz/news/national/461599/politicians-react-as-bill-to-ban-conversion-therapy-passes')}
STATUS_LABEL = {'current-mp': 'Current MP', 'current-mp-standing-2026': 'Current MP — standing in 2026', 'current-mp-retiring': 'Current MP — retiring at the 2026 election',
                'former-mp': 'Former MP', 'deceased': 'Deceased (former MP)', 'candidate-2026': '2026 candidate (not an MP)', 'party-official': 'Party official'}

def pdate(s):
    if not s: return None
    s = s.strip()
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', s)
    if m: return s[:10]
    m = re.search(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', s)
    if m and m.group(2).lower() in MONTHS: return f'{int(m.group(3)):04d}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}'
    m = re.search(r'([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})', s)
    if m and m.group(1).lower() in MONTHS: return f'{int(m.group(3)):04d}-{MONTHS[m.group(1).lower()]:02d}-{int(m.group(2)):02d}'
    m = re.search(r'([A-Za-z]+)\s+(\d{4})', s)
    if m and m.group(1).lower() in MONTHS: return f'{int(m.group(2)):04d}-{MONTHS[m.group(1).lower()]:02d}-01'
    m = re.search(r'(\d{4})', s)
    return f'{m.group(1)}-01-01' if m else None
def year(s): return (pdate(s) or '')[:4]
def parliaments_for(terms):
    out = set(); ks = sorted(PARL)
    for s, e in terms:
        if not s: continue
        for i, n in enumerate(ks[:-1]):
            if s < PARL[ks[i + 1]] and (e is None or e > PARL[n]): out.add(n)
    return sorted(out)
def clean_office(o):
    o = re.sub(r'^.*\|', '', o) if '|' in o else o
    return re.sub(r'^\d+(st|nd|rd|th)\s+', '', o).strip()
def read_content(slug):
    fn = os.path.join(CONTENT, slug + '.md')
    if not os.path.exists(fn): return {}, ''
    t = open(fn).read()
    head, _, body = t.partition('\n---\n')
    return json.loads(head), body.strip()
def section(body, name):
    m = re.search(r'^## ' + re.escape(name) + r'\s*\n(.*?)(?=^## |\Z)', body, flags=re.S | re.M)
    return m.group(1).strip() if m else ''
def save_photo(url, dest):
    data = fetch_bytes(url)
    im = Image.open(io.BytesIO(data))
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[-1]); im = bg
    im = im.convert('RGB'); im.thumbnail((400, 400)); im.save(dest, 'JPEG', quality=82)
def strip_html(s): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s or '')).strip()

derived = json.load(open(os.path.join(RAW, 'derived.json')))
wiki = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(os.path.join(RAW, 'wiki', '*.json'))}
photos = json.load(open(os.path.join(RAW, 'photos.json'))) if os.path.exists(os.path.join(RAW, 'photos.json')) else {}
official = json.load(open(os.path.join(RAW, 'ec', 'national-list-2026.json')))  # slug -> rank (Electoral Commission, 9 Oct 2026)
slugs = set(derived) | {s for s in os.listdir(PEOPLE) if os.path.isdir(os.path.join(PEOPLE, s))} | \
        {os.path.basename(f)[:-3] for f in glob.glob(os.path.join(CONTENT, '*.md'))}
only = set(sys.argv[1:])
index = []
for slug in sorted(slugs):
    d = os.path.join(PEOPLE, slug)
    hand, body = read_content(slug)
    dv = derived.get(hand.get('wiki_slug', slug), {})
    if only and slug not in only:
        pass
    os.makedirs(d, exist_ok=True)
    pj = os.path.join(d, 'person.json')
    p = json.load(open(pj)) if os.path.exists(pj) else {}
    w = wiki.get(hand.get('wiki_slug', slug), {})
    name = hand.get('name') or p.get('name') or (w.get('title') and re.sub(r'\s*\(.*\)', '', w['title'])) or slug
    # electorates & terms from infobox
    terms, electorates = [], []
    for o in dv.get('offices', []):
        c = o.get('constituency')
        if not c: continue
        s0, e0 = pdate(o['term_start']), pdate(o['term_end']) if o['term_end'] else None
        parts = [x.strip(' ,') for x in c.split(';') if x.strip(' ,')]
        multi = len(parts) > 1
        for part in parts:
            m = re.match(r'(.+?)\s*\((\d{4})\s*[–-]\s*(\d{2,4}|present)?\s*\)', part)
            if m:
                EY = {v[:4]: v for v in PARL.values()}
                nm, a, b = m.group(1).strip(' ,'), EY.get(m.group(2), m.group(2) + '-06-30'), m.group(3)
                b = None if (not b or b == 'present') else ((a[:2] + b) if len(b) == 2 else b)
                b = EY.get(b, b + '-06-30') if b else None
                a = s0 if (s0 and s0[:4] == a[:4]) else a
            else:
                nm, a, b = re.sub(r'\s*\(.*?\)', '', part).strip(), s0, e0
            terms.append((a, b))
            if not re.search(r'\blist\b', nm, re.I) and nm.lower() not in ('national', 'national party'):
                electorates.append({'electorate': nm, 'from': a, 'to': b, 'majority': o.get('majority') if not multi else None})
    roles = []
    for o in dv.get('offices', []):
        if o.get('office'):
            a, b = year(o['term_start']), year(o['term_end']) if o['term_end'] else ''
            roles.append(f"{clean_office(o['office'])} ({a}–{b})" if a else clean_office(o['office']))
    parls = hand.get('parliaments') or sorted(set(parliaments_for(terms)) | set(dv.get('parliaments_50_54', [])))
    in54 = 54 in dv.get('parliaments_50_54', [])
    sitting = in54 and any(e is None for s, e in terms)
    rank = official.get(slug)
    status = hand.get('status') or ('deceased' if dv.get('died') else ('current-mp-standing-2026' if sitting and rank else
              'current-mp-retiring' if sitting else 'former-mp' if dv else p.get('status', 'candidate-2026')))
    p.update({'name': name, 'slug': slug})
    p.setdefault('party', 'national')
    for k in ('party', 'party_history', 'status_detail', 'electorate_2026'):
        if k in hand: p[k] = hand[k]
    p['status'] = status
    p.setdefault('party_history', [{'party': 'national', 'from': year(min([t[0] for t in terms if t[0]], default='')) or None, 'to': None}] if dv else [])
    p['roles'] = hand.get('roles', roles)
    if parls: p['parliaments'] = parls
    if terms: p['first_elected'] = int(min(t[0] for t in terms if t[0])[:4])
    if hand.get('first_elected'): p['first_elected'] = hand['first_elected']
    if electorates: p['electorates'] = electorates
    if dv.get('born') or hand.get('born'): p['born'] = hand.get('born') or pdate(dv['born']) or dv['born']
    if dv.get('died'): p['died'] = pdate(dv['died']) or dv['died']
    if dv.get('wikipedia') or hand.get('wikipedia'): p['wikipedia'] = hand.get('wikipedia') or dv['wikipedia']
    if rank: p['list_rank_2026_official'] = rank
    if dv.get('votes'): p['conscience_votes'] = dv['votes']
    # photo
    photo = os.path.join(d, 'photo.jpg')
    if slug in photos and os.path.exists(photo) and not str(p.get('photo_source', '')).startswith('https://cdn.sanity.io'):
        p.update(photos[slug])
    if p.get('photo_source', '').startswith('https://cdn.sanity.io') and not p.get('photo_license'):
        p['photo_license'] = 'Not stated (candidate photo supplied to policy.nz; used for identification)'
    srcs = list(dict.fromkeys(hand.get('sources', []) + ([p['wikipedia']] if p.get('wikipedia') else []) + p.get('sources', [])))
    p['sources'] = srcs
    # README
    rd = os.path.join(d, 'README.md')
    old = open(rd).read() if os.path.exists(rd) else ''
    gen = re.search(re.escape(START) + '.*?' + re.escape(END), old, flags=re.S)
    L = [f'# {name}', '']
    if os.path.exists(photo): L += [f'<img src="photo.jpg" width="200" align="right" alt="{name}">', '']
    facts = [('Party', hand.get('party_label') or 'New Zealand National Party'), ('Status', STATUS_LABEL.get(status, status))]
    if p.get('status_detail'): facts.append(('Now (Oct 2026)', p['status_detail']))
    if hand.get('electorates_label'): facts.append(('Electorate(s)', hand['electorates_label']))
    elif electorates: facts.append(('Electorate(s)', '; '.join(f"{e['electorate']} ({(e['from'] or '')[:4]}–{(e['to'] or '')[:4]})" for e in sorted(electorates, key=lambda e: e['from'] or ''))))
    if p.get('parliaments'): facts.append(('Parliaments', ', '.join(f'{n}th' if n not in (51, 52, 53) else {51: '51st', 52: '52nd', 53: '53rd'}[n] for n in p['parliaments'])))
    if p.get('first_elected'): facts.append(('First elected', str(p['first_elected'])))
    if p.get('born'): facts.append(('Born', p['born'] + (f" — {dv['birth_place']}" if dv.get('birth_place') else '')))
    if p.get('died'): facts.append(('Died', p['died']))
    if rank or p.get('electorate_2026'): facts.append(('2026 election', ', '.join(x for x in [f'list #{rank}' if rank else '', f"standing in {p['electorate_2026']}" if p.get('electorate_2026') else ''] if x)))
    if p.get('wikipedia'): facts.append(('Wikipedia', f"[{p['wikipedia'].rsplit('/', 1)[-1].replace('_', ' ')}]({p['wikipedia']})"))
    L += ['| | |', '|---|---|'] + [f'| **{k}** | {v} |' for k, v in facts] + ['']
    if rank and p.get('list_rank_2026') and p['list_rank_2026'] != rank:
        L += [f"> **List rank note:** policy.nz (in the 2026 candidacy section below) gives #{p['list_rank_2026']}. The Electoral Commission's official National list gives **#{rank}**. From #14 down, policy.nz's numbering appears to still include Chris Penk, who withdrew. ([Electoral Commission](https://vote.nz/2026-general-election/voting-in-the-election/party-lists))", '']
    for sec in ('Current status', 'Biography', 'Political career', 'Record & notable actions', 'Controversies'):
        txt = section(body, sec)
        if sec == 'Political career' and p['roles'] and not hand.get('roles_in_text'):
            txt += ('\n\n' if txt else '') + ('**Roles held:**\n\n' if hand.get('roles') else '**Offices held** (from the Wikipedia infobox; dates are years):\n\n') + '\n'.join(f'- {r}' for r in p['roles'])
        if sec == 'Political career' and electorates and any(e.get('majority') for e in electorates):
            pass
        if sec == 'Record & notable actions' and dv.get('votes'):
            vt = '\n'.join(f'| [{VOTE_LABEL[k][0]}]({VOTE_LABEL[k][1]}) | {v} |' for k, v in dv['votes'].items())
            txt += ('\n\n' if txt else '') + '**Conscience votes** (recorded third-reading votes):\n\n| Bill | Vote |\n|---|---|\n' + vt
            if 'conversion_practices_2022_third_reading' not in dv['votes'] and 53 in (p.get('parliaments') or []) and any((e is None or e > '2022-02-15') and s and s < '2022-02-15' for s, e in terms):
                txt += '\n| Conversion Practices Prohibition Legislation Bill — third reading, 15 Feb 2022 | not among the 8 National MPs recorded as opposed (25 National MPs voted in favour) |'
        if txt: L += [f'## {sec}', '', txt, '']
    if gen: L += [gen.group(0), '']
    S = ['## Sources', ''] + [f'- <{s}>' for s in srcs]
    if p.get('photo_source'):
        S.append(f"- Photo: <{p['photo_source']}> — {p.get('photo_credit', '')}" + (f" ({p['photo_license']})" if p.get('photo_license') else ''))
    L += S + ['']
    open(rd, 'w').write('\n'.join(L))
    json.dump(p, open(pj, 'w'), ensure_ascii=False, indent=1)
    index.append(p)
json.dump(index, open(os.path.join(RAW, 'index-build.json'), 'w'), ensure_ascii=False, indent=1)
print(len(index), 'people built;', sum(1 for s in slugs if os.path.exists(os.path.join(CONTENT, s + '.md'))), 'with hand-written content')

#!/usr/bin/env python3
"""Create parties/<party>/people/<slug>/ for every 2026 candidate on policy.nz:
person.json, README.md (generated questionnaire section), photo.jpg (400px).
Never overwrites hand-written README content outside the GENERATED markers."""
import re as _re
PERSONAL_MAIL = _re.compile(r'@(gmail|googlemail|hotmail|outlook|live|yahoo|xtra|icloud|me|protonmail|proton|aol|msn|slingshot|orcon|inspire|vodafone|spark|clear|paradise|ihug|windowslive)\.', _re.I)
import json, glob, pathlib, re, sys, io, urllib.request
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from partymap import PNZ_TO_REPO
ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / 'raw' / 'policy.nz'
people = {}

def add(c, party_slug, electorate=None, desc=None, rank=None, leader=None, cand_policies=None):
    slug = c['slug']; p = people.setdefault((party_slug, slug), {'slug': slug, 'party': PNZ_TO_REPO.get(party_slug, party_slug)})
    p['name'] = f"{c['firstName']} {c['lastName']}".strip()
    p['first_name'], p['last_name'] = c['firstName'], c['lastName']
    if c.get('image'): p['image_src'] = c['image']
    if electorate: p['electorate_2026'] = electorate
    if rank and rank.strip(): p['list_rank_2026'] = int(rank)
    if desc: p['candidacy_2026'] = desc
    if leader: p['leadership_label'] = leader
    attrs = p.setdefault('questionnaire_2026', {})
    for a in c.get('attributes') or []:
        if not a.get('value') or a['name'] == 'Residence': continue   # home suburb is never stored or published
        if a['name'] == 'Public email' and PERSONAL_MAIL.search(a['value']): continue   # personal webmail dropped
        attrs[a['name']] = a['value']
    if cand_policies: p['candidate_policies_2026'] = cand_policies

titles = {}
for f in glob.glob(str(RAW / 'electorates' / '*.json')):
    el = json.load(open(f))['election']; titles[el['slug']] = el['title'].replace(' electorate', '')
for f in glob.glob(str(RAW / 'parties' / '*.json')):
    d = json.load(open(f)); ps = d['party']['slug']
    for c in d['partyList'] or []:
        pa = c.get('partyAffiliation') or {}
        add(c, ps, titles.get(c.get('electorateElectionSlug')), pa.get('candidacyDescription'), pa.get('listRank'), pa.get('leadershipLabel'))
for f in glob.glob(str(RAW / 'electorates' / '*.json')):
    el = json.load(open(f))['election']
    for c in el.get('candidates') or []:
        per = c['person']; ps = (per.get('party') or {}).get('slug') or 'independent'
        pa = per.get('partyAffiliation') or {}
        pol = [{'statement': x.get('statement'), 'details': {a['name']: a['value'] for a in x.get('attributes') or []}} for x in c.get('policies') or []]
        add(per, ps, titles[el['slug']], pa.get('candidacyDescription'), pa.get('listRank'), pa.get('leadershipLabel'), pol or None)

def photo(url, dest):
    if dest.exists(): return True
    try:
        data = urllib.request.urlopen(urllib.request.Request(url + '?w=400&h=400&fit=crop', headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read()
        im = Image.open(io.BytesIO(data)).convert('RGB'); im.thumbnail((400, 400)); im.save(dest, 'JPEG', quality=82); return True
    except Exception as e:
        print('photo fail', url, e, file=sys.stderr); return False

START, END = '<!-- GENERATED:2026-candidacy START -->', '<!-- GENERATED:2026-candidacy END -->'
for (ps, slug), p in sorted(people.items()):
    d = ROOT / 'parties' / p['party'] / 'people' / slug; d.mkdir(parents=True, exist_ok=True)
    pj = d / 'person.json'
    existing = json.loads(pj.read_text()) if pj.exists() else {}
    if p.get('image_src') and photo(p['image_src'], d / 'photo.jpg') and not existing.get('photo'):
        existing.update({'photo': 'photo.jpg', 'photo_source': p['image_src'], 'photo_credit': 'Supplied to policy.nz by the candidate/party'})
    base = {'name': p['name'], 'slug': slug, 'party': p['party'], 'status': existing.get('status', 'candidate-2026')}
    # hand-corrected names in person.json win over policy.nz's spelling (e.g. macrons); everything else refreshes
    merged = {**base, **existing, **{k: v for k, v in p.items() if k not in ('image_src',) and not (k == 'name' and existing.get('name'))}}
    merged.setdefault('sources', [])
    src = f'https://policy.nz/2026/party-vote/parties/{ps}'
    if src not in merged['sources']: merged['sources'].append(src)
    pj.write_text(json.dumps(merged, ensure_ascii=False, indent=1))
    q = p.get('questionnaire_2026', {})
    lines = [START, '## 2026 candidacy', '']
    if p.get('electorate_2026'): lines.append(f"- **Electorate:** {p['electorate_2026']}")
    if p.get('list_rank_2026'): lines.append(f"- **List ranking:** {p['list_rank_2026']}")
    if p.get('leadership_label'): lines.append(f"- **Role:** {p['leadership_label']}")
    # Privacy: the candidate's home suburb ('Residence') is never published, and personal webmail addresses are dropped
    # (Privacy Act 2020 IPP 11(1)(d); see docs/LEGAL_REVIEW.md M8/S9). Only party/parliament/campaign-domain emails are shown.
    q.pop('Residence', None)
    if q.get('Public email') and PERSONAL_MAIL.search(q['Public email']): q.pop('Public email')
    for k in ('Before politics', 'Age', 'Public email', 'Website', 'Facebook', 'Instagram', 'X', 'Twitter', 'LinkedIn', 'TikTok', 'YouTube'):
        if k in q: lines.append(f'- **{k}:** {q[k]}')
    for k, v in q.items():
        if k in ('Before politics', 'Residence', 'Age', 'Public email', 'Website', 'Facebook', 'Instagram', 'X', 'Twitter', 'LinkedIn', 'TikTok', 'YouTube'): continue
        lines += ['', f'### {k}', '', v.strip()]
    for pol in p.get('candidate_policies_2026') or []:
        lines += ['', f"### Local commitment: {pol['statement']}", ''] + [f'**{k}:** {v}' for k, v in pol['details'].items()]
    lines += ['', '_Source: candidate questionnaire answers published on [policy.nz](%s), retrieved Oct 2026._' % src, END]
    block = '\n'.join(lines)
    rd = d / 'README.md'
    if rd.exists():
        t = rd.read_text()
        t = re.sub(re.escape(START) + '.*?' + re.escape(END), block, t, flags=re.S) if START in t else t.rstrip() + '\n\n' + block + '\n'
    else:
        img = '<img src="photo.jpg" width="200" align="right" alt="%s">\n\n' % p['name'] if (d / 'photo.jpg').exists() else ''
        t = f"# {p['name']}\n\n{img}**Party:** {p['party']} · **Status:** 2026 candidate\n\n{block}\n"
    rd.write_text(t)
print(len(people), 'candidates written')

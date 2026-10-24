#!/usr/bin/env python3
"""Bundle the archive into site/data/ for the interactive explorer (site/index.html).
Run after any data change:  python3 tools/build_site.py"""
import json, glob, pathlib, re, io, base64, os
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'site' / 'data'; OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'fulltext').mkdir(exist_ok=True)

import math
def clean(o):
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)): return None
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list): return [clean(v) for v in o]
    return o
def dumps(o): return json.dumps(clean(o), ensure_ascii=False, allow_nan=False)
def load(p, default=None):
    try: return json.loads(pathlib.Path(p).read_text())
    except Exception: return default

def frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---\n?', text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1); meta[k.strip()] = v.strip().strip('"\'')
        text = text[m.end():]
    return meta, text

meta = load(ROOT / 'data' / 'parties-meta.json', {'parties': {}})['parties']
TOPIC_LIST = ['economy', 'health', 'education', 'housing', 'environment', 'law-justice-and-government', 'community-and-inclusion', 'te-ao-maori', 'migration',
              'transport-and-infrastructure', 'incomes-and-employment', 'defence-and-foreign-affairs', 'media-culture-and-recreation']
elections = sorted([load(f) for f in glob.glob(str(ROOT / 'data' / 'elections' / '*.json'))], key=lambda e: e.get('year', 0) if e else 0)
elections = [e for e in elections if e]
upcoming = [e for e in elections if not any(isinstance(r, dict) and r.get('party_vote_pct') is not None for r in e.get('parties') or [])]
elections = [e for e in elections if e not in upcoming]
parliaments = sorted([load(f) for f in glob.glob(str(ROOT / 'data' / 'parliaments' / '*.json'))], key=lambda p: p.get('parliament', 0) if p else 0)
parliaments = [p for p in parliaments if p]
polls_raw = load(ROOT / 'data' / 'polls-2026.json', [])
if isinstance(polls_raw, dict): polls_raw = polls_raw.get('polls', [])
polls = []
for x in polls_raw or []:
    d = x.get('end_date') or x.get('date'); res = x.get('results') or x.get('parties') or {}
    if d and re.match(r'\d{4}-\d{2}-\d{2}', str(d)) and res:
        polls.append({'date': d, 'pollster': x.get('pollster'), 'parties': {k: v for k, v in res.items() if isinstance(v, (int, float))}, 'source_url': x.get('source_url'),
                      'sample_size': x.get('sample_size'), 'fieldwork': x.get('date')})
promises = {pathlib.Path(f).stem: load(f, []) for f in glob.glob(str(ROOT / 'data' / 'promises' / '*.json'))}

# --- parties
parties = {}
for d in sorted((ROOT / 'parties').iterdir()):
    if not d.is_dir(): continue
    s = d.name; m = meta.get(s, {})
    readme = (d / 'README.md').read_text() if (d / 'README.md').exists() else ''
    intro = ''
    for para in re.split(r'\n\s*\n', re.sub(r'^#.*$', '', readme, flags=re.M)):
        p = para.strip()
        if p and not p.startswith(('|', '<', '!', '-', '*', '>')) and len(p) > 80: intro = p; break
    pols = load(d / 'policies' / 'policies.json', []) or []
    people_n = len(list((d / 'people').glob('*/person.json'))) if (d / 'people').exists() else 0
    title = re.search(r'^#\s+(.+)$', readme, re.M)
    parties[s] = {'slug': s, 'name': m.get('name') or (title.group(1).strip() if title else s.replace('-', ' ').title()),
                  'short': m.get('short') or s.replace('-', ' ').title(), 'color': m.get('color', '#A7ADB5'),
                  'order': m.get('order', 90), 'intro': intro[:900], 'policy_count': len(pols), 'people_count': people_n,
                  'has_readme': bool(readme), 'has_track_record': (d / 'track-record.md').exists()}

for s, m in meta.items():
    if s not in parties: parties[s] = {'slug': s, 'name': m['name'], 'short': m['short'], 'color': m['color'], 'order': m.get('order', 90), 'intro': '', 'policy_count': 0, 'people_count': 0, 'has_readme': False, 'has_track_record': False}

# --- policies + full texts
policies = {}
for s in parties:
    d = ROOT / 'parties' / s / 'policies'
    pols = load(d / 'policies.json', []) or []
    if pols: policies[s] = pols
    docs = {}
    for f in sorted((d / 'documents').glob('*.md')) if (d / 'documents').exists() else []:
        raw = f.read_text(errors='replace')
        if '\ufffd' in raw: raise SystemExit(f'{f}: contains U+FFFD (undecoded PDF glyph) at {raw.find(chr(0xfffd))} - fix the source text')
        fm, body = frontmatter(raw)
        docs['documents/' + f.name] = {'title': fm.get('title', f.stem), 'source_url': fm.get('source_url', ''),
                                       'retrieved': fm.get('retrieved', ''), 'text': body}
    if docs: (OUT / 'fulltext' / f'{s}.json').write_text(json.dumps(docs, ensure_ascii=False))
    parties[s]['document_count'] = len(docs)

# --- policy swipe deck: party-blind cards (statement + summary), leak-filtered
LEAK_NAMES = re.compile(r"\b(National|Labour|Greens?|ACT|NZ First|New Zealand First|Te P[āa]ti M[āa]ori|M[āa]ori Party|TOP|Opportunities Party|Alliance|Conservatives?|Vision NZ|NZ Loyal|Animal Justice|Women's Rights Party|"
    r"Luxon|Hipkins|Seymour|Peters|Swarbrick|Davidson|Waititi|Ngarewa-Packer|Willis|van Velden|Bishop|Brown|Jones|Costello|Doocey|Reti|Stanford|Upston|Robertson|Ardern|Edmonds|Sepuloni|Jackson|Kapa-Kingi|Ferris|Maipi-Clarke|Manji|Minto)\b")
LEAK_ACRONYMS = re.compile(r"\b(NAP|TOP|ALCP|AJP|WRP|NZF|NZOFP|NZOF|TTP|TTTP|PANZ|SEG|TPM|NZL|Nats|Nat|Lab|Grn|Not A Party|Opportunities|Women’s Rights|Women's Rights|Outdoors & Freedom|Outdoors and Freedom|Legalise Cannabis|Progressive Aotearoa|Socialist Equality|Vision|Loyal|Alliance)\b")
LEAK_TERMS = re.compile(r"coalition|current Government|this Government|the Government's|Luxon Government|National-led|Labour-led|our party|our government|we will|we would|we are|Green Budget|KiwiMart|Kiwipower|Future Fund|Medicard|LabourSaver|FamilyBoost|Treaty Principles Bill|Regulatory Standards|Fast-track Approvals Act|Three Strikes|Fair Pay Agreements?|Roads of National Significance|Te Aka Whai Ora|Whānau Ora|Mana Motuhake|kaupapa M[āa]ori", re.I)
def leaks(t): return bool(LEAK_NAMES.search(t) or LEAK_ACRONYMS.search(t) or LEAK_TERMS.search(t))
MAIN = {'national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'opportunity'}
swipe, seen_stmt = [], set()
for s, pols in policies.items():
    for pol in pols:
        sm = pol.get('summary') or {}
        why, how, text = (sm.get('why') or '').strip(), (sm.get('how') or '').strip(), (sm.get('text') or '').strip()
        st = (pol.get('statement') or '').strip()
        if not st or not (why or how or text): continue
        blob = ' '.join([st, why, how, text])
        if leaks(blob): continue
        key = re.sub(r'\W+', ' ', st.lower()).strip()
        if key in seen_stmt: continue
        seen_stmt.add(key)
        doc = next((x.get('document') for x in pol.get('sources') or [] if x.get('document')), None)
        topic = next((t for t in pol.get('topics') or [] if t in TOPIC_LIST), 'other')
        swipe.append({'id': pol.get('id'), 'party': s, 'statement': st, 'why': why[:600], 'how': (how or text)[:600], 'topic': topic, 'doc': doc,
                      'weight': 3 if s in MAIN else 1})
(OUT / 'swipe.json').write_text(dumps(swipe))
print('swipe cards', len(swipe), {s: sum(1 for c in swipe if c['party'] == s) for s in sorted({c['party'] for c in swipe})})

# --- people
def bio_excerpt(readme):
    for head in ('Current status', 'Biography', 'Political career'):
        m = re.search(r'^##+\s*' + head + r'.*?\n(.*?)(?=\n##|\Z)', readme, re.S | re.M)
        if m:
            t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>|\[([^\]]+)\]\([^)]+\)', r'\1', m.group(1))).strip()
            if len(t) > 40: return t[:700]
    return ''
people, thumbs = [], {}
for pj in sorted((ROOT / 'parties').glob('*/people/*/person.json')):
    p = load(pj, {}) or {}
    d = pj.parent; readme = (d / 'README.md').read_text() if (d / 'README.md').exists() else ''
    q = p.get('questionnaire_2026') or {}
    rec = {k: p.get(k) for k in ('name', 'slug', 'party', 'status', 'status_detail', 'roles', 'parliaments', 'first_elected',
                                 'electorate_2026', 'list_rank_2026', 'leadership_label', 'wikipedia', 'party_history', 'born') if p.get(k)}
    rec['folder'] = str(d.relative_to(ROOT))
    if p.get('list_rank_2026_official'): rec['list_rank_2026'] = p['list_rank_2026_official']
    rec['party'] = rec.get('party') or d.parent.parent.name
    rec['bio'] = bio_excerpt(readme)
    rec['has_profile'] = len(re.sub(r'<!-- GENERATED.*?END -->', '', readme, flags=re.S)) > 600
    if q.get("Why I'm standing"): rec['why'] = q["Why I'm standing"][:600]
    if q.get('Before politics'): rec['before'] = q['Before politics']
    ph = d / (p.get('photo') or 'photo.jpg')
    if ph.exists():
        try:
            im = Image.open(ph).convert('RGB'); w, h = im.size; s = min(w, h)
            im = im.crop(((w - s) // 2, max(0, (h - s) // 4), (w - s) // 2 + s, max(0, (h - s) // 4) + s)).resize((128, 128))
            # one small JPEG per person, loaded lazily by the browser (replaces the 2.7 MB base64 thumbs.json)
            (OUT / 'faces').mkdir(exist_ok=True); fn = f"{rec['party']}--{d.name}.jpg"; im.save(OUT / 'faces' / fn, 'JPEG', quality=72, optimize=True)
            rec['photo'] = 'data/faces/' + fn; thumbs[rec['folder']] = rec['photo']
            rec['photo_credit'] = p.get('photo_credit') or ''
            if p.get('photo_license'): rec['photo_license'] = p['photo_license']
            if p.get('photo_license_url'): rec['photo_license_url'] = p['photo_license_url']
        except Exception: pass
    people.append(rec)

# --- readable pages (markdown) for the in-app reader
pages = {}
for f in [ROOT / 'REPORT.md', ROOT / 'README.md'] + sorted((ROOT / 'elections').glob('*.md')) + sorted((ROOT / 'parties').glob('*/README.md')) \
         + sorted((ROOT / 'parties').glob('*/track-record.md')) + [ROOT / 'parties' / 'MINOR_PARTIES.md'] \
         + sorted((ROOT / 'parties').glob('*/policies/README.md')) + sorted((ROOT / 'guide').glob('*.md')) + sorted((ROOT / 'electorates').glob('*.md')) \
         + sorted((ROOT / 'parties').glob('*/people/*/README.md')) + sorted((ROOT / 'docs').glob('*.md')) + [ROOT / 'NOTICE.md', ROOT / 'CONTRIBUTING.md']:
    if f.exists(): pages[str(f.relative_to(ROOT))] = f.read_text()

guide = {'parties': load(ROOT / 'data' / 'guide' / 'parties.json', []), 'issues': load(ROOT / 'data' / 'guide' / 'issues.json', []),
         'howtovote': load(ROOT / 'data' / 'guide' / 'howtovote.json', {}),
         'quiz2': (lambda q, ex: ({**{k: v for k, v in q.items() if k != 'reconciliation_log'},
                                   'statements': [{**st, **({'explainer': ex[st['id']]} if st.get('id') in ex else {})} for st in q.get('statements', [])]}))(
             load(ROOT / 'data' / 'guide' / 'quiz2.json', {}), (load(ROOT / 'data' / 'guide' / 'quiz2-explainers.json', {}) or {}).get('explainers', {})),
         'compass': load(ROOT / 'data' / 'guide' / 'compass.json', {}), 'compass_parties': load(ROOT / 'data' / 'guide' / 'compass-parties.json', {})}
if isinstance(guide['parties'], dict): guide['parties'] = guide['parties'].get('parties', [])
if isinstance(guide['issues'], dict): guide['issues'] = guide['issues'].get('issues', [])
electorates = load(ROOT / 'data' / 'electorates' / '2026.json', [])
if isinstance(electorates, dict): electorates = electorates.get('electorates', [])
forecast = load(ROOT / 'data' / 'forecast.json', None)
# Election-night results (tools/results_feed.py). Attached only once real votes exist, so no zero-count 'live' page can appear.
results = load(ROOT / 'data' / 'results-2026.json', None)
if results and results.get('votes_cast') and upcoming:
    upcoming[0] = {**upcoming[0], 'results': results}
(OUT / 'results.json').write_text(dumps(results if results and results.get('votes_cast') else {'votes_cast': 0}))
bundle = {'forecast': forecast, 'upcoming': upcoming[0] if upcoming else None, 'guide': guide, 'electorates': electorates, 'generated': __import__('datetime').date.today().isoformat(), 'parties': parties, 'elections': elections,
          'parliaments': parliaments, 'polls': polls, 'promises': promises}
(OUT / 'bundle.json').write_text(dumps(bundle))
# --- party newsroom: headline + date + link only (no teaser text; see docs/LEGAL_REVIEW.md S8), plus the follow directory
rel = load(ROOT / 'data' / 'releases.json', {}) or {}
fol = load(ROOT / 'data' / 'guide' / 'follow.json', {}) or {}
PERSONAL_MAIL = re.compile(r'@(gmail|googlemail|hotmail|outlook|live|yahoo|xtra|icloud|me|protonmail|proton|aol|msn|slingshot|orcon|inspire|vodafone|spark|clear|paradise|ihug|windowslive)\.', re.I)
newsroom = {'updated': rel.get('updated'), 'window_days': rel.get('window_days'),
            'items': [{k: it.get(k) for k in ('party', 'title', 'date', 'url', 'source', 'ministerial', 'byline') if it.get(k) is not None} for it in rel.get('items', [])],
            'parties': {k: {kk: v.get(kk) for kk in ('name', 'newsroom_url', 'newsroom_verified')} for k, v in (rel.get('parties') or {}).items()},
            }
(OUT / 'newsroom.json').write_text(dumps(newsroom))
# the follow directory is only needed on the newsroom's single-party view, so it ships separately
(OUT / 'follow.json').write_text(dumps({'follow_parties': fol.get('parties') or {},
            'follow_people': [{k: v for k, v in pp.items() if k != 'email' or (v and not PERSONAL_MAIL.search(v))} for pp in (fol.get('people') or [])]}))
otd = load(ROOT / 'data' / 'onthisday.json', None)
if otd:
    (OUT / 'onthisday.json').write_text(dumps(otd))
    (OUT / 'onthisday').mkdir(exist_ok=True)   # one small file per calendar day for the Today feed
    for md, entries in (otd.get('days') or {}).items():
        (OUT / 'onthisday' / f'{md}.json').write_text(dumps({'days': {md: entries}, 'nzhistory_day_url': {md: (otd.get('nzhistory_day_url') or {}).get(md)}, 'licence_notes': otd.get('licence_notes')}))
(OUT / 'policies.json').write_text(dumps(policies))
(OUT / 'people.json').write_text(dumps(people))
if (OUT / 'thumbs.json').exists(): (OUT / 'thumbs.json').unlink()
# long-form pages: an index of titles plus four chunks loaded on demand (was one 5.6 MB file)
def page_group(k): return 'people' if '/people/' in k else 'parties' if k.startswith('parties/') else 'electorates' if k.startswith('electorates/') else 'docs'
def page_title(k, t):
    m = re.search(r'^#\s+(.+)$', t, re.M); return re.sub(r'[*_`]', '', m.group(1)).strip() if m else k
(OUT / 'pages').mkdir(exist_ok=True)
for grp in ('docs', 'parties', 'electorates', 'people'):
    (OUT / 'pages' / f'{grp}.json').write_text(json.dumps({k: v for k, v in pages.items() if page_group(k) == grp}, ensure_ascii=False))
(OUT / 'pages' / 'index.json').write_text(json.dumps({k: [page_group(k), page_title(k, v)] for k, v in pages.items()}, ensure_ascii=False))
if (OUT / 'pages.json').exists(): (OUT / 'pages.json').unlink()

# --- geo (electorate boundaries)
import shutil
(OUT / 'geo').mkdir(exist_ok=True)
for f in (ROOT / 'data' / 'geo').glob('*.json'): shutil.copy(f, OUT / 'geo' / f.name)

# --- assemble pages: artifact fragment (no doctype) + standalone index.html
# The app source is modular: site/src/shell.html (markup) + site/src/css/*.css + site/src/js/*.js, concatenated in
# filename order into one single-file page (the redesign of 23-24 Oct 2026; see site/redesign/ and docs/PORT_PLAN.md).
SRC = ROOT / 'site' / 'src'
css = '\n'.join(f.read_text() for f in sorted((SRC / 'css').glob('*.css')))
js = '\n'.join(f.read_text() for f in sorted((SRC / 'js').glob('*.js')))
src = (SRC / 'shell.html').read_text().replace('/* @CSS */', css).replace('/* @JS */', js)
HEAD = ('<!doctype html>\n<html lang="en-NZ"><head><meta charset="utf-8"><title>Ballot Book NZ — an independent guide to the 2026 election</title>'
        '<meta name="description" content="Independent, non-partisan guide to New Zealand\'s 7 November 2026 general election: how to vote, your electorate, every party and policy, polls and Parliament.">'
        '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 30 30%27%3E%3Ccircle cx=%2713%27 cy=%2716%27 r=%2711%27 fill=%27none%27 stroke=%27%23181a1f%27 stroke-width=%273%27/%3E%3Cpath d=%27M7.5 15.5l4.5 4.5L27 3.5%27 fill=%27none%27 stroke=%27%23d6246e%27 stroke-width=%273.5%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27/%3E%3C/svg%3E">'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>\n')
(ROOT / 'site' / 'artifact.html').write_text(src)
(ROOT / 'site' / 'index.html').write_text(HEAD + src + '\n</body></html>\n')
# new.html was the preview address during the port; keep it as a redirect so shared links still work
(ROOT / 'site' / 'new.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=./index.html"><title>Ballot Book NZ</title><a href="./index.html">Ballot Book NZ has moved to index.html</a>\n')
sz = {f.name: f.stat().st_size for f in OUT.rglob('*.json')}
print('parties', len(parties), 'policies', sum(len(v) for v in policies.values()), 'people', len(people), 'thumbs', len(thumbs),
      'elections', len(elections), 'parliaments', len(parliaments), 'pages', len(pages))
print('total data MB', round(sum(sz.values()) / 1e6, 1), 'largest', sorted(sz.items(), key=lambda x: -x[1])[:4])

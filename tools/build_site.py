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
LEAK_TERMS = re.compile(r"coalition|current Government|this Government|the Government's|Luxon Government|National-led|Labour-led|our party|our government|we will|we would|we are|Green Budget|KiwiMart|Kiwipower|Future Fund|Medicard|LabourSaver|FamilyBoost|Treaty Principles Bill|Regulatory Standards|Fast-track Approvals Act|Three Strikes|Fair Pay Agreements?|Roads of National Significance|Te Aka Whai Ora|Whānau Ora|Mana Motuhake|kaupapa M[āa]ori", re.I)
def leaks(t): return bool(LEAK_NAMES.search(t) or LEAK_TERMS.search(t))
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
            b = io.BytesIO(); im.save(b, 'JPEG', quality=72); thumbs[rec['folder']] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
            rec['photo_credit'] = p.get('photo_credit') or ''
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
         'quiz': load(ROOT / 'data' / 'guide' / 'quiz.json', {}),
         'compass': load(ROOT / 'data' / 'guide' / 'compass.json', {}), 'compass_parties': load(ROOT / 'data' / 'guide' / 'compass-parties.json', {})}
if isinstance(guide['parties'], dict): guide['parties'] = guide['parties'].get('parties', [])
if isinstance(guide['issues'], dict): guide['issues'] = guide['issues'].get('issues', [])
electorates = load(ROOT / 'data' / 'electorates' / '2026.json', [])
if isinstance(electorates, dict): electorates = electorates.get('electorates', [])
forecast = load(ROOT / 'data' / 'forecast.json', None)
bundle = {'forecast': forecast, 'upcoming': upcoming[0] if upcoming else None, 'guide': guide, 'electorates': electorates, 'generated': __import__('datetime').date.today().isoformat(), 'parties': parties, 'elections': elections,
          'parliaments': parliaments, 'polls': polls, 'promises': promises}
(OUT / 'bundle.json').write_text(dumps(bundle))
(OUT / 'policies.json').write_text(dumps(policies))
(OUT / 'people.json').write_text(dumps(people))
(OUT / 'thumbs.json').write_text(json.dumps(thumbs))
(OUT / 'pages.json').write_text(json.dumps(pages, ensure_ascii=False))

# --- geo (electorate boundaries)
import shutil
(OUT / 'geo').mkdir(exist_ok=True)
for f in (ROOT / 'data' / 'geo').glob('*.json'): shutil.copy(f, OUT / 'geo' / f.name)

# --- assemble pages: artifact fragment (no doctype) + standalone index.html
src = (ROOT / 'site' / 'src' / 'app.html').read_text()
design_css = (ROOT / 'site' / 'design' / 'tokens.css').read_text() + '\n' + (ROOT / 'site' / 'design' / 'components.css').read_text()
src = src.replace('<!-- DESIGN_CSS -->', '<style>\n' + design_css + '\n</style>', 1)
(ROOT / 'site' / 'artifact.html').write_text(src)
(ROOT / 'site' / 'index.html').write_text('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>\n' + src + '\n</body></html>\n')
sz = {f.name: f.stat().st_size for f in OUT.rglob('*.json')}
print('parties', len(parties), 'policies', sum(len(v) for v in policies.values()), 'people', len(people), 'thumbs', len(thumbs),
      'elections', len(elections), 'parliaments', len(parliaments), 'pages', len(pages))
print('total data MB', round(sum(sz.values()) / 1e6, 1), 'largest', sorted(sz.items(), key=lambda x: -x[1])[:4])

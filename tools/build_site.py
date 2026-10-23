#!/usr/bin/env python3
"""Bundle the archive into site/data/ for the interactive explorer (site/index.html).
Run after any data change:  python3 tools/build_site.py"""
import json, glob, pathlib, re, io, base64, os
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'site' / 'data'; OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'fulltext').mkdir(exist_ok=True)

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
elections = sorted([load(f) for f in glob.glob(str(ROOT / 'data' / 'elections' / '*.json'))], key=lambda e: e.get('year', 0) if e else 0)
elections = [e for e in elections if e]
parliaments = sorted([load(f) for f in glob.glob(str(ROOT / 'data' / 'parliaments' / '*.json'))], key=lambda p: p.get('parliament', 0) if p else 0)
parliaments = [p for p in parliaments if p]
polls = load(ROOT / 'data' / 'polls-2026.json', [])
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

# --- policies + full texts
policies = {}
for s in parties:
    d = ROOT / 'parties' / s / 'policies'
    pols = load(d / 'policies.json', []) or []
    if pols: policies[s] = pols
    docs = {}
    for f in sorted((d / 'documents').glob('*.md')) if (d / 'documents').exists() else []:
        fm, body = frontmatter(f.read_text(errors='replace'))
        docs['documents/' + f.name] = {'title': fm.get('title', f.stem), 'source_url': fm.get('source_url', ''),
                                       'retrieved': fm.get('retrieved', ''), 'text': body}
    if docs: (OUT / 'fulltext' / f'{s}.json').write_text(json.dumps(docs, ensure_ascii=False))
    parties[s]['document_count'] = len(docs)

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
    rec['party'] = rec.get('party') or d.parent.parent.name
    rec['bio'] = bio_excerpt(readme)
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
         + sorted((ROOT / 'parties').glob('*/track-record.md')) + [ROOT / 'parties' / 'MINOR_PARTIES.md']:
    if f.exists(): pages[str(f.relative_to(ROOT))] = f.read_text()

bundle = {'generated': __import__('datetime').date.today().isoformat(), 'parties': parties, 'elections': elections,
          'parliaments': parliaments, 'polls': polls, 'promises': promises}
(OUT / 'bundle.json').write_text(json.dumps(bundle, ensure_ascii=False))
(OUT / 'policies.json').write_text(json.dumps(policies, ensure_ascii=False))
(OUT / 'people.json').write_text(json.dumps(people, ensure_ascii=False))
(OUT / 'thumbs.json').write_text(json.dumps(thumbs))
(OUT / 'pages.json').write_text(json.dumps(pages, ensure_ascii=False))

# --- assemble pages: artifact fragment (no doctype) + standalone index.html
src = (ROOT / 'site' / 'src' / 'app.html').read_text()
(ROOT / 'site' / 'artifact.html').write_text(src)
(ROOT / 'site' / 'index.html').write_text('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>\n' + src + '\n</body></html>\n')
sz = {f.name: f.stat().st_size for f in OUT.rglob('*.json')}
print('parties', len(parties), 'policies', sum(len(v) for v in policies.values()), 'people', len(people), 'thumbs', len(thumbs),
      'elections', len(elections), 'parliaments', len(parliaments), 'pages', len(pages))
print('total data MB', round(sum(sz.values()) / 1e6, 1), 'largest', sorted(sz.items(), key=lambda x: -x[1])[:4])

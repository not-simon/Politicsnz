#!/usr/bin/env python3
"""Build parties/labour/people/<slug>/{person.json,README.md,photo.jpg} for Labour MPs (50th-54th
Parliaments) and 2026 candidates, from:
  - Wikipedia wikitext (cached by tools/people_labour_wiki.py) -> infobox offices, NZ parlbox rows, birth date, image
  - hand-written, sourced notes in tools/people_labour_notes/<slug>.md (front matter + sections)
  - existing person.json / README generated 2026-candidacy block (never modified)
Also writes parties/labour/people/README.md (index).
Usage: python3 tools/people_labour_build.py [slug ...]"""
import json, re, sys, io, pathlib, urllib.parse, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from people_labour_wiki import raw, get, ROOT
from people_labour_parse import person as wiki_person, clean

PEOPLE = ROOT / 'parties' / 'labour' / 'people'
NOTES = pathlib.Path(__file__).parent / 'people_labour_notes'
_sf = ROOT / 'raw' / 'people' / 'labour' / 'work' / 'shadow_current.json'
SHADOW = json.loads(_sf.read_text()) if _sf.exists() else {}
START, END = '<!-- GENERATED:2026-candidacy START -->', '<!-- GENERATED:2026-candidacy END -->'
ORDN = {'49th': 49, '50th': 50, '51st': 51, '52nd': 52, '53rd': 53, '54th': 54}
STATUS_LABEL = {'current-mp': 'Current MP', 'current-mp-standing-2026': 'Current MP, standing in 2026',
                'current-mp-retiring': 'Current MP, retiring at the 2026 election', 'former-mp': 'Former MP',
                'deceased': 'Deceased', 'candidate-2026': '2026 candidate (not previously an MP)',
                'former-mp-candidate-2026': 'Former MP, 2026 candidate', 'party-official': 'Party official'}


def slugify(name):
    import unicodedata
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    s = re.sub(r"['’`]", '', s.lower())
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def read_notes(slug):
    f = NOTES / f'{slug}.md'
    if not f.exists(): return {}, {}
    t = f.read_text()
    fm, body = {}, t
    m = re.match(r'---\n(.*?)\n---\n', t, re.S)
    if m:
        body = t[m.end():]
        for line in m.group(1).splitlines():
            if ':' not in line: continue
            k, v = line.split(':', 1); v = v.strip()
            if v.startswith('[') or v.startswith('{'):
                v = json.loads(v)
            elif v.isdigit():
                v = int(v)
            elif v in ('null', 'None', ''):
                v = None
            fm[k.strip()] = v
    secs = {}
    for part in re.split(r'^## ', body, flags=re.M)[1:]:
        h, _, txt = part.partition('\n'); secs[h.strip()] = txt.strip()
    return fm, secs


def years(s):
    m = re.findall(r'(\d{4})', s or '')
    return m[-1] if m else ''


def fmt_role(o):
    a, b = years(o['start']), years(o['end']) if o['end'] else ''
    if o['end'] and not b: b = '?'
    rng = f"{a}–{b}" if b and b != a else (f"{a}" if b == a else f"{a}–")
    return f"{o['office']} ({rng})" if a else o['office']


LICENSES = [(r'cc-by-sa-4\.0', 'CC BY-SA 4.0'), (r'cc-by-sa-3\.0', 'CC BY-SA 3.0'), (r'cc-by-sa-2\.5', 'CC BY-SA 2.5'),
            (r'cc-by-sa-2\.0', 'CC BY-SA 2.0'), (r'cc-by-4\.0', 'CC BY 4.0'), (r'cc-by-3\.0', 'CC BY 3.0'),
            (r'cc-by-2\.5', 'CC BY 2.5'), (r'cc-by-2\.0', 'CC BY 2.0'), (r'cc-zero|cc0', 'CC0 1.0'),
            (r'pd-[a-z-]*', 'Public domain'), (r'attribution', 'Attribution (Commons {{Attribution}})'),
            (r'gfdl', 'GFDL')]


def commons_meta(fname):
    w = raw('File:' + fname, host='commons.wikimedia.org')['wikitext']
    if not w:
        return {'photo_credit': '', 'photo_license': 'see Commons file page'}
    def field(k):
        m = re.search(r'\|\s*' + k + r'\s*=(.*?)(?=\n\s*\||\n\}\})', w, re.S | re.I)
        return clean(m.group(1)) if m else ''
    author = field('author') or field('Author') or field('photographer')
    author = re.sub(r'\{\{[^{}]*\}\}', '', author).strip()
    lic = ''
    low = w.lower()
    for pat, name in LICENSES:
        if re.search(r'\{\{\s*(?:self\|)?[^{}]*?' + pat, low):
            lic = name; break
    src = field('source')
    return {'photo_credit': author or 'See Commons file page', 'photo_license': lic or 'see Commons file page',
            'photo_original_source': src[:300]}


def fetch_photo(fname, dest):
    from PIL import Image
    import hashlib
    fn = fname.replace(' ', '_'); fn = fn[0].upper() + fn[1:]
    h = hashlib.md5(fn.encode('utf-8')).hexdigest()
    q = urllib.parse.quote(fn)
    data = None
    # Wikimedia only serves standard thumbnail widths (https://w.wiki/GHai); take 500px and downscale to 400
    for url in (f'https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/500px-{q}',
                f'https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/330px-{q}',
                f'https://upload.wikimedia.org/wikipedia/en/thumb/{h[0]}/{h[:2]}/{q}/500px-{q}',
                f'https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{q}'):
        try:
            data = get(url, binary=True, tries=3); break
        except IOError:
            continue
    if data is None: raise IOError('no image ' + fname)
    im = Image.open(io.BytesIO(data)).convert('RGB'); im.thumbnail((400, 400))
    im.save(dest, 'JPEG', quality=82)
    return 'https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(fname.replace(' ', '_'))


def urls_in(text):
    return list(dict.fromkeys(re.findall(r'\]\((https?://[^)\s]+)\)', text)))


def build(slug, title=None, roster_entry=None):
    fm, secs = read_notes(slug)
    title = fm.get('wikipedia') or title
    d = PEOPLE / slug; d.mkdir(parents=True, exist_ok=True)
    pj = d / 'person.json'
    ex = json.loads(pj.read_text()) if pj.exists() else {}
    w = wiki_person(title) if title else None
    if w and not w['parlbox'] and not w['offices'] and not w['born']:
        w = w  # article exists but sparse
    name = ex.get('name') or fm.get('name') or (w['name'] if w else slug)
    if fm.get('name'): name = fm['name']
    p = dict(ex)
    p['name'] = name; p['slug'] = slug
    p['party'] = fm.get('party') or ex.get('party') or 'labour'
    rows = [r for r in (w['parlbox'] if w else []) if r.get('term') in ORDN]
    parls = sorted({ORDN[r['term']] for r in rows}) or fm.get('parliaments') or []
    if roster_entry:
        parls = sorted(set(parls) | set(roster_entry.get('labour_parls', [])))
    if parls: p['parliaments'] = parls
    if fm.get('parliaments'): p['parliaments'] = fm['parliaments']
    fe = fm.get('first_elected')
    if not fe and rows:
        try: fe = int(years(rows[0].get('start', '')) or 0) or None
        except ValueError: fe = None
    if fe: p['first_elected'] = fe
    elecs = []
    for r in rows:
        e = (r.get('electorate') or '').strip()
        if e and e.lower() not in ('list', '') and e not in elecs: elecs.append(e)
    if fm.get('electorates') is not None: elecs = fm['electorates']
    if elecs: p['electorates'] = elecs
    if w and w['born']: p['born'] = w['born']
    if fm.get('born'): p['born'] = fm['born']
    if w and w.get('died'): p['died'] = w['died']
    if w: p['wikipedia'] = 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(w['title'].replace(' ', '_'))
    roles = [fmt_role(o) for o in (w['offices'] if w else []) if not o['office'].startswith('MP for')]
    roles += fm.get('roles_extra') or []
    sh = SHADOW.get(slug)
    if sh and sh['portfolios']:
        roles.insert(0, 'Labour shadow cabinet #%s (as of 11 Mar 2026): %s' % (sh['rank'], '; '.join(sh['portfolios'])))
    if roles: p['roles'] = roles
    for k in ('status', 'status_detail', 'party_history'):
        if fm.get(k) is not None: p[k] = fm[k]
    p.setdefault('status', 'former-mp' if parls else 'candidate-2026')
    if 'party_history' not in p:
        if parls:
            p['party_history'] = [{'party': 'labour', 'from': str(fe or ''), 'to': None if p['status'].startswith('current') else ''}]
    # photo
    if not (d / 'photo.jpg').exists() and w and w['image']:
        try:
            src = fetch_photo(w['image'], d / 'photo.jpg')
            meta = commons_meta(w['image'])
            p.update({'photo': 'photo.jpg', 'photo_source': src, 'photo_credit': meta['photo_credit'],
                      'photo_license': meta['photo_license']})
        except Exception as e:
            print('photo fail', slug, e, file=sys.stderr)
    elif (d / 'photo.jpg').exists():
        p.setdefault('photo', 'photo.jpg')
        p.setdefault('photo_license', 'Not stated (image supplied to policy.nz by the candidate/party)' if 'policy.nz' in p.get('photo_credit', '') else '')
    srcs = list(ex.get('sources', []))
    if p.get('wikipedia'): srcs.insert(0, p['wikipedia'])
    if sh and sh['portfolios']: srcs.append('https://en.wikipedia.org/wiki/Shadow_Cabinet_of_Chris_Hipkins')
    for s in secs.values(): srcs += urls_in(s)
    p['sources'] = list(dict.fromkeys(srcs))
    order = ['name', 'slug', 'party', 'party_history', 'status', 'status_detail', 'roles', 'parliaments', 'first_elected',
             'electorates', 'electorate_2026', 'list_rank_2026', 'born', 'died', 'wikipedia', 'photo', 'photo_source',
             'photo_credit', 'photo_license']
    p = {**{k: p[k] for k in order if k in p}, **{k: v for k, v in p.items() if k not in order}}
    pj.write_text(json.dumps(p, ensure_ascii=False, indent=1))
    # README
    rd = d / 'README.md'
    old = rd.read_text() if rd.exists() else ''
    m = re.search(re.escape(START) + '.*?' + re.escape(END), old, re.S)
    block = m.group(0) if m else None
    L = [f'# {name}', '']
    if (d / 'photo.jpg').exists():
        L += [f'<img src="photo.jpg" width="200" align="right" alt="{name}">', '']
    L += ['| | |', '|---|---|']
    ph = p.get('party_history') or []
    partytxt = 'Labour' if p['party'] == 'labour' else p['party']
    if p['party'] != 'labour': partytxt += ' (formerly Labour)'
    L.append(f'| **Party** | {partytxt} |')
    L.append(f"| **Status (Oct 2026)** | {STATUS_LABEL.get(p['status'], p['status'])} |")
    if p.get('born'):
        bp = (w or {}).get('birth_place') if w else ''
        L.append(f"| **Born** | {p['born']}{' — ' + bp if bp else ''} |")
    if p.get('died'): L.append(f"| **Died** | {p['died']} |")
    if p.get('electorates'): L.append(f"| **Electorate(s) held** | {', '.join(p['electorates'])} |")
    if p.get('parliaments'): L.append(f"| **Parliaments** | {', '.join(str(x) for x in p['parliaments'])} |")
    if p.get('first_elected'): L.append(f"| **First elected** | {p['first_elected']} |")
    if p.get('electorate_2026') or p.get('list_rank_2026'):
        L.append(f"| **2026 candidacy** | {p.get('electorate_2026') or 'List only'}{' · list #' + str(p['list_rank_2026']) if p.get('list_rank_2026') else ' · electorate only'} |")
    key = [r for r in (p.get('roles') or [])][:6]
    if key: L.append('| **Key roles** | ' + '<br>'.join(key) + ' |')
    if p.get('wikipedia'): L.append(f"| **Wikipedia** | [{(w or {}).get('title', name)}]({p['wikipedia']}) |")
    L.append('')
    L += ['## Current status', '', secs.get('Current status') or p.get('status_detail') or STATUS_LABEL.get(p['status'], ''), '']
    if secs.get('Biography'): L += ['## Biography', '', secs['Biography'], '']
    if rows or secs.get('Political career') or (w and w['offices']) or (sh and sh['portfolios']):
        L += ['## Political career', '']
        if rows:
            L += ['### Parliamentary terms', '', '| Parliament | Years | Electorate | List position | Party |', '|---|---|---|---|---|']
            for r in rows:
                pt = r.get('party', '').replace('New Zealand Labour Party', 'Labour')
                L.append(f"| {r.get('term','')} | {r.get('start','')}–{r.get('end','')} | {r.get('electorate') or 'List'} | {r.get('list','')} | {pt} |")
            L += ['', '_Source: Wikipedia parliamentary-term table._', '']
        offs = [o for o in (w['offices'] if w else []) if not o['office'].startswith('MP for')]
        if offs:
            L += ['### Offices held', '', '| Office | From | To | Prime Minister at the time |', '|---|---|---|---|']
            for o in offs:
                L.append(f"| {o['office']} | {o['start']} | {o['end'] or 'present'} | {o['pm'] or ''} |")
            L += ['', '_Source: Wikipedia infobox._', '']
        if sh and sh['portfolios']:
            L += ['### Opposition portfolios (as of 11 March 2026)', '', f"Rank {sh['rank']} in Chris Hipkins' shadow cabinet:", '']
            L += [f'- {x}' for x in sh['portfolios']]
            L += ['', '_Source: [Shadow Cabinet of Chris Hipkins](https://en.wikipedia.org/wiki/Shadow_Cabinet_of_Chris_Hipkins), list as of 11 March 2026._', '']
        if secs.get('Political career'): L += [secs['Political career'], '']
    for s in ('Record & notable actions', 'Controversies'):
        if secs.get(s): L += [f'## {s}', '', secs[s], '']
    for s, v in secs.items():
        if s not in ('Current status', 'Biography', 'Political career', 'Record & notable actions', 'Controversies', 'Sources'):
            L += [f'## {s}', '', v, '']
    if block:
        L += [block, '']
    else:
        L += ['## 2026 candidacy', '', secs.get('2026 candidacy note') or 'Not listed as a Labour candidate for the 2026 election on policy.nz (Oct 2026).', '']
    L += ['## Sources', '']
    L += [f'- {u}' for u in p['sources']]
    L += ['', f'_Profile compiled {datetime.date(2026, 10, 23).isoformat()} from the sources above; Wikipedia tables parsed by tools/people_labour_build.py._', '']
    txt = '\n'.join(L)
    txt = txt.replace('\n## 2026 candidacy note', '\n## 2026 candidacy note')
    rd.write_text(txt)
    return p


def main():
    roster = json.loads((ROOT / 'raw' / 'people' / 'labour' / 'work' / 'roster_final.json').read_text())
    only = set(sys.argv[1:])
    done = set()
    for e in roster:
        if only and e['slug'] not in only: continue
        build(e['slug'], e['title'], e); done.add(e['slug'])
    for d in sorted(PEOPLE.iterdir()):
        if d.is_dir() and d.name not in done and (not only or d.name in only):
            if any(e['slug'] == d.name for e in roster): continue
            build(d.name, None)
    print('built', len(done))


if __name__ == '__main__':
    main()

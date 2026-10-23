#!/usr/bin/env python3
"""Derive structured facts for National people from downloaded Wikipedia wikitext:
infobox offices/terms/electorates/majorities, birth/death, conscience votes (2013 marriage, 2019 EOLC,
2020 abortion third readings; 2022 conversion-practices third-reading 'against' list), official 2026 list rank.
Writes raw/people/national/derived.json"""
import json, os, re, glob, unicodedata
import mwparserfromhell as mw
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = os.path.join(ROOT, 'raw', 'people', 'national')
ALIAS = {'kanwaljit-singh-bakshi': 'kanwal-singh-bakshi', 'christopher-finlayson': 'chris-finlayson'}
def slugify(name):
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    s = re.sub(r'\([^)]*\)', '', s).lower().replace("'", '')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-'); return ALIAS.get(s, s)
def clean(v):
    if v is None: return ''
    s = str(v); s = re.sub(r'<ref[^>/]*/>', '', s); s = re.sub(r'<ref.*?</ref>', '', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = s.replace('{{!}}', '|'); s = re.sub(r'<br\s*/?>', '; ', s)
    code = mw.parse(s)
    for t in code.filter_templates(recursive=False):
        n = str(t.name).strip().lower()
        if n.startswith(('birth date', 'death date', 'start date', 'end date', 'dob')):
            nums = [str(p.value).strip() for p in t.params if not p.showkey]
            try:
                y, m, d = int(nums[0]), int(nums[1]), int(nums[2]); code.replace(t, f'{y:04d}-{m:02d}-{d:02d}')
            except Exception:
                code.replace(t, ' '.join(nums[:1]))
        elif n in ('nz electorate link',):
            code.replace(t, str(t.params[0].value).strip() if t.params else '')
        elif n in ('nowrap', 'small'):
            code.replace(t, str(t.params[0].value) if t.params else '')
        elif n in ('marriage',):
            code.replace(t, str(t.params[0].value) if t.params else '')
    out = code.strip_code()
    out = re.sub(r'\s+', ' ', out).strip()
    return out
def infobox(wt):
    code = mw.parse(wt)
    for t in code.filter_templates():
        if str(t.name).strip().lower().startswith('infobox'):
            return {str(p.name).strip(): p.value for p in t.params}
    return {}
def offices(ib):
    res = []
    keys = sorted({re.sub(r'\d+$', '', k) for k in ib}); idx = sorted({int(m.group(1)) for k in ib for m in [re.search(r'(\d+)$', k)] if m} | {0})
    for i in idx:
        sfx = '' if i == 0 else str(i)
        off = clean(ib.get('office' + sfx)); cons = clean(ib.get('constituency_MP' + sfx) or ib.get('constituency' + sfx))
        if not off and not cons: continue
        res.append({'office': off or None, 'constituency': cons or None,
                    'term_start': clean(ib.get('term_start' + sfx)), 'term_end': clean(ib.get('term_end' + sfx)),
                    'majority': clean(ib.get('majority' + sfx)) or None,
                    'predecessor': clean(ib.get('predecessor' + sfx)) or None, 'successor': clean(ib.get('successor' + sfx)) or None,
                    'order': clean(ib.get('order' + sfx)) or None})
    return res
def votes():
    C = os.path.join(D, 'context'); out = {}
    def table(fn, section_pat, key):
        w = open(os.path.join(C, fn)).read()
        m = re.search(section_pat, w); w = w[m.end():]
        w = w[:w.find('|}')]
        for row in re.split(r'\n\|-', w):
            if not re.search(r'[Pp]arty name with colou?r\|New Zealand National Party', row): continue
            cells = re.split(r'\n\|(?!\d)|\|\|', row)
            cells = [c for c in cells if 'National Party' not in c and c.strip()]
            labels = ['for', 'against', 'absent']
            for lab, c in zip(labels, cells):
                for l in re.findall(r'\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]', c):
                    out.setdefault(slugify(l.strip()), {})[key] = lab
    table('Marriage_(Definition_of_Marriage)_Amendment_Act_2013.wikitext', r'== Third reading ==', 'marriage_equality_2013_third_reading')
    table('End_of_Life_Choice_Act_2019.wikitext', r'=== Third Reading ===', 'end_of_life_choice_2019_third_reading')
    table('Abortion_Legislation_Act_2020.wikitext', r'===Third reading===', 'abortion_legislation_2020_third_reading')
    for n in ['Simon Bridges', 'Simeon Brown', 'Melissa Lee', 'Todd McClay', "Simon O'Connor", 'Chris Penk', 'Michael Woodhouse', 'Shane Reti']:
        out.setdefault(slugify(n), {})['conversion_practices_2022_third_reading'] = 'against'
    return out
def official_ranks():
    from bs4 import BeautifulSoup
    t = BeautifulSoup(open(os.path.join(D, 'ec', 'party-lists.html')).read(), 'html.parser').get_text(' ', strip=True)
    seg = t[t.find('National Party LUXON'):t.find('New Zealand First Party PETERS')][len('National Party '):]
    names = re.findall(r"([A-Za-z'\- ]*[A-Z][A-Za-z'\-]+), ((?:(?![A-Z]{2,}[a-z]*[ ,]|[A-Z][a-z]*[A-Z]{2,})[^\s,]+ ?)+)", seg)
    return names, seg
mps = json.load(open(os.path.join(D, 'mps.json')))
derived = {}
V = votes()
for f in sorted(glob.glob(os.path.join(D, 'wiki', '*.json'))):
    r = json.load(open(f)); ib = infobox(r['wikitext'])
    derived[r['slug']] = {'wiki_title': r['title'], 'wikipedia': r['url'],
        'born': clean(ib.get('birth_date')), 'birth_place': clean(ib.get('birth_place')),
        'died': clean(ib.get('death_date')) or None, 'birth_name': clean(ib.get('birth_name')) or None,
        'education': clean(ib.get('education') or ib.get('alma_mater')) or None,
        'occupation': clean(ib.get('occupation') or ib.get('profession')) or None,
        'other_party': clean(ib.get('otherparty')) or None, 'party_ib': clean(ib.get('party')) or None,
        'offices': offices(ib), 'votes': V.get(r['slug'], {}),
        'parliaments_50_54': mps.get(r['query_title'], {}).get('parliaments', [])}
json.dump(derived, open(os.path.join(D, 'derived.json'), 'w'), indent=1, ensure_ascii=False)
print(len(derived), 'people;', sum(1 for v in derived.values() if v['votes']), 'with votes')

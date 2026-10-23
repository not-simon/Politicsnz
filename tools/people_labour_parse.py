#!/usr/bin/env python3
"""Parse Wikipedia wikitext of NZ MPs: infobox offices, NZ parlbox rows, birth date, image, and a
reference-annotated plain-text rendering (for the researcher to read when writing profiles).
Usage: python3 tools/people_labour_parse.py <Wikipedia title> [--text] [--sections a,b]"""
import re, sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from people_labour_wiki import raw

MONTHS = {m: i for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                      'September', 'October', 'November', 'December'], 1)}


def find_template(wt, name):
    """Return the full text of the first {{name ...}} template (balanced braces)."""
    m = re.search(r'\{\{\s*' + name, wt, re.I)
    if not m: return ''
    i, depth = m.start(), 0
    while i < len(wt):
        if wt.startswith('{{', i): depth += 1; i += 2; continue
        if wt.startswith('}}', i):
            depth -= 1; i += 2
            if depth == 0: return wt[m.start():i]
            continue
        i += 1
    return wt[m.start():]


def strip_refs(t):
    t = re.sub(r'<ref[^>]*/>', '', t)
    t = re.sub(r'<ref[^>]*>.*?</ref>', '', t, flags=re.S)
    return re.sub(r'<!--.*?-->', '', t, flags=re.S)


def delink(t):
    t = re.sub(r'\[\[(?:File|Image):[^\[\]]*(?:\[\[[^\]]*\]\][^\[\]]*)*\]\]', '', t)
    t = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[\[([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[https?://\S+ ([^\]]*)\]', r'\1', t)
    return t


def simple_templates(t):
    t = re.sub(r'\{\{(?:nowrap|small|nobr)\|([^{}]*)\}\}', r'\1', t, flags=re.I)
    t = re.sub(r'\{\{NZ electorate link\|([^{}|]*)[^{}]*\}\}', r'\1', t, flags=re.I)
    t = re.sub(r'\{\{(?:Party name with colou?r|party name with colou?r)\|([^{}|]*)[^{}]*\}\}', r'\1', t)
    t = re.sub(r'\{\{NZ election link year\|(\d{4})\}\}', r'\1', t)
    t = re.sub(r'\{\{(?:birth|death)[^|{}]*\|(?:\s*[a-z]+\s*=\s*[a-z]*\s*\|)*\s*(\d{4})\s*\|\s*(\d{1,2})\s*\|\s*(\d{1,2})[^{}]*\}\}',
               lambda m: f'{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}', t, flags=re.I)
    t = re.sub(r'\{\{\s*br\s*\}\}', ' ', t, flags=re.I)
    t = re.sub(r'\{\{By-election link year\|[^{}|]*\|(\d{4})[^{}]*\}\}', r'\1 (by-election)', t, flags=re.I)
    t = re.sub(r'\{\{birth based on age as of date\s*\|\s*(\d{1,3})\s*\|\s*(\d{4})[^{}]*\}\}',
               lambda m: f'{int(m.group(2)) - int(m.group(1)) - 1} or {int(m.group(2)) - int(m.group(1))}', t, flags=re.I)
    t = re.sub(r'\{\{(?:birth|death)[^|{}]*\|(?:\s*[a-z]+\s*=\s*[a-z]*\s*\|)*\s*(\d{4})[^{}]*\}\}', r'\1', t, flags=re.I)
    t = re.sub(r'\{\{post-nominals[^{}]*\}\}', '', t, flags=re.I)
    t = re.sub(r'\{\{(?:lang|langx)\|[a-z]+\|([^{}|]*)[^{}]*\}\}', r'\1', t, flags=re.I)
    t = re.sub(r'\{\{(?:ndash|snd|spaced ndash)\}\}', '–', t, flags=re.I)
    t = re.sub(r'\{\{(?:marriage)\|([^{}|]*)\|?([^{}]*)\}\}', r'\1 (m. \2)', t, flags=re.I)
    return t


def clean(t):
    t = strip_refs(t)
    t = re.sub(r'^[^\[\]|{}]*\{\{!\}\}', '', t.strip())  # bare 'Target{{!}}Label' -> 'Label'
    t = t.replace('{{!}}', '|')
    t = re.sub(r'\{\{(?:spaced en dash space|spaced en dash|en dash|ndash|snd)\}\}', ' – ', t, flags=re.I)
    for _ in range(3): t = simple_templates(t)
    t = delink(t)
    t = re.sub(r"'{2,}", '', t)
    t = re.sub(r'<br\s*/?>', '; ', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = t.replace('&nbsp;', ' ').replace('&ndash;', '–')
    return re.sub(r'\s+', ' ', t).strip()


def infobox(wt):
    box = find_template(wt, 'Infobox')
    fields = {}
    for m in re.finditer(r'^\s*\|\s*([a-zA-Z_0-9]+)\s*=(.*?)(?=^\s*\||^\}\}|\Z|^\{\{Collapsed)', box, re.M | re.S):
        k, v = m.group(1).strip(), m.group(2).strip()
        if v and k not in fields: fields[k] = v
    return fields


def offices(ib):
    out = []
    keys = sorted({re.sub(r'\D', '', k) for k in ib if re.match(r'(office|constituency_MP|constituency_mp|title|order)\d*$', k)},
                  key=lambda x: int(x or 0))
    for n in keys:
        off = ib.get('office' + n) or ib.get('title' + n)
        if not off and re.search(r'[A-Za-z]{4,}', re.sub(r'^\d+(st|nd|rd|th)\s*', '', clean(ib.get('order' + n, '')))):
            off = ib.get('order' + n); ib = dict(ib); ib['order' + n] = ''
        cons = ib.get('constituency_MP' + n) or ib.get('constituency_mp' + n)
        name = clean(off) if off else (('MP for ' + clean(cons)) if cons else None)
        if not name: continue
        order = clean(ib.get('order' + n, ''))
        if order and not name.startswith(order): name = order + ' ' + name
        out.append({'office': name, 'start': clean(ib.get('term_start' + n, '')), 'end': clean(ib.get('term_end' + n, '')) or None,
                    'pm': clean(ib.get('primeminister' + n, '') or ib.get('prime_minister' + n, '')) or None})
    return out


def parlbox(wt):
    rows = []
    for m in re.finditer(r'\{\{NZ parlbox\s*\|((?:[^{}]|\{\{[^{}]*\}\})*)\}\}', wt):
        d = {}
        for part in re.split(r'\|(?![^{]*\}\})(?![^\[]*\]\])', m.group(1)):
            if '=' in part:
                k, v = part.split('=', 1); d[k.strip()] = clean(v)
        rows.append(d)
    return rows


def ref_annotated(t):
    """Plain text with refs replaced by [U:url] markers (first URL in ref)."""
    named = {}
    def r(m):
        body = m.group(0)
        u = re.search(r'url\s*=\s*(https?://[^\s|}]+)', body)
        nm = re.search(r'name\s*=\s*"?([^">/]+)"?', body)
        url = u.group(1) if u else ''
        if nm and url: named[nm.group(1).strip()] = url
        return f' [U:{url}]' if url else ''
    t = re.sub(r'<ref[^>/]*>.*?</ref>', r, t, flags=re.S)
    t = re.sub(r'<ref\s+name\s*=\s*"?([^">/]+?)"?\s*/>', lambda m: f' [U:{named.get(m.group(1).strip(), "")}]' if named.get(m.group(1).strip()) else '', t)
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    for _ in range(3): t = simple_templates(t)
    t = re.sub(r'\{\{(?:Infobox|Collapsed|NZ parlbox|End|Short description|Use |Main|See also|Further|For |Redirect|Ministers|Navboxes|Authority|Sixth|Fifth|Labour|Portal|Cite|Reflist|Commons|Chris |Jacinda|Current|Persondata|DEFAULTSORT)[^{}]*(?:\{\{[^{}]*\}\}[^{}]*)*\}\}', '', t, flags=re.S | re.I)
    t = re.sub(r'\{\{[^{}]*(?:\{\{[^{}]*\}\}[^{}]*)*\}\}', '', t)
    t = re.sub(r'\{\|.*?\|\}', '[table omitted]', t, flags=re.S)
    t = delink(t)
    t = re.sub(r"'{2,}", '', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'\[\[Category:[^\]]*\]\]', '', t)
    return re.sub(r'\n{3,}', '\n\n', t)


def person(title):
    w = raw(title); wt = w['wikitext']
    ib = infobox(wt)
    born = clean(ib.get('birth_date', '')) if ib.get('birth_date') else ''
    died = clean(ib.get('death_date', '')) if ib.get('death_date') else ''
    img = re.sub(r'^(File|Image):', '', clean(ib.get('image', '')).split('|')[0]).strip()
    return {'title': w['title'], 'name': clean(ib.get('name', '')) or w['title'], 'born': born, 'died': died,
            'birth_place': clean(ib.get('birth_place', '')), 'image': img, 'offices': offices(ib), 'parlbox': parlbox(wt),
            'party': clean(ib.get('party', '')), 'otherparty': clean(ib.get('otherparty', '')),
            'education': clean(ib.get('alma_mater', '') or ib.get('education', '')), 'spouse': clean(ib.get('spouse', '')),
            'occupation': clean(ib.get('occupation', '') or ib.get('profession', ''))}


if __name__ == '__main__':
    t = sys.argv[1]
    if '--text' in sys.argv:
        wt = raw(t)['wikitext']
        txt = ref_annotated(wt)
        if '--short' in sys.argv:
            txt = re.sub(r' \[U:[^\]]*\]', '', txt)
        print(txt)
    else:
        print(json.dumps(person(t), ensure_ascii=False, indent=1))

#!/usr/bin/env python3
"""Fetch ACT New Zealand 2026 policy sources (run with python3 -I).

Inputs : raw/policy.nz/parties/act-party.json (citations), act.org.nz sitemap.
Outputs: raw/party-docs/act/html/*.html, raw/party-docs/act/pdf/*.pdf (+ .txt),
         raw/party-docs/act/fetched.json  (url -> {slug, kind, title, text, links, ...})
Extraction: act.org.nz is a Framer site. Desktop-hidden SSR variants are dropped,
then block elements (headings, paragraphs, list items) inside #main are emitted in
document order between the page's "Back"/menu header and the "Stay up to date" footer.
"""
import json, os, re, subprocess, sys, time, urllib.parse, hashlib
from bs4 import BeautifulSoup

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW = os.path.join(ROOT, 'raw', 'party-docs', 'act')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
os.makedirs(os.path.join(RAW, 'html'), exist_ok=True)
os.makedirs(os.path.join(RAW, 'pdf'), exist_ok=True)

EXTRA_FOLLOW = {'https://www.act.org.nz/news/act-time-to-end-voting-rights-for-unelected-council-appointees'}
SKIP_PATHS = {'', 'form', 'people', 'thank-you', 'privacy-policy', 'news', 'overseas', 'kiwisaver-calculator'}


def orig(u):
    u = u.strip()
    return re.sub(r'^(https?://web\.archive\.org)?/web/\d+[a-z_]*/', '', u)


def curl(url, out):
    r = subprocess.run(['curl', '-sS', '-L', '--max-time', '90', '-A', UA, '-o', out,
                        '-w', '%{http_code} %{url_effective} %{content_type}', url],
                       capture_output=True, text=True)
    parts = (r.stdout or '').split(' ', 2)
    code = parts[0] if parts else '000'
    return code, (parts[1] if len(parts) > 1 else url), (parts[2] if len(parts) > 2 else ''), r.stderr.strip()


def slug_for(url):
    p = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(p.path).strip('/')
    if p.netloc.endswith('nationbuilder.com') or path.lower().endswith('.pdf'):
        base = os.path.basename(path)
        base = re.sub(r'\.pdf$', '', base, flags=re.I)
        s = 'pdf-' + base
    elif 'scoop.co.nz' in p.netloc:
        s = 'scoop-' + os.path.basename(path).replace('.htm', '')
    elif path.startswith('news/'):
        s = 'news-' + path[5:]
    elif path.startswith('policies/'):
        s = 'policies-' + path[9:]
    else:
        s = path or 'home'
    s = s.lower().replace('’', '').replace("'", '').replace('‘', '')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:90]


BLOCKS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'blockquote']


def framer_extract(html, base_url):
    s = BeautifulSoup(html, 'html.parser')
    title = s.title.get_text(strip=True) if s.title else ''
    css = ' '.join(t.get_text() for t in s.find_all('style'))
    desktop_hidden = set(re.findall(r'@media\s*\(min-width:\s*1200px\)\s*\{\s*\.(hidden-[a-z0-9]+)', css))
    for t in s(['script', 'style', 'noscript', 'svg', 'link']):
        t.decompose()
    for el in s.find_all(class_='ssr-variant'):
        if desktop_hidden & set(el.get('class') or []):
            el.decompose()
    for el in s.find_all(class_=lambda c: c and any(x in desktop_hidden for x in (c if isinstance(c, list) else [c]))):
        el.decompose()
    main = s.find(id='main') or s.body
    items = []
    for el in main.find_all(BLOCKS):
        if el.find_parent(BLOCKS):
            continue
        txt = re.sub(r'[ \t ]+', ' ', el.get_text(' ', strip=True)).strip()
        txt = re.sub(r' ([,.;:!?])', r'\1', txt)
        if not txt:
            continue
        items.append((el.name, txt, el))
    texts = [t for _, t, _ in items]
    start = 0
    if 'Back' in texts:
        start = texts.index('Back') + 1
    else:
        while start < len(texts) and texts[start] == 'Menu':
            start += 1
    end = texts.index('Stay up to date') if 'Stay up to date' in texts else len(texts)
    body = items[start:end]
    lines, links = [], []
    for name, txt, el in body:
        if name.startswith('h'):
            lines.append('#' * (int(name[1]) + 1) + ' ' + txt)  # h1 -> ## (doc title is #)
        elif name == 'li':
            lines.append('- ' + txt)
        elif name == 'blockquote':
            lines.append('> ' + txt)
        else:
            lines.append(txt)
        for a in el.find_all('a', href=True):
            links.append({'text': a.get_text(' ', strip=True), 'href': urllib.parse.urljoin(base_url, a['href'])})
    # also links that are not inside block elements but sit in the content region (buttons)
    region_links = []
    for a in main.find_all('a', href=True):
        h = urllib.parse.urljoin(base_url, a['href'])
        region_links.append({'text': a.get_text(' ', strip=True), 'href': h})
    h1 = next((t for n, t, _ in body if n == 'h1'), '')
    return {'page_title': title, 'h1': h1, 'blocks': lines, 'links': links, 'all_links': region_links}


def scoop_extract(html, base_url):
    s = BeautifulSoup(html, 'html.parser')
    for t in s(['script', 'style', 'noscript', 'svg']):
        t.decompose()
    art = s.find(id='article') or s.body
    h1 = s.find('h1').get_text(' ', strip=True) if s.find('h1') else ''
    by = art.find(class_='byline')
    lines = []
    if by:
        lines.append(re.sub(r'\s+', ' ', by.get_text(' ', strip=True)))
    for el in art.find_all(['h2', 'h3', 'p', 'li']):
        if el.find(['p', 'li', 'h2', 'h3']):
            continue  # keep innermost blocks only (Scoop markup has unclosed <p>)
        txt = re.sub(r'\s+', ' ', el.get_text(' ', strip=True)).strip()
        if not txt or txt.startswith('Advertisement - scroll'):
            continue
        if txt.startswith('© Scoop Media'):
            break
        lines.append(('### ' + txt) if el.name in ('h2', 'h3') else txt)
    return {'page_title': s.title.get_text(strip=True) if s.title else '', 'h1': h1, 'blocks': lines, 'links': [], 'all_links': []}


def generic_extract(html, base_url):
    """Non-Framer, non-Scoop pages (e.g. the balancethebooks.nz microsite): every visible text node, in order."""
    s = BeautifulSoup(html, 'html.parser')
    for t in s(['script', 'style', 'noscript', 'svg', 'template']):
        t.decompose()
    h1 = s.find('h1').get_text(' ', strip=True) if s.find('h1') else ''
    lines = []
    for line in s.body.get_text('\n', strip=True).split('\n'):
        line = re.sub(r'\s+', ' ', line).strip()
        if line:
            lines.append(line)
    links = [{'text': a.get_text(' ', strip=True), 'href': urllib.parse.urljoin(base_url, a['href'])}
             for a in s.find_all('a', href=True)]
    return {'page_title': s.title.get_text(strip=True) if s.title else '', 'h1': h1, 'blocks': lines,
            'links': links, 'all_links': [], 'extraction': 'all visible text nodes (interactive page; live counters show their initial value)'}


def fetch(url, store, meta=None):
    if url in store and store[url].get('ok'):
        return store[url]
    slug = slug_for(url)
    is_pdf = '.pdf' in url.lower()
    out = os.path.join(RAW, 'pdf' if is_pdf else 'html', slug + ('.pdf' if is_pdf else '.download'))
    code, eff, ctype, err = curl(url, out)
    rec = {'url': url, 'slug': slug, 'http': code, 'final_url': eff, 'content_type': ctype,
           'retrieved': time.strftime('%Y-%m-%d'), 'ok': False, 'error': err}
    rec.update(meta or {})
    if code != '200':
        rec['error'] = f'HTTP {code} {err}'.strip()
        store[url] = rec
        return rec
    if 'pdf' in ctype or is_pdf:
        rec['kind'] = 'pdf'
        if not out.endswith('.pdf') or os.path.dirname(out).endswith('html'):
            newout = os.path.join(RAW, 'pdf', os.path.basename(out).rsplit('.', 1)[0] + '.pdf')
            os.replace(out, newout); out = newout
        txt = out[:-4] + '.txt'
        subprocess.run(['pdftotext', '-layout', out, txt])
        t = open(txt, encoding='utf-8', errors='replace').read() if os.path.exists(txt) else ''
        rec['text'] = t
        rec['raw_file'] = os.path.relpath(out, ROOT)
        rec['size'] = os.path.getsize(out)
        info = subprocess.run(['pdfinfo', out], capture_output=True, text=True).stdout
        m = re.search(r'^Pages:\s+(\d+)', info, re.M)
        rec['pages'] = int(m.group(1)) if m else None
        rec['ok'] = bool(t.strip())
        if not rec['ok']:
            rec['error'] = 'pdftotext produced no text (image-only PDF?)'
        if rec['size'] > 10 * 1024 * 1024:
            os.remove(out); rec['raw_file'] = None
    else:
        rec['kind'] = 'html'
        newout = out[:-len('.download')] + '.html' if out.endswith('.download') else out
        os.replace(out, newout); out = newout
        html = open(out, encoding='utf-8', errors='replace').read()
        if 'scoop.co.nz' in eff:
            ex = scoop_extract(html, eff)
        elif 'act.org.nz' in urllib.parse.urlparse(eff).netloc:
            ex = framer_extract(html, eff)
        else:
            ex = generic_extract(html, eff)
        rec.update(ex)
        rec['raw_file'] = os.path.relpath(out, ROOT)
        rec['ok'] = len(ex['blocks']) > 0
        if not rec['ok']:
            rec['error'] = 'no content extracted'
    store[url] = rec
    print(code, slug, rec.get('kind'), 'ok' if rec['ok'] else 'FAIL', file=sys.stderr)
    return rec


def main():
    store_path = os.path.join(RAW, 'fetched.json')
    store = json.load(open(store_path)) if os.path.exists(store_path) else {}
    d = json.load(open(os.path.join(ROOT, 'raw', 'policy.nz', 'parties', 'act-party.json')))
    urls = []
    for p in d['policies']:
        for c in p.get('citations', []):
            o = orig(c['url'])
            if o not in urls:
                urls.append(o)
    sm = os.path.join(RAW, 'sitemap_en-NZ.xml')
    curl('https://www.act.org.nz/sitemap_en-NZ.xml', sm)
    locs = re.findall(r'<loc>([^<]+)</loc>', open(sm).read())
    site_pages = []
    for l in locs:
        path = urllib.parse.urlparse(l).path.strip('/')
        if path.startswith('news/') or path.startswith('people/') or path in SKIP_PATHS or path.endswith('-record'):
            continue
        site_pages.append(l)
    for u in urls:
        fetch(u, store, {'cited_by_policynz': True})
    for u in site_pages:
        fetch(u, store, {'from_sitemap': True})
    # follow "Read the full policy" and PDF links inside page content
    for u in [k for k, v in store.items() if 'action.act.org.nz/r?' in k]:
        del store[u]
    for u in list(store):
        r = store[u]
        if r.get('kind') != 'html':
            continue
        for a in r.get('links', []) + r.get('all_links', []):
            h = a['href']
            if 'Constitution' in h or '250713_ACT' in h:
                continue
            txt = a['text'].lower()
            short = re.match(r'^https?://(www\.)?act\.org\.nz/[a-z0-9]+_[a-z0-9_]+/?$', h)
            if 'action.act.org.nz/r?' in h:
                continue  # email click-tracking redirects (not fetchable)
            if ('nationbuilder.com' in h and '.pdf' in h.lower()) or 'full policy' in txt or 'read the policy' in txt \
                    or 'download' in txt or short or h in EXTRA_FOLLOW:
                rr = fetch(h, store, {'linked_from': u})
                key = rr['url']
                r.setdefault('full_policy_links', [])
                if key not in r['full_policy_links']:
                    r['full_policy_links'].append(key)
    json.dump(store, open(store_path, 'w'), indent=1, ensure_ascii=False)
    print('total', len(store), 'failed', [u for u, r in store.items() if not r['ok']], file=sys.stderr)


if __name__ == '__main__':
    main()

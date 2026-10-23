#!/usr/bin/env python3
"""Fetch National Party 2026 policy sources (policy.nz citations, national.org.nz policy hub,
campaign-period news releases, linked PDFs) into raw/party-docs/national/.

Usage: python3 -I tools/policies_national_fetch.py [urls|hub|news|pdfs|all]
Outputs: raw/party-docs/national/html/<slug>.html, raw/party-docs/national/pdf/<name>.pdf,
         raw/party-docs/national/fetch_log.json
"""
import json, os, re, sys, hashlib, subprocess, urllib.parse
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'raw', 'party-docs', 'national')
HTML = os.path.join(RAW, 'html'); PDF = os.path.join(RAW, 'pdf')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
os.makedirs(HTML, exist_ok=True); os.makedirs(PDF, exist_ok=True)
LOG = os.path.join(RAW, 'fetch_log.json')
log = json.load(open(LOG)) if os.path.exists(LOG) else {}


def orig(u):
    u = re.sub(r'^https?://web\.archive\.org/(web|save)/(\d+[a-z_]*/)?', '', u)
    u = re.sub(r'^/web/\d+[a-z_]*/', '', u)
    return u


def key_for(u):
    p = urllib.parse.urlparse(u)
    if p.path.lower().endswith('.pdf'):
        return 'pdf', urllib.parse.unquote(os.path.basename(p.path))
    s = (p.netloc.replace('www.', '') + p.path).strip('/').replace('/', '__')
    s = re.sub(r'[^A-Za-z0-9_.-]', '-', s)
    return 'html', s + '.html'


def fetch(u):
    kind, name = key_for(u)
    out = os.path.join(PDF if kind == 'pdf' else HTML, name)
    if os.path.exists(out) and os.path.getsize(out) > 0 and log.get(u, {}).get('status') == 200:
        return u, log[u]
    r = subprocess.run(['curl', '-sS', '-L', '--max-time', '120', '-A', UA, '-o', out, '-w', '%{http_code}', u],
                       capture_output=True, text=True)
    code = int(r.stdout.strip() or 0) if r.stdout.strip().isdigit() else 0
    info = {'status': code, 'file': os.path.relpath(out, ROOT), 'kind': kind, 'err': r.stderr.strip()[:300]}
    if code != 200 and os.path.exists(out):
        os.remove(out)
    return u, info


def run(urls):
    with ThreadPoolExecutor(8) as ex:
        for u, info in ex.map(fetch, urls):
            log[u] = info
            if info['status'] != 200:
                print('FAIL', info['status'], u, info['err'])
    json.dump(log, open(LOG, 'w'), indent=1)


def policynz_urls():
    d = json.load(open(os.path.join(ROOT, 'raw/policy.nz/parties/national-party.json')))
    s = set()
    for p in d['policies']:
        for c in p.get('citations', []):
            s.add(orig(c['url']))
    return sorted(s)


def sitemap_urls():
    sm = open(os.path.join(RAW, 'sitemap.xml')).read()
    return re.findall(r'<loc>([^<]+)</loc>', sm)


def hub_urls():
    sm = sitemap_urls()
    idx = os.path.join(HTML, 'national.org.nz__policies.html')
    hrefs = set(re.findall(r'href="(/policies/[^"#?]+)"', open(idx).read())) if os.path.exists(idx) else set()
    u = {x for x in sm if '/policies' in x} | {'https://www.national.org.nz' + h for h in hrefs}
    u |= {'https://www.national.org.nz/plan', 'https://www.national.org.nz/policies'}
    return sorted(u)


def news_urls():
    out = []
    for x in sitemap_urls():
        m = re.search(r'/news/(\d+)', x)
        if not m:
            continue
        d = m.group(1)
        d = d[2:] if len(d) >= 8 else d  # 20260705 -> 260705
        if d[:4] >= '2606':
            out.append(x)
    return sorted(out)


def pdf_links():
    s = set()
    for f in os.listdir(HTML):
        t = open(os.path.join(HTML, f), errors='replace').read()
        for m in re.findall(r'https://assets\.national\.org\.nz/web/prod/[^"\\\s<>&]+?\.pdf(?:\?v=\d+)?', t):
            s.add(m)
    return sorted(s)


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('urls', 'all'):
        run(policynz_urls())
    if what in ('hub', 'all'):
        run(hub_urls())
    if what in ('news', 'all'):
        run(news_urls())
    if what in ('pdfs', 'all'):
        run(pdf_links())
    print(len(log), 'urls logged;', sum(1 for v in log.values() if v['status'] == 200), 'ok')

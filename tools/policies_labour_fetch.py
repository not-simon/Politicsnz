#!/usr/bin/env python3
"""Fetch every source cited by policy.nz for Labour + every page on labour.org.nz's policy hub.

Usage: python3 -I tools/policies_labour_fetch.py
Writes raw HTML/PDF into raw/party-docs/labour/{html,pdf}/ and an index raw/party-docs/labour/fetch_index.json
(url -> {file, status, final_url, content_type, slug}).
"""
import json, os, re, subprocess, sys, time, hashlib
from urllib.parse import urlparse, urljoin

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'raw', 'party-docs', 'labour')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'


def original_url(u):
    u = u.strip()
    if not re.match(r'https?://', u):
        u = 'https://' + u
    m = re.match(r'https?://(?:web|wayback-api)\.archive\.org/(?:web/[0-9a-z_*]+|save)/(.*)$', u)
    if m:
        u = m.group(1)
        if not re.match(r'https?://', u):
            u = 'https://' + u
    # drop google analytics linker params
    u = re.sub(r'[?&]_gl=[^#]*', '', u)
    return u


def slug_for(u):
    p = urlparse(u)
    host = p.netloc.replace('www.', '')
    path = p.path.strip('/')
    if host == 'labour.org.nz':
        s = path.replace('news/', '').replace('/', '-') or 'home'
    elif host == 'scoop.co.nz':
        s = 'scoop-' + path.split('/')[-1].replace('.htm', '')
    elif host == 'rnz.co.nz':
        s = 'rnz-' + path.split('/')[-1]
    else:
        s = host.split('.')[0] + '-' + path.replace('/', '-')
    s = re.sub(r'[^a-z0-9-]+', '-', s.lower()).strip('-')
    return s[:90].rstrip('-')


def curl(url, out):
    r = subprocess.run(['curl', '-sS', '-L', '--max-time', '60', '-A', UA, '-o', out,
                        '-w', '%{http_code}\t%{url_effective}\t%{content_type}', url],
                       capture_output=True, text=True)
    parts = (r.stdout or '').split('\t')
    code = parts[0] if parts else ''
    return {'status': code, 'final_url': parts[1] if len(parts) > 1 else '',
            'content_type': parts[2] if len(parts) > 2 else '', 'err': r.stderr.strip()}


def main():
    os.makedirs(os.path.join(RAW, 'html'), exist_ok=True)
    os.makedirs(os.path.join(RAW, 'pdf'), exist_ok=True)
    pj = json.load(open(os.path.join(ROOT, 'raw', 'policy.nz', 'parties', 'labour-party.json')))
    urls = []
    for pol in pj['policies']:
        for c in pol.get('citations', []):
            if c.get('url'):
                urls.append(original_url(c['url']))
    # policy hub pages
    hub = open(os.path.join(RAW, 'html', 'policy.html')).read() if os.path.exists(os.path.join(RAW, 'html', 'policy.html')) else ''
    skip = re.compile(r"^/(css|media|api|donate|join-labour|contact|shop|volunteer|privacy-policy|party-information|redirects|news/?$|our-policies|priority-pages|#|$)")
    for h in re.findall(r'href="(/[^"#?]*)', hub):
        if not skip.match(h) and h != '/':
            urls.append('https://www.labour.org.nz' + h.rstrip('/'))
    for extra in ['https://www.labour.org.nz/policy', 'https://www.labour.org.nz/costofliving', 'https://www.labour.org.nz/healthcare',
                  'https://www.labour.org.nz/homes', 'https://www.labour.org.nz/jobs',
                  'https://www.labour.org.nz/community-housing-and-retirement-villages']:
        urls.append(extra)
    urls.extend(sys.argv[1:])
    idx_path = os.path.join(RAW, 'fetch_index.json')
    idx = json.load(open(idx_path)) if os.path.exists(idx_path) else {}
    seen = []
    for u in urls:
        if u.rstrip('/') in [s.rstrip('/') for s in seen]:
            continue
        seen.append(u)
        if u in idx and idx[u].get('status') == '200':
            continue
        slug = slug_for(u)
        out = os.path.join(RAW, 'html', slug + '.html')
        res = curl(u, out)
        if 'pdf' in res['content_type']:
            newout = os.path.join(RAW, 'pdf', slug + '.pdf')
            os.replace(out, newout)
            out = newout
        res['file'] = os.path.relpath(out, ROOT) if os.path.exists(out) else None
        res['slug'] = slug
        res['retrieved'] = time.strftime('%Y-%m-%d')
        idx[u] = res
        print(res['status'], u, '->', res['file'], res['err'][:80], flush=True)
        time.sleep(0.5)
    json.dump(idx, open(idx_path, 'w'), indent=1)


if __name__ == '__main__':
    main()

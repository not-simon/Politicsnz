#!/usr/bin/env python3
"""Cached, rate-limit-friendly Wikipedia/Commons fetcher for Labour people profiles.
The MediaWiki API is heavily rate-limited (429) for this shared IP, so wikitext is read via
index.php?action=raw and lead images via the REST summary endpoint.
Usage: python3 tools/people_labour_wiki.py wikitext <Title> [...]
Caches to raw/people/labour/wiki/."""
import json, re, pathlib, sys, time, urllib.request, urllib.parse, hashlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / 'raw' / 'people' / 'labour' / 'wiki'
CACHE.mkdir(parents=True, exist_ok=True)
UA = 'PoliticsNZResearch/1.0 (personal research)'
API = 'https://en.wikipedia.org/w/api.php'


def get(url, binary=False, tries=8):
    delay = 3
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            data = urllib.request.urlopen(req, timeout=60).read()
            if not binary and data[:30].startswith(b'You are making too many'):
                raise IOError('ratelimited')
            time.sleep(0.5)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise IOError('404 ' + url)
            print('retry', i, url[:120], e, file=sys.stderr)
        except Exception as e:
            print('retry', i, url[:120], e, file=sys.stderr)
        time.sleep(delay); delay = min(delay * 2, 60)
    raise IOError('failed ' + url)


def _safe(t):
    return re.sub(r'[^A-Za-z0-9_.()-]', '_', t.replace(' ', '_'))


def api(params, base=API):
    params = dict(params, format='json', formatversion='2')
    q = urllib.parse.urlencode(sorted(params.items()))
    key = hashlib.sha1((base + q).encode()).hexdigest()[:16]
    f = CACHE / f'api_{key}.json'
    if f.exists():
        return json.loads(f.read_text())
    d = json.loads(get(base + '?' + q))
    f.write_text(json.dumps(d, ensure_ascii=False))
    return d


def raw(title, host='en.wikipedia.org'):
    """Wikitext via index.php?action=raw; follows redirects. Returns {'title','wikitext'}."""
    out = {'title': title, 'wikitext': ''}
    for _ in range(3):
        f = CACHE / (('c_' if 'commons' in host else 'wt_') + _safe(title) + '.json')
        if f.exists():
            out = json.loads(f.read_text())
        else:
            url = f'https://{host}/w/index.php?' + urllib.parse.urlencode({'title': title, 'action': 'raw'})
            try:
                txt = get(url, tries=5).decode('utf-8')
            except IOError:
                txt = ''
            out = {'title': title, 'wikitext': txt}
            f.write_text(json.dumps(out, ensure_ascii=False))
        m = re.match(r'#REDIRECT\s*\[\[([^\]#|]+)', out['wikitext'], re.I)
        if not m:
            return out
        title = m.group(1).strip()
    return out


wikitext = raw


def summary(title):
    f = CACHE / f'sum_{_safe(title)}.json'
    if f.exists():
        return json.loads(f.read_text())
    try:
        d = json.loads(get('https://en.wikipedia.org/api/rest_v1/page/summary/' +
                           urllib.parse.quote(title.replace(' ', '_'), safe=''), tries=5))
    except IOError:
        d = {}
    f.write_text(json.dumps(d, ensure_ascii=False))
    return d


if __name__ == '__main__':
    if sys.argv[1] == 'wikitext':
        for t in sys.argv[2:]:
            w = raw(t); print(w['title'], len(w['wikitext']))

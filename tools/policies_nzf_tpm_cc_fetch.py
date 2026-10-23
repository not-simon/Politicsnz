"""Fetch nzfirst.nz / maoriparty.org.nz pages from Common Crawl WARC records (latest HTTP-200 HTML capture per path
across raw/party-docs/<party>/cc/*.jsonl, from tools/policies_nzf_tpm_cc_index.py). Adapted from policies_green_cc_fetch.py.
Usage: python3 -I tools/policies_nzf_tpm_cc_fetch.py <party> [regex ...]
Saves raw/party-docs/<party>/cc_html/<path>.html (scripts/styles stripped) + cc_html/index.json"""
import sys, os, re, json, glob, gzip, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
party = sys.argv[1]
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'party-docs', party)
HTML = os.path.join(ROOT, 'cc_html'); os.makedirs(HTML, exist_ok=True)
idxf = os.path.join(HTML, 'index.json')
idx = json.load(open(idxf)) if os.path.exists(idxf) else {}
SKIP = re.compile(r'public_meeting|_meeting|style_guide|^test|_test|donat|renewal|signup|newsletter|join_|^tags/|video-|^isuru/')
caps = {}
for f in glob.glob(os.path.join(ROOT, 'cc', '*.jsonl')):
    for l in open(f):
        if not l.startswith('{'): continue
        x = json.loads(l)
        if x.get('status') != '200' or 'html' not in x.get('mime', ''): continue
        u = x['url']
        path = u.split('/', 3)[3] if u.count('/') >= 3 else ''
        q = '?' in path
        path = path.split('?')[0].split('#')[0].rstrip('/')
        if path in caps and (caps[path]['timestamp'] >= x['timestamp'] or (q and '?' not in caps[path]['url'])): continue
        caps[path] = x
pats = [re.compile(p) for p in sys.argv[2:]] or [re.compile('.')]
todo = [(p, x) for p, x in sorted(caps.items()) if any(r.search(p) for r in pats) and not SKIP.search(p)
        and not (p in idx and idx[p]['timestamp'] >= x['timestamp'])]
print(len(caps), 'paths;', len(todo), 'to fetch', flush=True)
def fetch(item):
    path, x = item
    off, ln = int(x['offset']), int(x['length'])
    for i in range(8):
        try:
            req = urllib.request.Request('https://data.commoncrawl.org/' + x['filename'], headers={'Range': f'bytes={off}-{off+ln-1}', 'User-Agent': 'PoliticsNZResearch/1.0'})
            data = gzip.decompress(urllib.request.urlopen(req, timeout=120).read()); break
        except Exception as e:
            time.sleep(2 + i)
    else:
        return path, None
    body = data.split(b'\r\n\r\n', 2)[2]
    sp = BeautifulSoup(body.decode('utf8', 'replace'), 'html.parser')
    for t in sp(['script', 'style', 'noscript', 'link', 'svg', 'iframe']): t.decompose()
    out = ('<!-- Common Crawl capture of %s at %s (WARC %s); scripts/styles removed -->\n' % (x['url'], x['timestamp'], x['filename'])) + str(sp)
    fn = re.sub(r'[^A-Za-z0-9_.-]', '_', path) or 'index'
    open(os.path.join(HTML, fn + '.html'), 'w').write(out)
    return path, {'file': fn + '.html', 'url': x['url'], 'timestamp': x['timestamp'], 'warc': x['filename'],
                  'offset': x['offset'], 'length': x['length']}
with ThreadPoolExecutor(8) as ex:
    for n, (path, meta) in enumerate(ex.map(fetch, todo)):
        if meta: idx[path] = meta
        else: print('FAIL', path, flush=True)
        if n % 50 == 0:
            json.dump(idx, open(idxf, 'w'), indent=1); print(n, flush=True)
json.dump(idx, open(idxf, 'w'), indent=1)
print('done', len(idx))

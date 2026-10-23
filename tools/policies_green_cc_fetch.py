"""Fetch greens.org.nz pages from Common Crawl WARC records (latest HTTP-200 capture across the CDX files saved by
policies_green_cc_index.py). Usage: python3 -I tools/policies_green_cc_fetch.py <regex-on-path> [...]
Saves raw/party-docs/green/html/<path>.html and appends metadata to raw/party-docs/green/html/index.json"""
import sys, os, re, json, glob, gzip, time, urllib.request
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'party-docs', 'green')
HTML = os.path.join(ROOT, 'html'); os.makedirs(HTML, exist_ok=True)
idxf = os.path.join(HTML, 'index.json')
idx = json.load(open(idxf)) if os.path.exists(idxf) else {}
caps = {}
for f in glob.glob(os.path.join(ROOT, 'cc', '*.jsonl')):
    for l in open(f):
        if not l.startswith('{'): continue
        x = json.loads(l)
        if x.get('status') != '200' or 'html' not in x.get('mime', ''): continue
        path = x['url'].split('www.greens.org.nz/', 1)[1].split('?')[0].split('#')[0].rstrip('/')
        if path in caps and caps[path]['timestamp'] >= x['timestamp']: continue
        if '?' in x['url'] and path in caps: continue
        caps[path] = x
pats = [re.compile(p) for p in sys.argv[1:]]
force = os.environ.get('FORCE')
for path, x in sorted(caps.items()):
    if not any(p.search(path) for p in pats): continue
    if path in idx and idx[path]['timestamp'] >= x['timestamp'] and not force: continue
    off, ln = int(x['offset']), int(x['length'])
    data = None
    for i in range(10):
        try:
            req = urllib.request.Request('https://data.commoncrawl.org/' + x['filename'], headers={'Range': f'bytes={off}-{off+ln-1}', 'User-Agent': 'PoliticsNZResearch/1.0'})
            data = gzip.decompress(urllib.request.urlopen(req, timeout=120).read()); break
        except Exception as e:
            print('retry', path, e, file=sys.stderr); time.sleep(2 + i)
    if data is None: print('FAIL', path); continue
    body = data.split(b'\r\n\r\n', 2)[2]  # skip WARC header + HTTP header
    if os.environ.get('MAIN_ONLY'):  # keep <title> + <main> only, to keep raw/ small
        from bs4 import BeautifulSoup
        sp = BeautifulSoup(body.decode('utf8', 'replace'), 'html.parser')
        mn = sp.find('main')
        if mn:
            for t in mn(['script', 'style', 'noscript', 'link']): t.decompose()
            body = ('<!-- trimmed to <main>; source %s CC %s -->\n<title>%s</title>\n%s' % (x['url'], x['timestamp'], sp.title.get_text() if sp.title else '', mn)).encode()
    fn = re.sub(r'[^A-Za-z0-9_.-]', '_', path) or 'index'
    open(os.path.join(HTML, fn + '.html'), 'wb').write(body)
    idx[path] = {'file': fn + '.html', 'url': x['url'], 'timestamp': x['timestamp'], 'warc': x['filename']}
    print('ok', path, x['timestamp'], len(body))
    json.dump(idx, open(idxf, 'w'), indent=1)

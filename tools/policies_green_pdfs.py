"""Download Green Party policy PDFs (assets.nationbuilder.com/beachheroes/...) listed in a file (one URL per line).
Saves to raw/party-docs/green/pdf/<basename>.pdf; writes raw/party-docs/green/pdf/manifest.json"""
import sys, os, json, time, urllib.request, urllib.parse, hashlib
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'party-docs', 'green', 'pdf')
os.makedirs(OUT, exist_ok=True)
mf = os.path.join(OUT, 'manifest.json')
man = json.load(open(mf)) if os.path.exists(mf) else {}
for url in [l.strip() for l in open(sys.argv[1]) if l.strip().startswith('http')]:
    if url in man and os.path.exists(os.path.join(OUT, man[url]['file'])): continue
    name = urllib.parse.unquote(urllib.parse.urlparse(url).path.rsplit('/', 1)[1])
    name = name.replace("'", '').replace(' ', '_')
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 PoliticsNZResearch/1.0'}), timeout=120) as r:
                data = r.read(); ct = r.headers.get('Content-Type'); break
        except Exception as e:
            print('retry', url, e); time.sleep(3); data = None
    if not data or not data[:5] == b'%PDF-':
        print('FAIL', url); man[url] = {'file': None, 'error': 'download failed or not a PDF'}; continue
    open(os.path.join(OUT, name), 'wb').write(data)
    man[url] = {'file': name, 'bytes': len(data), 'sha1': hashlib.sha1(data).hexdigest(), 'retrieved': time.strftime('%Y-%m-%d')}
    print('ok', name, len(data))
json.dump(man, open(mf, 'w'), indent=1, ensure_ascii=False)

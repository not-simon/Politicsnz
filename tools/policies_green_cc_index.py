"""Query Common Crawl CDX indexes for www.greens.org.nz captures (greens.org.nz itself is Cloudflare-blocked
and web.archive.org is unreachable through the proxy). Output: raw/party-docs/green/cc/<crawl>.jsonl"""
import json, sys, time, urllib.request, urllib.parse, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'raw', 'party-docs', 'green', 'cc')
CRAWLS = sys.argv[1:] or ['CC-MAIN-2026-43', 'CC-MAIN-2026-39', 'CC-MAIN-2026-34', 'CC-MAIN-2026-30']
def get(url, tries=12):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'PoliticsNZResearch/1.0'}), timeout=120) as r:
                return r.read().decode()
        except Exception as e:
            print('  retry', i, e, file=sys.stderr); time.sleep(3 + i * 2)
    raise SystemExit('failed ' + url)
for c in CRAWLS:
    base = f'https://index.commoncrawl.org/{c}-index?url=' + urllib.parse.quote('www.greens.org.nz/*') + '&output=json&fl=url,status,timestamp,filename,offset,length,mime'
    n = json.loads(get(base + '&showNumPages=true'))['pages']
    lines = []
    for p in range(n):
        t = get(base + f'&page={p}')
        lines += [l for l in t.splitlines() if l.startswith('{')]
    open(os.path.join(OUT, c + '.jsonl'), 'w').write('\n'.join(lines) + '\n')
    print(c, n, 'pages', len(lines), 'captures')

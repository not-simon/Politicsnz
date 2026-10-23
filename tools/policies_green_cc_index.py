"""Build a list of Common Crawl captures of www.greens.org.nz (the site is Cloudflare-blocked and web.archive.org is
unreachable via the proxy, but Common Crawl's WARC archive on data.commoncrawl.org works).
Uses the static cluster.idx + cdx-NNNNN.gz shards (the index.commoncrawl.org API is unreliable from here).
Usage: python3 -I tools/policies_green_cc_index.py CC-MAIN-2026-43 [...]  -> raw/party-docs/green/cc/<crawl>.jsonl"""
import json, sys, time, urllib.request, os, zlib
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'party-docs', 'green', 'cc')
os.makedirs(OUT, exist_ok=True)
KEY = 'nz,org,greens)/'
def get(url, rng=None, tries=10):
    for i in range(tries):
        try:
            h = {'User-Agent': 'PoliticsNZResearch/1.0'}
            if rng: h['Range'] = 'bytes=%d-%d' % rng
            return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=180).read()
        except Exception as e:
            print('  retry', i, e, file=sys.stderr); time.sleep(2 + i * 2)
    raise SystemExit('failed ' + url)
for c in sys.argv[1:]:
    base = f'https://data.commoncrawl.org/cc-index/collections/{c}/indexes/'
    lines = get(base + 'cluster.idx').decode().splitlines()
    sel = [i for i, l in enumerate(lines) if l.startswith(KEY)]
    if not sel:  # all captures inside one block: find the block whose start key precedes KEY
        sel = [max(i for i, l in enumerate(lines) if l.split('\t')[0] < KEY)]
    else:
        sel = [sel[0] - 1] + sel
    out = []
    for i in sel:
        k, shard, off, ln, _ = lines[i].split('\t')
        raw = get(base + shard, (int(off), int(off) + int(ln) - 1))
        for row in zlib.decompress(raw, 16 + zlib.MAX_WBITS).decode().splitlines():
            if not row.startswith(KEY): continue
            surt, ts, js = row.split(' ', 2)
            d = json.loads(js)
            out.append({'url': d['url'], 'status': d.get('status'), 'timestamp': ts, 'filename': d['filename'],
                        'offset': d['offset'], 'length': d['length'], 'mime': d.get('mime', ''), 'redirect': d.get('redirect')})
    open(os.path.join(OUT, c + '.jsonl'), 'w').write('\n'.join(json.dumps(x) for x in out) + '\n')
    print(c, len(sel), 'blocks', len(out), 'captures', flush=True)

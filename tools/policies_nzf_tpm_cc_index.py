"""List Common Crawl captures of www.nzfirst.nz / www.maoriparty.org.nz (both Cloudflare-blocked) using the static
cluster.idx + cdx shards on data.commoncrawl.org (adapted from tools/policies_green_cc_index.py).
Usage: python3 -I tools/policies_nzf_tpm_cc_index.py CC-MAIN-2026-43 [...] -> raw/party-docs/<party>/cc/<crawl>.jsonl"""
import json, sys, time, urllib.request, os, zlib
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'party-docs')
KEYS = {'nz-first': 'nz,nzfirst)/', 'te-pati-maori': 'nz,org,maoriparty)/'}
def get(url, rng=None, tries=8):
    for i in range(tries):
        try:
            h = {'User-Agent': 'PoliticsNZResearch/1.0'}
            if rng: h['Range'] = 'bytes=%d-%d' % rng
            return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=180).read()
        except Exception as e:
            if '404' in str(e): return None
            print('  retry', i, e, file=sys.stderr); time.sleep(2 + i * 2)
    return None
for c in sys.argv[1:]:
    base = f'https://data.commoncrawl.org/cc-index/collections/{c}/indexes/'
    ci = get(base + 'cluster.idx')
    if not ci: print(c, 'no index'); continue
    lines = ci.decode().splitlines()
    for party, KEY in KEYS.items():
        sel = [i for i, l in enumerate(lines) if l.startswith(KEY)]
        sel = ([sel[0] - 1] + sel) if sel else [max(i for i, l in enumerate(lines) if l.split('\t')[0] < KEY)]
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
        od = os.path.join(BASE, party, 'cc'); os.makedirs(od, exist_ok=True)
        open(os.path.join(od, c + '.jsonl'), 'w').write('\n'.join(json.dumps(x) for x in out) + '\n')
        print(c, party, len(out), 'captures', flush=True)

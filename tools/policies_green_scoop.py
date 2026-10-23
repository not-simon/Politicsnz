"""Mirror Green Party press releases from scoop.co.nz (greens.org.nz is Cloudflare-blocked).
Enumerates scoop story ids /stories/<SECTION><YYMM>/S00001.. (each redirects to its slug URL), fetches each,
keeps those whose 'Press Release:' source is the Green Party. Saves trimmed article HTML + index.json.
Usage: python3 -I tools/policies_green_scoop.py PA2610 PA2609 ..."""
import sys, os, re, json, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'party-docs', 'green', 'scoop')
os.makedirs(OUT, exist_ok=True)
idxf = os.path.join(OUT, 'index.json')
idx = json.load(open(idxf)) if os.path.exists(idxf) else {}
UA = {'User-Agent': 'Mozilla/5.0 PoliticsNZResearch/1.0'}
def fetch(u):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r:
                return r.geturl(), r.read().decode('utf8', 'replace')
        except urllib.error.HTTPError as e:
            if e.code == 404: return None, None
            time.sleep(2)
        except Exception:
            time.sleep(2)
    return None, None
def one(sec_id):
    sec, sid = sec_id
    key = f'{sec}/{sid}'
    if key in idx: return None
    url, html = fetch(f'https://www.scoop.co.nz/stories/{sec}/{sid}.htm')
    if not html: return None
    s = BeautifulSoup(html, 'html.parser')
    txt = s.get_text(' ', strip=True)
    m = re.search(r'Press Release:\s*([^|]{2,60}?)\s{1,3}(\d{1,2} [A-Z][a-z]+ 20\d\d|Green|$)', txt)
    if not re.search(r'Press Release:\s*(The\s+)?Green Party', txt): return (key, None)
    art = s.find(id='article') or s.find('article')
    title = s.title.get_text(strip=True).replace(' | Scoop News', '') if s.title else ''
    fn = sid + '_' + sec + '.html'
    open(os.path.join(OUT, fn), 'w').write('<!-- source %s -->\n<title>%s</title>\n%s' % (url, title, art))
    return (key, {'url': url, 'title': title, 'file': fn})
for sec in sys.argv[1:]:
    ids = [(sec, 'S%05d' % n) for n in range(1, 700)]
    miss = 0
    with ThreadPoolExecutor(8) as ex:
        for r in ex.map(one, ids):
            if r: idx[r[0]] = r[1]
    json.dump(idx, open(idxf, 'w'), indent=1, ensure_ascii=False)
    print(sec, sum(1 for k, v in idx.items() if k.startswith(sec) and v), 'Green releases', flush=True)

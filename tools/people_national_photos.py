#!/usr/bin/env python3
"""Download Wikipedia/Commons lead images (≤400px JPEG q82) for National people lacking photo.jpg.
Records source/credit/licence in raw/people/national/photos.json (merged into person.json by people_national_build.py)."""
import json, os, glob, sys, io, re, time
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people_national_wiki import fetch_bytes
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
RAW = os.path.join(ROOT, 'raw', 'people', 'national'); PEOPLE = os.path.join(ROOT, 'parties', 'national', 'people')
SKIP = set(sys.argv[1:])
log = os.path.join(RAW, 'photos.json'); meta = json.load(open(log)) if os.path.exists(log) else {}
def strip_html(s): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s or '')).strip()
for f in sorted(glob.glob(os.path.join(RAW, 'wiki', '*.json'))):
    w = json.load(open(f)); slug = w['slug']; ii = w.get('imageinfo')
    dest = os.path.join(PEOPLE, slug, 'photo.jpg')
    if slug in SKIP or not ii or os.path.exists(dest): continue
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        print('try', slug, flush=True)
        orig = ii['url'].split('?')[0]; m0 = re.match(r'https://upload\.wikimedia\.org/wikipedia/(\w+)/(\w)/(\w\w)/(.+)$', orig)
        data = None
        for wpx in (500, 330, 250, 120):
            if not m0: break
            u = f'https://thumb.wikimedia.org/wikipedia/{m0.group(1)}/thumb/{m0.group(2)}/{m0.group(3)}/{m0.group(4)}/{wpx}px-{m0.group(4)}'
            if m0.group(4).lower().endswith('.svg'): u += '.png'
            try:
                data = fetch_bytes(u); break
            except Exception as e:
                if '400' not in str(e) and '404' not in str(e): raise
        if data is None: raise RuntimeError('no thumb for ' + orig)
        im = Image.open(io.BytesIO(data))
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[-1]); im = bg
        im = im.convert('RGB'); im.thumbnail((400, 400)); im.save(dest, 'JPEG', quality=82)
    except Exception as e:
        print('fail', slug, e, flush=True); continue
    m = ii.get('extmetadata', {})
    meta[slug] = {'photo': 'photo.jpg', 'photo_source': ii.get('descriptionurl'),
                  'photo_credit': strip_html(m.get('Artist', {}).get('value')) + (' — ' + strip_html(m.get('Credit', {}).get('value')) if m.get('Credit') and strip_html(m.get('Credit', {}).get('value')) != strip_html(m.get('Artist', {}).get('value')) else ''),
                  'photo_license': strip_html(m.get('LicenseShortName', {}).get('value')),
                  'photo_license_url': m.get('LicenseUrl', {}).get('value')}
    json.dump(meta, open(log, 'w'), indent=1, ensure_ascii=False)
    print('ok', slug, flush=True); time.sleep(2)

#!/usr/bin/env python3
"""Fetch labour.org.nz candidate profile pages for never-MP 2026 candidates and extract the bio text.
Raw HTML -> raw/people/labour/labourorg/<slug>.html; text -> raw/people/labour/work/cand_bios.json.
Run with python3 -I (downloaded content is untrusted)."""
import json, os, re, subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT/'raw/people/labour/labourorg'; OUT.mkdir(parents=True, exist_ok=True)
roster = {e['slug'] for e in json.load(open(ROOT/'raw/people/labour/work/roster_final.json'))}
res = {}
for slug in sorted(os.listdir(ROOT/'parties/labour/people')):
    if slug in roster or slug == 'README.md':
        continue
    pj = json.load(open(ROOT/'parties/labour/people'/slug/'person.json'))
    url = (pj.get('questionnaire_2026') or {}).get('Website', '')
    if 'labour.org.nz' not in url:
        url = 'https://www.labour.org.nz/' + pj['name'].lower().replace(' ', '').replace("'", '').replace('-', '')
    f = OUT/f'{slug}.html'
    if not f.exists() or f.stat().st_size < 1000:
        subprocess.run(['curl', '-sS', '-L', '-m', '40', '-A', 'Mozilla/5.0', '-o', str(f), url])
    h = f.read_text(errors='ignore') if f.exists() else ''
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t); t = re.sub(r'&nbsp;|&#160;', ' ', t); t = re.sub(r'\s+', ' ', t)
    m = re.search(r'Meet (.*?)(Chip in|Support our movement)', t)
    bio = m.group(1) if m else ''
    res[slug] = {'name': pj['name'], 'url': url, 'bio': bio.strip()}
    print(slug, url, len(bio))
json.dump(res, open(ROOT/'raw/people/labour/work/cand_bios.json', 'w'), indent=1, ensure_ascii=False)

#!/usr/bin/env python3
"""Fetch National Party candidate biography pages (national.org.nz/team/<name>) for 2026 candidates without a
Wikipedia article. Saves raw HTML to raw/people/national/web/team/<slug>.html and extracted biography text to
raw/people/national/web/team/bios.json. Usage: python3 -I tools/people_national_team.py slug [slug...]"""
import json, os, re, sys, html, subprocess, time
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'raw', 'people', 'national', 'web', 'team')
PEOPLE = os.path.join(ROOT, 'parties', 'national', 'people')
os.makedirs(OUT, exist_ok=True)
bf = os.path.join(OUT, 'bios.json')
bios = json.load(open(bf)) if os.path.exists(bf) else {}
def text(h):
    h = re.sub(r'(?s)<script.*?</script>|<style.*?</style>', '', h)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()
for slug in sys.argv[1:]:
    p = json.load(open(os.path.join(PEOPLE, slug, 'person.json')))
    site = (p.get('questionnaire_2026') or {}).get('Website', '')
    urls = [site] if 'national.org.nz/team/' in site else []
    urls.append('https://www.national.org.nz/team/' + re.sub(r'[^a-z]', '', (p.get('first_name', '') + p.get('last_name', '')).lower()))
    urls.append('https://www.national.org.nz/team/' + slug)
    for u in dict.fromkeys(urls):
        fn = os.path.join(OUT, slug + '.html')
        code = subprocess.run(['curl', '-sS', '-m', '30', '-L', '-A', 'Mozilla/5.0 (PoliticsNZResearch)', '-o', fn, '-w', '%{http_code}', u],
                              capture_output=True, text=True).stdout
        time.sleep(1)
        if code == '200':
            t = text(open(fn, errors='replace').read())
            m = re.search(r'Biography (.*?)(?: Contact Get in Touch| Stay Updated|$)', t)
            bios[slug] = {'url': u, 'bio': m.group(1).strip() if m else '', 'retrieved': '2026-10-23'}
            print(slug, 'OK', u, len(bios[slug]['bio']))
            break
        else:
            if os.path.exists(fn): os.remove(fn)
    else:
        print(slug, 'NOT FOUND')
json.dump(bios, open(bf, 'w'), ensure_ascii=False, indent=1)

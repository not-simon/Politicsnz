"""Build parties/green/policies/documents/*.md (verbatim full text) from
  - raw/party-docs/green/pdf/*.pdf   (downloaded directly from assets.nationbuilder.com)
  - raw/party-docs/green/html/*.html (greens.org.nz pages recovered from Common Crawl WARC captures)
Writes documents/_catalog.json (slug -> metadata) used by policies_green_build.py.
Run: python3 -I tools/policies_green_build_docs.py
"""
import os, re, json, subprocess, unicodedata, urllib.parse
from bs4 import BeautifulSoup
import markdownify

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
RAW = os.path.join(BASE, 'raw', 'party-docs', 'green')
DOCS = os.path.join(BASE, 'parties', 'green', 'policies', 'documents')
os.makedirs(DOCS, exist_ok=True)
TODAY = '2026-10-23'

# HTML pages that are policy content (others captured, e.g. general news, are ignored)
POLICY_PAGE_RE = re.compile(r'^(manifesto_2026.*|manifesto_2020_climate_action_emissions_reduction|[a-z_]+_policy|policy|'
                            r'policy_announcements|nature_and_climate|people_and_communities|services_and_systems|'
                            r'te_tiriti_o_waitangi|affordable_food_for_all_of_us|connect_aotearoa|drink_swim_fish|'
                            r'power_for_all_of_us|tax_system_for_all|te_waonui_a_taane)$')
EXCLUDE = {'privacy_policy', 'greens_back_waitangi_tribunal_inquiry_into_climate_change_policy',
           'greens_stand_with_coromandel_locals_against_luxon_s_destructive_mining_policy'}
ANNOUNCE_FILE = os.path.join(BASE, 'tools', 'policies_green_announcements.txt')  # curated list of 2026 policy press releases


def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:90].rstrip('-')


def fm(d):
    out = ['---']
    for k, v in d.items():
        if v is None: continue
        out.append('%s: %s' % (k, json.dumps(v, ensure_ascii=False)))
    out.append('---\n')
    return '\n'.join(out)


BULLETS = {'●', '•', '○', '▪', '', '◦', '', '–', '■', '◆', '➢', '✓', ''}
NUMCELL = re.compile(r'^\(?-?\$?-?[\d,.]+[%m]?\)?$|^\$?-?[\d,.]+(bn|b|m)?$')


def clean_page(t):
    lines = t.split('\n')
    out, i = [], 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.strip() in BULLETS and ln.strip():
            j = i + 1
            while j < len(lines) and not lines[j].strip(): j += 1
            if j < len(lines):
                out.append('- ' + lines[j].strip()); i = j + 1; continue
        out.append(ln)
        i += 1
    s = '\n'.join(out)
    s = re.sub(r'\n{3,}', '\n\n', s).strip()
    return s


def table_like(layout_page):
    n = 0
    for ln in layout_page.split('\n'):
        cells = [c.strip() for c in re.split(r'\s{3,}', ln.strip()) if c.strip()]
        if len(cells) >= 3 and sum(bool(NUMCELL.match(c.replace(' ', ''))) for c in cells) >= 2: n += 1
    return n >= 3


def pdf_doc(path, url, meta):
    raw = subprocess.run(['pdftotext', '-enc', 'UTF-8', path, '-'], capture_output=True, text=True).stdout
    lay = subprocess.run(['pdftotext', '-enc', 'UTF-8', '-layout', path, '-'], capture_output=True, text=True).stdout
    info = subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout
    pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    title = (re.search(r'Title:\s+(.+)', info) or [None, None])[1]
    rp, lp = raw.split('\f'), lay.split('\f')
    tr = os.path.join(RAW, 'transcriptions', os.path.basename(path)[:-4] + '.txt')
    manual = os.path.exists(tr) and len(raw.strip()) < 50 * pages
    if manual:  # image-only PDF: use the manual transcription made from the rendered page images
        rp, lp = open(tr).read().split('\f'), []
    body, tables = [], 0
    for n in range(pages):
        t = clean_page(rp[n] if n < len(rp) else '')
        body.append('<!-- page %d -->\n\n%s' % (n + 1, t if t else '*(no extractable text on this page — image only)*'))
        if n < len(lp) and table_like(lp[n]):
            tables += 1
            body.append('<details><summary>Page %d with table layout preserved (pdftotext -layout)</summary>\n\n```text\n%s\n```\n\n</details>'
                        % (n + 1, lp[n].rstrip()))
    text = '\n\n'.join(body)
    if manual:
        text = ('> **Note:** this PDF consists of page images with no text layer, so pdftotext returns nothing. The text below was '
                'transcribed by hand from the rendered pages (pdftoppm, 110 dpi) on 2026-10-23, in page order; layout boxes are '
                'marked [Box:] and the two funding tables are rendered as Markdown tables. Check against the PDF for anything critical.\n\n' + text)
    return text, pages, title, tables


def html_main(path):
    s = BeautifulSoup(open(path, encoding='utf8', errors='replace').read(), 'html.parser')
    title = s.title.get_text(strip=True) if s.title else ''
    m = s.find('main') or s.body
    for t in m(['script', 'style', 'noscript', 'link', 'form', 'iframe', 'svg', 'img', 'button']): t.decompose()
    # drop "Related articles" block and everything after it
    for h in m.find_all(['h2', 'h3', 'h4']):
        if h.get_text(strip=True).lower() in ('related articles', 'related news'):
            for sib in list(h.find_all_next()): sib.decompose()
            h.decompose(); break
    md = markdownify.markdownify(str(m), heading_style='ATX', bullets='-')
    md = re.sub(r'\]\((/[^)]*)\)', lambda mm: '](https://www.greens.org.nz' + mm.group(1) + ')', md)
    md = '\n'.join(l.rstrip() for l in md.split('\n'))
    md = re.sub(r'^\s*<\s*$', '', md, flags=re.M)
    md = re.sub(r'\n{3,}', '\n\n', md).strip()
    posted = re.search(r'Posted at\s+([A-Z][a-z]+ \d{1,2}, \d{4})', md)
    return title, md, posted.group(1) if posted else None


# designed (non-template) PDFs: slug + title as printed on the cover
DESIGNED = {
    '2026_GREEN_PARTY_MANIFESTO.pdf': ('manifesto-2026-full-pdf', 'Green Party Manifesto 2026 — A Green government. For all of us. (full PDF)'),
    'Maori_Manifesto_Web_Version.pdf': ('maori-manifesto-2026-pdf', 'Green Party Māori Manifesto 2026 — Taiao, Tāngata, Tāhua, Rangatiratanga: Kei ō tātou ringa'),
    'Green_Party_Manifesto_EasyRead.pdf': ('manifesto-2026-easy-read-pdf', 'Green Party Manifesto 2026: A Green government. For all of us. (Easy Read)'),
    'GreensTaxPolicy2026.pdf': ('tax-policy-2026-a-tax-system-for-all-of-us', 'A tax system for all of us — Contributing fairly to society (Tax policy 2026)'),
    'DSF_Policy_2026.pdf': ('drink-swim-fish-policy-2026', 'Drink Swim Fish — Fixing the rules for fresh water and oceans'),
    'The_Greens_Full_Power_Policy.pdf': ('power-for-all-of-us-policy-2026', 'Power for all of us — Lower bills. Cleaner energy. Public ownership.'),
    'The_Greens_Kiwipower_explainer.pdf': ('kiwipower-explainer-2026', 'The Greens’ KiwiPower explainer'),
    'TWT_policy_2026_ONLINE.pdf': ('te-waonui-a-tane-policy-2026', 'Te Waonui a Tāne — Thriving Marae for Thriving Communities'),
    'a_job_for_every_young_person-policy.pdf': ('youth-jobs-guarantee-policy-2026', 'Youth Jobs Guarantee — A guaranteed job for every young person in Aotearoa'),
    'AI_policy_2026_WEBSITE.pdf': ('ai-policy-2026-safe-sovereign-ai', 'Safe, sovereign AI — An AI Plan for Aotearoa'),
    'Green_Party__Paid_Placements__Apprenticeships_for_our_future_workforce_2026.pdf': ('paid-placements-apprenticeships-policy-2026', 'Paid Placements & Apprenticeships — For our future workforce'),
    'Hauraki_Gulf___Tipaka_Moana_Marine_Protection.pdf': ('hauraki-gulf-restoration-of-high-protection-areas-bill-draft', 'Hauraki Gulf / Tīkapa Moana Marine Protection (Restoration of High Protection Areas) Amendment Bill (Green Party draft bill)'),
    'Budget_Print_MW_version_5-08-25_web.pdf': ('green-budget-2025', 'Green Budget 2025 (the Greens’ costed alternative Budget, 2025)'),
    'AFFORDABLE_FOOD_FOR_ALL_OF_US_POLICY_FINAL.pdf': ('affordable-food-for-all-of-us-policy-2026', 'Affordable food for all of us — Reforming the food system'),
}

CITED = set()  # greens.org.nz paths cited by policy.nz
for x in json.load(open(os.path.join(BASE, 'raw', 'policy.nz', 'parties', 'green-party.json')))['policies']:
    for c in x.get('citations') or []:
        m = re.search(r'greens\.org\.nz/([^?#]*)', c['url'])
        if m: CITED.add(m.group(1).rstrip('/'))

catalog = {}
# ---------- PDFs ----------
man = json.load(open(os.path.join(RAW, 'pdf', 'manifest.json')))
for url, v in man.items():
    if not v.get('file') or not os.path.exists(os.path.join(RAW, 'pdf', v['file'])):
        continue  # failed download, or deliberately removed (e.g. GE090 printable paper-train craft sheet, not policy)
    fn = v['file']
    stem = re.sub(r'^Policy-Greens_', '', fn[:-4])
    slug = slugify(stem)
    text, pages, ptitle, tables = pdf_doc(os.path.join(RAW, 'pdf', fn), url, v)
    first = next((l.strip() for l in text.split('\n') if l.strip() and not l.startswith('<!--')), stem)
    title = ptitle if ptitle and len(ptitle) > 4 and not ptitle.lower().startswith(('microsoft', 'untitled', 'canva')) else first
    if fn.startswith('Policy-Greens_'): title = re.sub(r'\s+\d+$', '', first) + ' (Green Party policy document)'
    if fn in DESIGNED: slug, title = DESIGNED[fn]
    ver = re.search(r'Version:\s*([0-9]{1,2} [A-Z][a-z]+ 20\d\d)', text)
    d = {'title': title, 'party': 'green', 'source_url': url, 'retrieved': v['retrieved'], 'format': 'pdf',
         'fetch_method': ('direct HTTPS download from ' + url.split('/')[2] + '; image-only PDF, text transcribed manually from page images'
                          if text.startswith('> **Note:** this PDF consists of page images') else
                          'direct HTTPS download from ' + url.split('/')[2] + '; text by pdftotext (poppler, default reading order, '
                          'lone bullet glyphs re-joined to their text); pages whose -layout output contains tables are repeated in layout form'),
         'pages': pages, 'policy_version': ver.group(1) if ver else None,
         'local_copy': 'raw/party-docs/green/pdf/' + fn if v['bytes'] < 10_000_000 else None, 'sha1': v['sha1']}
    open(os.path.join(DOCS, slug + '.md'), 'w').write(fm(d) + '# ' + title + '\n\n' + text + '\n')
    catalog[slug] = {**d, 'kind': 'pdf', 'chars': len(text), 'table_pages': tables}

# ---------- HTML (Common Crawl) ----------
idx = json.load(open(os.path.join(RAW, 'html', 'index.json')))
ann = set()
if os.path.exists(ANNOUNCE_FILE):
    ann = {l.split('#')[0].strip() for l in open(ANNOUNCE_FILE) if l.split('#')[0].strip()}
for p, v in sorted(idx.items()):
    if p in EXCLUDE or not (POLICY_PAGE_RE.match(p) or p in ann or p in CITED): continue
    title, md, posted = html_main(os.path.join(RAW, 'html', v['file']))
    title = re.sub(r'\s*-\s*Green Party of Aotearoa New Zealand$', '', title)
    if len(md) < 200: print('WARN short page', p, len(md))
    slug = 'web-' + slugify(p)
    ts = v['timestamp']
    d = {'title': title, 'party': 'green', 'source_url': v['url'], 'retrieved': TODAY, 'format': 'html',
         'fetch_method': 'greens.org.nz is Cloudflare-blocked (HTTP 403) and web.archive.org unreachable from this environment; '
                         'page recovered from the Common Crawl WARC capture of %s-%s-%s (%s); <main> content converted to Markdown'
                         % (ts[:4], ts[4:6], ts[6:8], v['warc'].split('/')[1]),
         'capture_date': '%s-%s-%s' % (ts[:4], ts[4:6], ts[6:8]), 'posted': posted}
    open(os.path.join(DOCS, slug + '.md'), 'w').write(fm(d) + md + '\n')
    catalog[slug] = {**d, 'kind': 'announcement' if p in ann else 'web', 'path': p, 'chars': len(md)}

# ---------- scoop.co.nz mirrors ----------
sidx = json.load(open(os.path.join(RAW, 'scoop', 'index.json')))
for key in sorted(a[6:] for a in ann if a.startswith('scoop:')):
    v = sidx[key]
    sp = BeautifulSoup(open(os.path.join(RAW, 'scoop', v['file']), encoding='utf8').read(), 'html.parser')
    art = sp.find(id='article')
    for t in art(['script', 'style', 'noscript', 'iframe', 'img']): t.decompose()
    for t in art.find_all('div', class_='article-left-box-wrapper'): t.decompose()
    from bs4 import Comment
    for c in art.find_all(string=lambda x: isinstance(x, Comment)): c.extract()
    for a in art.find_all('a', href=re.compile(r'scoop\.co\.nz/about/terms')):
        for sib in list(a.find_all_next()): sib.decompose()
        a.decompose()
    for t in art.find_all(string=True):  # Scoop hard-wraps text inside paragraphs: unwrap
        if '\n' in t: t.replace_with(re.sub(r'\s*\n\s*', ' ', t))
    md = markdownify.markdownify(str(art), heading_style='ATX', bullets='-')
    md = '\n'.join(l.strip() for l in md.split('\n'))
    md = re.sub(r'\n{3,}', '\n\n', md).strip()
    title = v['title'].strip()
    date = re.search(r'(\d{1,2} [A-Z][a-z]+ 20\d\d)', md)
    slug = 'scoop-' + slugify(title)
    d = {'title': title, 'party': 'green', 'source_url': v['url'], 'retrieved': TODAY, 'format': 'html',
         'fetch_method': 'Green Party press release as published on scoop.co.nz (mirror; original greens.org.nz page is Cloudflare-blocked '
                         'and not in Common Crawl); article body converted to Markdown, Scoop line-wrapping removed',
         'posted': date.group(1) if date else None}
    open(os.path.join(DOCS, slug + '.md'), 'w').write(fm(d) + md + '\n')
    catalog[slug] = {**d, 'kind': 'announcement', 'scoop_key': key, 'chars': len(md)}

# remove stale generated documents from earlier runs (only *.md files this script generates: pdf/web/scoop slugs)
for f in os.listdir(DOCS):
    if f.endswith('.md') and f[:-3] not in catalog and not f.startswith('unretrievable-'):
        os.remove(os.path.join(DOCS, f))

json.dump(catalog, open(os.path.join(DOCS, '_catalog.json'), 'w'), indent=1, ensure_ascii=False)
print(len(catalog), 'documents')

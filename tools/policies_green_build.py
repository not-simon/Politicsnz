"""Build parties/green/policies/policies.json and README.md.
Inputs: raw/policy.nz/parties/green-party.json (226 statements), documents/_catalog.json (from policies_green_build_docs.py),
tools/policies_green_archive_entries.json (hand-written neutral summaries), raw/party-docs/green/* (PDF manifest).
Run after policies_green_build_docs.py:  python3 -I tools/policies_green_build.py
"""
import os, re, json, collections, urllib.parse

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
POL = os.path.join(BASE, 'parties', 'green', 'policies')
DOCS = os.path.join(POL, 'documents')
RAW = os.path.join(BASE, 'raw', 'party-docs', 'green')
TODAY = '2026-10-23'

GROUPS = [  # policy.nz top-level topic groups (the ones that carry 'key-policies-*' tags)
    ('economy', 'Economy'), ('incomes-and-employment', 'Incomes and employment'), ('health', 'Health'),
    ('housing', 'Housing'), ('education', 'Education'), ('environment', 'Environment'),
    ('transport-and-infrastructure', 'Transport and infrastructure'), ('te-ao-maori', 'Te ao Māori'),
    ('community-and-inclusion', 'Community and inclusion'), ('law-justice-and-government', 'Law, justice and government'),
    ('migration', 'Migration'), ('media-culture-and-recreation', 'Media, culture and recreation'),
    ('defence-and-foreign-affairs', 'Defence and foreign affairs')]
GNAME = dict(GROUPS)

pnz = json.load(open(os.path.join(BASE, 'raw', 'policy.nz', 'parties', 'green-party.json')))
cat = json.load(open(os.path.join(DOCS, '_catalog.json')))
arch = json.load(open(os.path.join(BASE, 'tools', 'policies_green_archive_entries.json')))
man = json.load(open(os.path.join(RAW, 'pdf', 'manifest.json')))


def slugify(s):
    import unicodedata
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:90].rstrip('-')


# ---------------------------------------------------------------- unretrievable sources: explicit note documents
UNRETRIEVABLE = {
    'disability_policy_full': ('Disability Policy (full PDF, linked from greens.org.nz/disability_policy_full)',
        'https://www.greens.org.nz/disability_policy_full',
        'greens.org.nz is behind Cloudflare (HTTP 403 for all automated clients, incl. headless browser); web.archive.org is not '
        'reachable from this environment; no Common Crawl capture of this path exists (CC-MAIN-2026-30/34/39/43 checked). The PDF it '
        'points to (https://assets.nationbuilder.com/beachheroes/pages/64598/attachments/original/1779231111/Policy-Greens_Disability_Policy_2025-2026.pdf) '
        'returned HTTP 403 Forbidden on 2026-10-23 (5 attempts), i.e. it appears to have been withdrawn or replaced. The policy summary page '
        'greens.org.nz/disability_policy IS available (see web-disability-policy.md), and disability commitments appear in the 2026 manifesto '
        '(web-manifesto-2026-disability.md).'),
    'greens_announce_jobs_guarantee_for_young_people': ('Greens announce jobs guarantee for young people (press release, c. 11 Oct 2026)',
        'https://www.greens.org.nz/greens_announce_jobs_guarantee_for_young_people',
        'greens.org.nz is behind Cloudflare (HTTP 403); web.archive.org unreachable from this environment; not present in Common Crawl '
        '(latest crawl CC-MAIN-2026-43 ended 18 Oct 2026) and not found among Green Party releases on scoop.co.nz (PA2607-PA2610 and '
        'PO2607-PO2610 story ids enumerated). The policy document the release announced IS available in full: '
        'youth-jobs-guarantee-policy-2026.md.'),
}
for p, (title, url, reason) in UNRETRIEVABLE.items():
    slug = 'unretrievable-' + slugify(p)
    open(os.path.join(DOCS, slug + '.md'), 'w').write(
        '---\ntitle: %s\nparty: "green"\nsource_url: %s\nretrieved: null\nformat: "html"\nfetch_method: "not retrievable (Cloudflare 403)"\n---\n'
        '# %s\n\n**Full text not retrievable.**\n\nSource URL: <%s>\n\nReason: %s\n\nNo text is reproduced here, so nothing in this file '
        'should be read as the party\'s wording.\n' % (json.dumps(title, ensure_ascii=False), json.dumps(url), title, url, reason))
    cat[slug] = {'title': title, 'source_url': url, 'kind': 'unretrievable', 'chars': 0}

MIRROR = {  # greens.org.nz path -> scoop mirror document
    'greens_announce_plans_to_protect_the_hauraki_gulf': 'scoop-greens-announce-plans-to-protect-the-hauraki-gulf',
    'greens_will_regulate_ai_for_the_public_good': 'scoop-greens-will-regulate-ai-for-the-public-good',
}
url2slug = {}
for slug, v in cat.items():
    u = v.get('source_url', '')
    url2slug[u.split('?')[0]] = slug
for u, v in man.items():
    if v.get('file'):
        for slug, c in cat.items():
            if c.get('source_url') == u: url2slug[u.split('?')[0]] = slug


def resolve(url):
    """Return (original_url, archive_url_or_None, doc_slug_or_None, note)."""
    arch_url = None
    m = re.match(r'https?://web\.archive\.org/(?:web/\d+[a-z_]*|save)/(https?://.*)', url)
    if m:
        arch_url, url = url, m.group(1)
    base = url.split('?')[0]
    if base in url2slug: return url, arch_url, url2slug[base], None
    if base.replace('%27', "'") in url2slug: return url, arch_url, url2slug[base.replace('%27', "'")], None
    g = re.search(r'greens\.org\.nz/([^?#]*)', url)
    if g:
        p = g.group(1).rstrip('/')
        if 'web-' + slugify(p) in cat: return url, arch_url, 'web-' + slugify(p), None
        if p in MIRROR: return url, arch_url, MIRROR[p], 'greens.org.nz page not retrievable; same press release mirrored on scoop.co.nz'
        if 'unretrievable-' + slugify(p) in cat: return url, arch_url, 'unretrievable-' + slugify(p), 'not retrievable (Cloudflare 403)'
        return url, arch_url, None, 'not retrievable (Cloudflare 403)'
    if 'nationbuilder' in url:
        fn = urllib.parse.unquote(base.rsplit('/', 1)[1])
        for u2, v in man.items():
            if v.get('file') and urllib.parse.unquote(u2.split('?')[0]).endswith(fn): return url, arch_url, url2slug.get(u2.split('?')[0]), None
    if 'maoriparty.org.nz' in url or 'labour.org.nz' in url:
        return url, arch_url, None, ('cited by policy.nz but this is another party\'s web page, not a Green Party document; not archived here '
                                     '(maoriparty.org.nz is Cloudflare-blocked; the labour.org.nz page\'s article body is loaded by script and was not checked)')
    return url, arch_url, None, 'unmapped'


def doclink(slug, rel='documents/'):
    return '%s%s.md' % (rel, slug)


# ---------------------------------------------------------------- policy.nz entries
NOTES = {
    'POL54653': 'Discrepancy: policy.nz\'s "How" says the rate would be kept "at 33% for small and medium businesses"; the cited tax '
                'policy PDF says the corporate rate would be kept at 28 percent for small and medium enterprises and returned to 33 percent '
                'only for the biggest 0.7 percent of corporations (see document, page 3).',
    'POL54980': 'policy.nz also cites a Te Pāti Māori web page (maoriparty.org.nz/mana_motuhake) for this Green policy; that page is not a Green source.',
    'POL55038': 'policy.nz also cites a Labour Party release ("National moves the goalposts on jobs", 8 Oct 2026), which is not a Green source; the Green source is the manifesto Te Tiriti chapter.',
}
entries = []
unmapped = []
for x in pnz['policies']:
    attrs = {a['name'].strip().lower(): a['value'].strip() for a in x.get('attributes') or []}
    topics = list(dict.fromkeys(x.get('topics') or []))
    kp = next((t[len('key-policies-'):] for t in topics if t.startswith('key-policies-')), None)
    grp = kp if kp in GNAME else next((t for t in topics if t in GNAME), 'economy')
    srcs = []
    for c in x.get('citations') or []:
        url, aurl, slug, note = resolve(c['url'])
        if slug is None and note == 'unmapped': unmapped.append(c['url'])
        s = {'title': c.get('title', '').strip(), 'url': url}
        if aurl: s['archive_url'] = aurl
        s['document'] = doclink(slug) if slug else None
        if note: s['note'] = note
        srcs.append(s)
    e = {'id': x['reference'], 'statement': x['statement'].strip(), 'topics': topics, 'group': grp,
         'key_policy': any(t.startswith('key-policies-') for t in topics),
         'summary': {'why': attrs.get('why'), 'how': attrs.get('how')}, 'summary_source': 'policy.nz', 'sources': srcs}
    if x['reference'] in NOTES: e['notes'] = NOTES[x['reference']]
    entries.append(e)

# ---------------------------------------------------------------- manifesto 'Our plan' commitments (verbatim)
manifesto_items = collections.OrderedDict()
for slug in sorted(cat):
    m = re.match(r'web-manifesto-20(26|20)-(.+)$', slug)
    if not m or slug == 'web-manifesto-2026': continue
    chap = m.group(2)
    if m.group(1) == '20': chap = chap  # greens.org.nz/manifesto_2020_climate_action_emissions_reduction is the 2026 emissions chapter (URL typo by the party)
    body = open(os.path.join(DOCS, slug + '.md')).read().split('---\n', 2)[2]
    title = re.search(r'^# (.+)$', body, re.M).group(1).strip()
    lede = re.search(r'^### (.+)$', body, re.M)
    lede = lede.group(1).strip().strip('*') if lede else ''
    items = re.findall(r'^\d+\. (.+)$', body, re.M)
    group = arch['manifesto_chapter_group'].get(chap, 'economy')
    manifesto_items[slug] = {'title': title, 'lede': lede, 'group': group, 'items': items}
    for i, it in enumerate(items, 1):
        entries.append({'id': 'GRN-M26-%s-%02d' % (chap, i), 'statement': it.strip(), 'topics': [group], 'group': group, 'key_policy': False,
                        'summary': {'why': '%s — %s' % (title, lede), 'how': None},
                        'summary_source': 'archive (statement is the verbatim "Our plan" commitment from the Green Party Manifesto 2026)',
                        'manifesto_chapter': title,
                        'sources': [{'title': 'Green Party Manifesto 2026 — %s' % title, 'url': cat[slug]['source_url'], 'document': doclink(slug)},
                                    {'title': 'Green Party Manifesto 2026 (full PDF)', 'url': cat['manifesto-2026-full-pdf']['source_url'],
                                     'document': doclink('manifesto-2026-full-pdf')}]})

# ---------------------------------------------------------------- documents & announcements (archive summaries)
for slug, d in arch['documents'].items():
    entries.append({'id': 'GRN-DOC-' + slug, 'statement': d['statement'], 'topics': [d['group']], 'group': d['group'], 'key_policy': False,
                    'summary': {'why': None, 'how': d['summary']}, 'summary_source': 'archive',
                    'sources': [{'title': cat[slug]['title'], 'url': cat[slug]['source_url'], 'document': doclink(slug)}]})
for slug, g in arch['policy_pdfs_group'].items():
    web = None
    entries.append({'id': 'GRN-POLDOC-' + slug, 'statement': 'Standing policy: ' + re.sub(r' \(Green Party policy document\)$', '', cat[slug]['title']),
                    'topics': [g], 'group': g, 'key_policy': False,
                    'summary': {'why': None, 'how': arch['policy_pdfs_summary'][slug]}, 'summary_source': 'archive',
                    'policy_version': cat[slug].get('policy_version'),
                    'sources': [{'title': cat[slug]['title'], 'url': cat[slug]['source_url'], 'document': doclink(slug)}]})
for slug, d in arch['announcements'].items():
    entries.append({'id': 'GRN-ANN-' + slug, 'statement': d['statement'], 'topics': [d['group']], 'group': d['group'], 'key_policy': False,
                    'summary': {'why': None, 'how': d['summary']}, 'summary_source': 'archive', 'announced': cat[slug].get('posted'),
                    'sources': [{'title': cat[slug]['title'], 'url': cat[slug]['source_url'], 'document': doclink(slug)}]})

# sanity: every archive key exists
for k in list(arch['documents']) + list(arch['policy_pdfs_group']) + list(arch['announcements']):
    assert k in cat, k
assert set(arch['policy_pdfs_group']) == set(arch['policy_pdfs_summary'])

json.dump(entries, open(os.path.join(POL, 'policies.json'), 'w'), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- README
pz = [e for e in entries if e['summary_source'] == 'policy.nz']
mi = [e for e in entries if e['id'].startswith('GRN-M26')]
ndocs = len([k for k in cat if cat[k]['kind'] != 'unretrievable'])
L = []
A = L.append
A('# Green Party of Aotearoa New Zealand — every 2026 election policy\n')
A('*Compiled %s for the 7 November 2026 general election. Part of a non-partisan archive; every item links to its source and, '
  'wherever it could be retrieved, to the full verbatim text in [`documents/`](documents/).*\n' % TODAY)
A('## About this page\n')
A('- **%d policy statements from [policy.nz](https://policy.nz)** (the independent, non-partisan guide), each with its *Why* and *How* '
  'summary exactly as policy.nz wrote it, its topics and its citations. These are the core of this page.' % len(pz))
A('- **%d verbatim "Our plan" commitments** from the 38 chapters of the Green Party Manifesto 2026 (launched 26 July 2026), so that every '
  'manifesto commitment is listed even where policy.nz did not write it up. These are quoted exactly; they have no separate summary.' % len(mi))
A('- **%d further entries** for party policy documents and 2026 campaign announcements, with a short neutral summary written for this archive '
  '(marked `summary_source: "archive"` in [`policies.json`](policies.json)).' % (len(entries) - len(pz) - len(mi)))
A('- **%d full-text documents** in [`documents/`](documents/): %d PDFs (manifesto, Māori manifesto, Easy Read manifesto, %d standing policy '
  'papers, 2026 campaign policy papers, Green Budget 2025), %d greens.org.nz pages and %d press releases mirrored on Scoop.\n' % (
      ndocs, sum(1 for v in cat.values() if v['kind'] == 'pdf'), len(arch['policy_pdfs_group']),
      sum(1 for v in cat.values() if v['kind'] == 'web' or (v['kind'] == 'announcement' and 'path' in v)),
      sum(1 for v in cat.values() if 'scoop_key' in v)))
A('**How the text was obtained.** greens.org.nz is behind Cloudflare and refuses automated access (HTTP 403), and the Internet Archive '
  '(web.archive.org) could not be reached from the research environment. So:')
A('1. **PDFs** were downloaded directly from the party\'s file host `assets.nationbuilder.com/beachheroes/…` (and two from `img.scoop.co.nz`) and '
  'converted with `pdftotext`. Reading order was checked; the default (non-layout) mode was cleaner for the multi-column brochures, and pages that '
  'contain tables are additionally reproduced in `-layout` form so that table rows stay intact. One image-only PDF (the KiwiPower explainer) was '
  'transcribed by hand and is marked as such. Local copies are in `raw/party-docs/green/pdf/`.')
A('2. **greens.org.nz web pages** (manifesto chapters, policy summary pages, press releases) were recovered from **Common Crawl** WARC '
  'captures (crawls CC-MAIN-2026-30, -34, -39 and -43, i.e. July to 18 October 2026); each document records its capture date.')
A('3. **Press releases not captured by Common Crawl** were taken from the copies the party posted on **scoop.co.nz**.')
A('4. Nothing was paraphrased inside a full-text document. Where a source could not be retrieved the document says so.\n')
A('**Not retrievable:**')
A('- `greens.org.nz/disability_policy_full`. The Disability Policy PDF it points to now returns HTTP 403, so it appears to have been withdrawn. '
  'The disability policy summary page and the manifesto disability chapter are included. See [note](documents/unretrievable-disability-policy-full.md).')
A('- `greens.org.nz/greens_announce_jobs_guarantee_for_young_people` (about 11 Oct 2026). The policy paper it announced is included in full. '
  'See [note](documents/unretrievable-greens-announce-jobs-guarantee-for-young-people.md).')
A('- The **fiscal plan released on 23 October 2026** (the day this page was compiled). It is not yet in any crawl or mirror reachable from here. '
  'The section below summarises press coverage of it.')
A('- policy.nz also cites two pages from other parties for Green policies (POL54980, POL55038). They are flagged on those entries.\n')
if unmapped:
    A('Unmapped citations: ' + ', '.join(unmapped) + '\n')

# headline
A('## Headline commitments\n')
A('policy.nz marks these as the Greens\' **key policies**:\n')
for e in pz:
    if e['key_policy']:
        A('- **%s** (%s). [%s](#%s)' % (e['statement'], GNAME[e['group']], e['id'], e['id'].lower()))
A('\nThe party\'s campaign is built around three priorities: "affordable living, healthy nature and real democracy". It is to be paid for by taxing '
  '"the super-rich and mega-corporations" while cutting income tax "for 96 percent of people" ([manifesto introduction](documents/web-manifesto-2026.md)). '
  'The main policy packages released during 2026 were:\n')
for slug in ['tax-policy-2026-a-tax-system-for-all-of-us', 'drink-swim-fish-policy-2026', 'power-for-all-of-us-policy-2026',
             'te-waonui-a-tane-policy-2026', 'affordable-food-for-all-of-us-policy-2026', 'ai-policy-2026-safe-sovereign-ai',
             'youth-jobs-guarantee-policy-2026', 'paid-placements-apprenticeships-policy-2026']:
    A('- **%s**: %s [full text](documents/%s.md)' % (arch['documents'][slug]['statement'], arch['documents'][slug]['summary'], slug))
A('- **Connect: Aotearoa transport plan**: %s [full text](documents/web-green-party-launches-the-transport-plan-to-combat-fossil-fuel-crisis.md), '
  '[policy page](documents/web-connect-aotearoa.md)' % arch['announcements']['web-green-party-launches-the-transport-plan-to-combat-fossil-fuel-crisis']['summary'])
A('')

# fiscal
A('## Costed plan and fiscal position\n')
A('**Tax plan revenue.** The table below gives the party\'s own estimates from *A tax system for all of us* (page 10). Figures are $ million per year; '
  'negative figures are revenue forgone. The document says the estimates come from Parliamentary Library models, with an allowance for avoidance '
  'and evasion of the super-rich tax.\n')
A('| Policy | 2027/28 | 2028/29 | 2029/30 | 2030/31 |\n|---|---:|---:|---:|---:|')
for row in [('Super-rich tax', '3,762', '3,883', '4,008', '4,137'), ('Capital Acquisitions Tax', '953', '1,001', '1,051', '1,103'),
            ('Big corporations tax', '1,370', '1,436', '1,502', '1,570'), ('Major banks levy', '373', '388', '404', '420'),
            ('Big tech tax', '204', '214', '223', '233'), ('Reversing bright-line test changes', '45', '45', '45', '45'),
            ('Reversing landlord tax cuts', '876', '922', '970', '1,003'), ('Tax setting changes (income tax cuts)', '-2,335', '-2,439', '-2,557', '-2,680'),
            ('Funding for Inland Revenue', '-100', '-102', '-104', '-106'), ('**Total**', '**5,147**', '**5,348**', '**5,541**', '**5,725**')]:
    A('| %s | %s | %s | %s | %s |' % row)
A('\nSource: [tax policy, full text](documents/tax-policy-2026-a-tax-system-for-all-of-us.md) (the table is reproduced in layout form on page 10).\n')
A('**Fiscal plan (23 October 2026).** The party released its overall fiscal plan at Parliament on 23 October 2026. The document itself could not '
  'be retrieved here. According to [RNZ\'s report](https://www.rnz.co.nz/news/politics_election-2026/2097318/green-party-releases-fiscal-plan-promises-to-increase-health-spending-by-3-billion-each-year) '
  '(Russell Palmer, 23 Oct 2026), the plan:')
A('- adds $3 billion to health funding in each of the next four Budgets, about $30 billion over the period;')
A('- relies on "nearly $29 billion in extra revenue over four years" from the wealth tax, the tax on large gifts and inheritances, higher company tax for big '
  'businesses, a bank levy and landlord tax changes, alongside income tax cuts for most workers;')
A('- raises future operating allowances to $4.5b–$4.7b a year, compared with about $2.4b under the coalition\'s plans;')
A('- returns to surplus in 2029/30, a year later than Treasury forecasts, and leaves debt $26.6 billion higher than Treasury expects by 2030/31;')
A('- commits future Budget funding to buying overseas carbon credits. Treasury estimated that bill could reach $5 billion; the Greens say more domestic cuts would reduce it.')
A('Infometrics reviewed the plan\'s direct fiscal effects. Swarbrick said every election policy had been costed, and that the party still wants a '
  'Parliamentary Budget Office. National (Simeon Brown) and ACT (David Seymour) criticised the plan; their reactions are in the same RNZ report. '
  'Other outlets\' coverage gave a debt figure of 44% of GDP by 2030/31 against Treasury\'s 39.5%. That figure has not been verified against the party document.\n')
A('**Costings in individual policy papers.** Most 2026 policy papers end with four-year cost tables (2027/28–2030/31). These include '
  '[Power for all of us](documents/power-for-all-of-us-policy-2026.md), [KiwiPower](documents/kiwipower-explainer-2026.md), '
  '[Te Waonui a Tāne](documents/te-waonui-a-tane-policy-2026.md), [Affordable food](documents/affordable-food-for-all-of-us-policy-2026.md), '
  '[Youth Jobs Guarantee](documents/youth-jobs-guarantee-policy-2026.md) and [Paid placements & apprenticeships](documents/paid-placements-apprenticeships-policy-2026.md). '
  'Release-level costings include pay equity for care workers (about $1.1bn a year), cancelling public-service cuts ($3.17bn over four years) and '
  'te reo Māori ($200m). The party\'s 2025 alternative budget, [Green Budget 2025](documents/green-budget-2025.md), includes a full fiscal summary.\n')

# library
A('## Policy documents library\n')
A('Every document collected, with its full text. **Pages** is the PDF page count; for web pages it shows the capture or posting date.\n')
A('| Document | Type | Pages / date | Version | Full text | Original |\n|---|---|---|---|---|---|')
order = {'pdf': 0, 'web': 1, 'announcement': 2, 'unretrievable': 3}
for slug, v in sorted(cat.items(), key=lambda kv: (order[kv[1]['kind']], kv[1]['title'].lower())):
    if v['kind'] == 'pdf':
        typ, pg = 'PDF', str(v['pages'])
    elif v['kind'] == 'unretrievable':
        typ, pg = 'not retrievable', '—'
    else:
        typ = 'press release' if v['kind'] == 'announcement' else 'web page'
        pg = v.get('posted') or ('captured ' + v.get('capture_date', '')) if v.get('posted') or v.get('capture_date') else '—'
    A('| %s | %s | %s | %s | [%s.md](documents/%s.md) | [link](%s) |' % (
        v['title'].replace('|', '/'), typ, pg, v.get('policy_version') or '', slug, slug, v['source_url']))
A('')

# TOC
by = collections.defaultdict(list)
for e in entries: by[e['group']].append(e)
A('## Contents by topic\n')
for g, name in GROUPS:
    n_p = sum(1 for e in by[g] if e['summary_source'] == 'policy.nz')
    n_m = sum(1 for e in by[g] if e['id'].startswith('GRN-M26'))
    A('- [%s](#%s): %d policy.nz statements, %d manifesto commitments, %d documents/announcements' % (
        name, slugify(name), n_p, n_m, len(by[g]) - n_p - n_m))
A('\nTopics follow policy.nz\'s top-level groups. Each policy.nz statement appears once: under the group policy.nz flagged it as a key policy for, otherwise under the first top-level group it is tagged with; '
  'all of its topics are listed with it.\n')

def src_md(e):
    out = []
    for s in e['sources']:
        t = s['title'] or s['url']
        if s.get('document'):
            out.append('[%s](%s) ([original](%s))' % (t, s['document'], s['url']))
        else:
            out.append('%s (<%s>), %s' % (t, s['url'], s.get('note', 'no document')))
    return '; '.join(out)

for g, name in GROUPS:
    A('## %s\n' % name)
    ps = [e for e in by[g] if e['summary_source'] == 'policy.nz']
    if ps:
        A('### Policies (policy.nz)\n')
        for e in ps:
            A('<a id="%s"></a>' % e['id'].lower())
            A('**%s**%s  ' % (e['statement'], ' ⭐ key policy' if e['key_policy'] else ''))
            A('`%s` · topics: %s\n' % (e['id'], ', '.join(e['topics'])))
            if e['summary']['why']: A('- **Why:** %s' % e['summary']['why'])
            if e['summary']['how']: A('- **How:** %s' % e['summary']['how'])
            A('- **Full text:** %s' % src_md(e))
            if e.get('notes'): A('- **Note:** %s' % e['notes'])
            A('')
    chs = [(s, c) for s, c in manifesto_items.items() if c['group'] == g]
    if chs:
        A('### Manifesto 2026 commitments (verbatim)\n')
        for s, c in chs:
            A('**%s**: *%s* ([full chapter](documents/%s.md))\n' % (c['title'], c['lede'], s))
            for i, it in enumerate(c['items'], 1):
                A('%d. %s' % (i, it))
            A('')
    others = [e for e in by[g] if e['summary_source'] == 'archive']
    if others:
        A('### Policy documents and 2026 announcements\n')
        for e in others:
            date = (' (%s)' % e['announced']) if e.get('announced') else ''
            A('- **%s**%s: %s Full text: %s' % (e['statement'], date, e['summary']['how'], src_md(e)))
        A('')

A('---\n*Built by `tools/policies_green_build_docs.py` and `tools/policies_green_build.py` from policy.nz data, party PDFs, Common Crawl and Scoop. '
  'Raw downloads are in `raw/party-docs/green/`.*')
open(os.path.join(POL, 'README.md'), 'w').write('\n'.join(L) + '\n')
print(len(entries), 'entries;', len(pz), 'policy.nz;', len(mi), 'manifesto items; unmapped', len(unmapped))

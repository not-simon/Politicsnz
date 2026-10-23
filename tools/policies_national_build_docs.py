#!/usr/bin/env python3
"""Build parties/national/policies/documents/*.md (verbatim full text) from raw/party-docs/national/.
Run after tools/policies_national_fetch.py.  python3 -I tools/policies_national_build_docs.py
Writes documents + raw/party-docs/national/doc_index.json (url -> doc path, title, ...).
"""
import json, os, re, sys, hashlib, subprocess, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from policies_national_extract import national_main, beehive_main, rnz_main, to_md
from policies_national_fetch import orig, key_for, policynz_urls

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'raw', 'party-docs', 'national')
DOCS = os.path.join(ROOT, 'parties', 'national', 'policies', 'documents')
os.makedirs(DOCS, exist_ok=True)
RETRIEVED = '2026-10-23'
log = json.load(open(os.path.join(RAW, 'fetch_log.json')))

# Replacement for a policy.nz-cited URL that now 404s (same release, re-slugged by National).
SUBSTITUTE = {'https://www.national.org.nz/news/260831-nicolawillis': 'https://www.national.org.nz/news/260830-nicolawillis'}
PLAYWRIGHT = {'https://www.beehive.govt.nz/release/active-investor-plus-delivers-3-billion-investment-new-zealand',
              'https://www.beehive.govt.nz/release/unlocking-economic-potential-high-country-farms'}

# Campaign-period National Party policy announcements (news releases) not cited by policy.nz,
# selected by reading the June-Oct 2026 news index (see report). Government (Beehive-style) releases are excluded.
EXTRA_NEWS = '''20260625-brownbishopwatts 20260705-hontoddmcclay 20260715-honchrispenk 20260719-honpaulgoldsmith
20260621-rthonchristopherluxon 260621-national-to-further-boost-kiwis-financia 260608-national-backs-farmers---qeii-national-t
260927-christopherluxon-1 260927-christopherluxon 260928-nicolawillis 261005-chrisbishop
261006-simeonbrown 261007-cameronbrewer 261012-nicolawillis 261015-simeonbrown-1 20261019-chrisbishop
20261021-christopherluxon 20261022-retirement 20261023-young-adults 261009-toddmcclay-1'''.split()

# PDFs linked from included pages that are NOT National election-policy documents (newsletters, govt report cards,
# attack documents about other parties, government consultation material) - excluded.
PDF_EXCLUDE = re.compile(r'Newsletter|newsletter|Report Card|Labour|Development levies|Public Consultation|Realm Leaders|Phillips Inquiry')


def slugify(s):
    s = s.replace('’', '').replace("'", '').replace('%27', '')
    s = re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()
    return s[:90]


def doc_slug(url):
    p = urllib.parse.urlparse(url)
    if p.path.lower().endswith('.pdf'):
        n = urllib.parse.unquote(os.path.basename(p.path))[:-4]
        n = re.sub(r'-1$', '', n)
        return 'pdf-' + slugify(n)
    host = p.netloc.replace('www.', '')
    parts = [x for x in p.path.split('/') if x]
    if host == 'national.org.nz':
        if not parts:
            return 'web-home'
        if parts[0] == 'policies':
            return 'policy-' + slugify(parts[1]) if len(parts) > 1 else 'policy-index'
        if parts[0] == 'news':
            return 'news-' + slugify(parts[1])
        return 'web-' + slugify('-'.join(parts))
    if host == 'beehive.govt.nz':
        return 'beehive-' + slugify(parts[-1])
    if host == 'rnz.co.nz':
        return 'rnz-' + slugify(parts[-1])
    return slugify(host + '-' + '-'.join(parts))


def fm(d):
    out = ['---']
    for k, v in d.items():
        if isinstance(v, list):
            out.append(f'{k}:')
            out += [f'  - {json.dumps(x, ensure_ascii=False)}' for x in v]
        else:
            out.append(f'{k}: {json.dumps(v, ensure_ascii=False)}')
    out.append('---')
    return '\n'.join(out)


def pdf_text(path, layout=False):
    args = ['pdftotext', '-enc', 'UTF-8'] + (['-layout'] if layout else []) + [path, '-']
    t = subprocess.run(args, capture_output=True, text=True).stdout
    t = t.replace('\f', '\n\n')
    t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()


def pdf_links_in(path):
    t = open(path, errors='replace').read()
    return sorted(set(re.findall(r'https://assets\.national\.org\.nz/web/prod/[^"\\\s<>&]+?\.pdf(?:\?v=\d+)?', t)))


index = {}
seen_md5 = {}


def write_pdf_doc(url, cited_title=None):
    info = log.get(url)
    if not info or info['status'] != 200:
        return write_failed(url, f"HTTP {info['status'] if info else 'not fetched'} {info.get('err','') if info else ''}", 'pdf', cited_title)
    path = os.path.join(ROOT, info['file'])
    md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
    slug = doc_slug(url)
    if md5 in seen_md5:                      # identical file under another name / version -> same doc
        index[url] = dict(index[seen_md5[md5]])
        d = index[url]; d.setdefault('alt_urls', [])
        return d
    seen_md5[md5] = url
    pages = subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout
    pages = int(re.search(r'Pages:\s+(\d+)', pages).group(1)) if 'Pages' in pages else None
    title = urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(url).path))[:-4]
    title = re.sub(r'-1$', '', title)
    body = pdf_text(path); lay = pdf_text(path, True)
    size = os.path.getsize(path)
    front = fm({'title': title, 'party': 'national', 'source_url': url, 'retrieved': RETRIEVED, 'format': 'pdf',
                'fetch_method': 'curl (direct from assets.national.org.nz); text via pdftotext (poppler)',
                'pages': pages, 'local_copy': info['file'] if size < 10_000_000 else None, 'md5': md5})
    md = f"""{front}

# {title}

Published by the New Zealand National Party as a PDF policy document. Source: <{url}>.
The text below is the verbatim text layer of the PDF extracted with `pdftotext` (reading order). Line breaks follow the
PDF; tables and multi-column layouts may read out of order in this section, so a second rendering that preserves the
page layout (`pdftotext -layout`) follows it. Nothing has been added, removed or paraphrased.

## Full text (reading order)

{body}

## Full text (page-layout rendering)

```text
{lay}
```
"""
    if not body.strip():
        md += '\n> NOTE: the PDF has no extractable text layer (image-only); text could not be extracted.\n'
    open(os.path.join(DOCS, slug + '.md'), 'w').write(md)
    index[url] = {'doc': f'documents/{slug}.md', 'title': title, 'kind': 'pdf', 'chars': len(body)}
    return index[url]


def write_failed(url, reason, kind, title=None):
    slug = doc_slug(url)
    front = fm({'title': title or url, 'party': 'national', 'source_url': url, 'retrieved': RETRIEVED,
                'format': kind, 'fetch_method': 'curl', 'status': 'not-retrievable'})
    md = f"{front}\n\n# {title or url}\n\n**Source not retrievable.** {url} could not be fetched on {RETRIEVED}: {reason}.\nNo text is reproduced here.\n"
    open(os.path.join(DOCS, slug + '.md'), 'w').write(md)
    index[url] = {'doc': f'documents/{slug}.md', 'title': title or url, 'kind': kind, 'chars': 0, 'failed': reason}
    return index[url]


def write_html_doc(url, cited_title=None, note=None):
    fetch_url = SUBSTITUTE.get(url, url)
    info = log.get(fetch_url)
    if not info or info['status'] != 200:
        return write_failed(url, f"HTTP {info['status'] if info else 'not fetched'}", 'html', cited_title)
    path = os.path.join(ROOT, info['file'])
    host = urllib.parse.urlparse(fetch_url).netloc
    if 'beehive' in host:
        title, bl = beehive_main(path); publisher = 'New Zealand Government (beehive.govt.nz)'
    elif 'rnz' in host:
        title, bl = rnz_main(path); publisher = 'RNZ (news report, third-party)'
        # drop RNZ page furniture before the headline
        i = next((k for k, (tag, _) in enumerate(bl) if tag in ('h1', 'h2')), 0)
        bl = [b for b in bl[i:] if not b[1].startswith(('Video player removed', 'https://players.brightcove'))]
    else:
        title, bl = national_main(path); publisher = 'New Zealand National Party (national.org.nz)'
        title = re.sub(r'\s*\|\s*National Party$', '', title)
        h1 = next((t for tag, t in bl if tag == 'h1'), None)
        title = h1 or title
    body = to_md(bl)
    pdfs = [u for u in pdf_links_in(path) if not PDF_EXCLUDE.search(urllib.parse.unquote(u))] if 'national.org.nz' in host else []
    slug = doc_slug(url)
    meta = {'title': title, 'party': 'national', 'source_url': fetch_url, 'retrieved': RETRIEVED, 'format': 'html',
            'fetch_method': ('headless Chromium (tools/fetch_page.js)' if fetch_url in PLAYWRIGHT else 'curl') +
                            '; main content extracted with BeautifulSoup (tools/policies_national_extract.py)',
            'publisher': publisher, 'local_copy': info['file']}
    if fetch_url != url:
        meta['cited_url'] = url
    md = fm(meta) + f"\n\n# {title}\n\n"
    if note:
        md += note + '\n\n'
    if fetch_url != url:
        md += f"> The URL cited by policy.nz ({url}) now returns HTTP 404; National re-published the same release at {fetch_url}, which is reproduced here.\n\n"
    md += f"Source: <{fetch_url}> ({publisher}). Main article/policy content only; site navigation, footer and 'More policies/Latest news' lists removed. Text is verbatim.\n\n## Full text\n\n{body}\n"
    index[url] = {'doc': f'documents/{slug}.md', 'title': title, 'kind': 'html', 'chars': len(body), 'pdfs': pdfs}
    if pdfs:
        links = []
        for pu in pdfs:
            d = write_pdf_doc(pu) if pu not in index else index[pu]
            links.append(f"- [{d['title']}]({d['doc'].replace('documents/', '')}) — <{pu}>")
        md += '\n## Linked policy documents (PDF)\n\n' + '\n'.join(links) + '\n'
        index[url]['linked_docs'] = [index[pu]['doc'] for pu in pdfs]
    open(os.path.join(DOCS, slug + '.md'), 'w').write(md)
    return index[url]


def main():
    d = json.load(open(os.path.join(ROOT, 'raw/policy.nz/parties/national-party.json')))
    cited_titles = {}
    for p in d['policies']:
        for c in p['citations']:
            cited_titles.setdefault(orig(c['url']), c['title'])
    urls = []
    for u in policynz_urls():
        urls.append(u)
    hub = sorted({u for u in log if re.match(r'https://www\.national\.org\.nz/(policies(/.*)?|plan)$', u)})
    urls += [u for u in hub if u not in urls]
    urls += ['https://www.national.org.nz/news/' + s for s in EXTRA_NEWS if 'https://www.national.org.nz/news/' + s not in urls]
    for u in urls:
        if u.lower().split('?')[0].endswith('.pdf'):
            if u not in index:
                write_pdf_doc(u, cited_titles.get(u))
        else:
            write_html_doc(u, cited_titles.get(u))
    json.dump(index, open(os.path.join(RAW, 'doc_index.json'), 'w'), indent=1, ensure_ascii=False)
    docs = {v['doc'] for v in index.values()}
    print(len(index), 'urls ->', len(docs), 'documents;', sum(1 for v in index.values() if v.get('failed')), 'failed')
    for u, v in index.items():
        if v['chars'] < 400:
            print('SHORT', v['chars'], u)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Convert fetched Labour policy sources (raw/party-docs/labour) into parties/labour/policies/documents/<slug>.md.

Main-content only, verbatim text; only whitespace/markup is normalised (headings -> #, lists -> -, tables -> |).
Usage: python3 -I tools/policies_labour_extract.py
"""
import json, os, re, subprocess
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'raw', 'party-docs', 'labour')
OUT = os.path.join(ROOT, 'parties', 'labour', 'policies', 'documents')

BLOCK = {'td', 'th', 'p', 'div', 'section', 'article', 'header', 'footer', 'main', 'aside', 'ul', 'ol', 'li', 'table', 'thead', 'tbody',
         'tr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'figure', 'figcaption', 'dl', 'dt', 'dd', 'details',
         'summary', 'br', 'hr', 'form', 'nav', 'button'}


PDF_TITLES = {
    'https://www.labour.org.nz/media/dbskvb1y/backinglocaldoctors.pdf': 'Labour: Backing local doctors (Family Doctor Loan Scheme) - PDF',
    'https://www.labour.org.nz/media/pfvguai5/labour-cgt.pdf': 'Labour: Capital gains tax - PDF',
    'https://www.labour.org.nz/media/prhel1zq/cervical-screening-factsheet.pdf': 'Labour: Free cervical screening factsheet - PDF',
    'https://www.labour.org.nz/media/vbyf0pxe/the-new-zealand-future-fund.pdf': 'Labour: The New Zealand Future Fund - PDF',
    'https://www.labour.org.nz/media/vtbneplb/labour-free-doctors-visits.pdf': 'Labour: Free doctor\'s visits (Medicard) - PDF',
    'https://img.scoop.co.nz/media/pdfs/2610/Factsheet__School_Costs.pdf': 'Labour factsheet: School costs (PDF attached to Scoop release)',
}


def norm(t):
    return re.sub(r'\s+', ' ', t.replace('\xa0', ' ')).strip()


class MD:
    def __init__(self):
        self.lines, self.buf = [], ''

    def flush(self, prefix=''):
        t = norm(self.buf)
        if t:
            self.lines.append(prefix + t)
        self.buf = ''

    def walk(self, el, prefix=''):
        for ch in el.children:
            if isinstance(ch, Comment):
                continue
            if isinstance(ch, NavigableString):
                self.buf += str(ch)
                continue
            if not isinstance(ch, Tag):
                continue
            name = ch.name
            if name in ('br',):
                self.flush(prefix)
                continue
            if name == 'table' and max([len(tr.find_all(['td', 'th'], recursive=False)) for tr in ch.find_all('tr')] or [0]) <= 1:
                self.flush(prefix)
                self.walk(ch, prefix)
                self.flush(prefix)
                continue
            if name == 'table':
                self.flush(prefix)
                rows = []
                for tr in ch.find_all('tr'):
                    cells = [norm(c.get_text(' ')) for c in tr.find_all(['td', 'th'])]
                    if any(cells):
                        rows.append('| ' + ' | '.join(cells) + ' |')
                if rows:
                    ncol = rows[0].count('|') - 1
                    rows.insert(1, '|' + ' --- |' * ncol)
                    self.lines.append('')
                    self.lines.extend(rows)
                    self.lines.append('')
                continue
            if re.match(r'h[1-6]$', name):
                self.flush(prefix)
                t = norm(ch.get_text(' '))
                if t:
                    self.lines.append('')
                    self.lines.append('#' * min(int(name[1]) + 1, 6) + ' ' + t)
                    self.lines.append('')
                continue
            if name == 'li':
                self.flush(prefix)
                sub = MD()
                sub.walk(ch)
                sub.flush()
                items = [l for l in sub.lines if l.strip()]
                if items:
                    self.lines.append(prefix + '- ' + items[0].lstrip('# '))
                    for l in items[1:]:
                        self.lines.append(prefix + '  ' + l)
                continue
            if name in BLOCK or ch.find(list(BLOCK)):
                self.flush(prefix)
                self.walk(ch, prefix)
                self.flush(prefix)
                if name in ('p', 'blockquote', 'ul', 'ol', 'figure', 'div', 'section', 'details', 'dd', 'td', 'tr'):
                    self.lines.append('')
                continue
            self.buf += ch.get_text()

    def text(self):
        out, prev_blank = [], True
        for l in self.lines:
            blank = not l.strip()
            if blank and prev_blank:
                continue
            out.append(l.rstrip())
            prev_blank = blank
        return '\n'.join(out).strip() + '\n'


def main_element(soup, host):
    for t in soup(['script', 'style', 'noscript', 'svg', 'iframe', 'img', 'picture', 'video', 'source', 'template']):
        t.decompose()
    for t in soup.select('blockquote.instagram-media, blockquote.tiktok-embed, .instagram-media'):
        t.decompose()
    if 'labour.org.nz' in host:
        return soup.find(id='root-themed-grid-wrapper') or soup.find(id='main-wrapper')
    if 'scoop.co.nz' in host:
        el = soup.find(id='article')
        if el:
            for t in el.select('.share, .social, .story-tools, .ad, [class*=advert], [class*=sharing]'):
                t.decompose()
        return el
    if 'rnz.co.nz' in host:
        el = soup.select_one('article')
        if el:
            for t in el.select('aside, nav, [class*=share], [class*=related], [class*=newsletter], [data-testid*=share]'):
                t.decompose()
        return el
    return soup.find('main') or soup.body


def page_title(soup):
    if soup.title:
        return norm(soup.title.get_text())
    return ''


def write_doc(slug, front, body):
    os.makedirs(OUT, exist_ok=True)
    fm = ['---'] + ['%s: %s' % (k, json.dumps(v, ensure_ascii=False)) for k, v in front.items()] + ['---', '']
    open(os.path.join(OUT, slug + '.md'), 'w').write('\n'.join(fm) + body)


def main():
    idx = json.load(open(os.path.join(RAW, 'fetch_index.json')))
    docmap = {}
    for url, rec in idx.items():
        slug = rec['slug']
        path = os.path.join(ROOT, rec['file']) if rec.get('file') else None
        front = {'title': '', 'party': 'labour', 'source_url': url, 'retrieved': rec.get('retrieved', ''),
                 'format': 'pdf' if path and path.endswith('.pdf') else 'html', 'fetch_method': 'curl (direct, original URL)'}
        if path and not os.path.exists(path) and os.path.exists(path + '.gz'):
            path = path + '.gz'  # raw HTML is stored gzipped to keep the repo small
        if rec.get('status') != '200' or not path or not os.path.exists(path):
            front['title'] = 'NOT RETRIEVABLE: ' + url
            write_doc(slug, front, '# Not retrievable\n\nThe source %s could not be fetched (HTTP status %s; %s). '
                      'No text is reproduced here.\n' % (url, rec.get('status'), rec.get('err') or 'no detail'))
            docmap[url] = {'doc': 'documents/%s.md' % slug, 'title': front['title'], 'ok': False}
            continue
        if path.endswith('.pdf'):
            txt = subprocess.run(['pdftotext', path, '-'], capture_output=True, text=True).stdout
            front['title'] = PDF_TITLES.get(url, os.path.basename(path))
            front['pdf_copy'] = os.path.relpath(path, ROOT)
            body = ('# ' + front['title'] + '\n\nText extracted with `pdftotext` in reading order (verbatim; page breaks removed; table columns may not line up - see the PDF). '
                    'Original PDF kept at `' + front['pdf_copy'] + '`.\n\n```text\n' + txt.replace('\f', '\n').strip() + '\n```\n')
        else:
            if path.endswith('.gz'):
                import gzip
                html = gzip.open(path, 'rt', encoding='utf-8', errors='replace').read()
            else:
                html = open(path, encoding='utf-8', errors='replace').read()
            soup = BeautifulSoup(html, 'html.parser')
            front['title'] = page_title(soup)
            host = url.split('/')[2]
            el = main_element(soup, host)
            md = MD()
            if el is not None:
                md.walk(el)
                md.flush()
            body = md.text()
            for marker in ('\n© Scoop Media', '\nTitles, characters and all other elements'):
                if marker in body:
                    body = body.split(marker)[0].rstrip() + '\n'
            if url.rstrip('/').endswith('/laboursaver'):
                body = ('> Note: this page is an interactive JavaScript savings calculator; the calculator figures are generated '
                        'in the browser and are not part of the published HTML. The text below is the static page text.\n\n' + body)
            if 'tvnz.co.nz' in host:
                body = ('> Note: this source is a TVNZ video page (1News Leaders Debate). The debate itself is video only; '
                        'no transcript is published on the page. The text below is everything the page itself displays.\n\n' + body)
            m = re.search(r'By LabourVoices\s*\n+\s*(\d{1,2} \w+ \d{4})', body)
            if m:
                front['published'] = m.group(1)
            front['title'] = re.sub(r'\s*[-|]\s*(NZ Labour|Scoop News|RNZ News)\s*$', '', front['title'])
        write_doc(slug, front, body)
        docmap[url] = {'doc': 'documents/%s.md' % slug, 'title': front['title'], 'ok': len(body) > 200, 'chars': len(body)}
    json.dump(docmap, open(os.path.join(RAW, 'docmap.json'), 'w'), indent=1)
    for u, d in docmap.items():
        if not d['ok']:
            print('PROBLEM', u, d)
    print(len(docmap), 'documents')


if __name__ == '__main__':
    main()

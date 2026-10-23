#!/usr/bin/env python3
"""Extract main content from fetched National Party HTML pages as Markdown-ish text.
Library module + CLI: python3 -I tools/policies_national_extract.py <html file>  (prints extracted md)
"""
import re, sys, json
from bs4 import BeautifulSoup, NavigableString, Tag

BLOCK = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'blockquote', 'td', 'th', 'figcaption', 'summary', 'dt', 'dd'}


def _inline(el):
    """Text of an element with inline whitespace normalised."""
    t = el.get_text(' ', strip=False)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def blocks(root):
    """Yield (tag, text) for block-level leaves in document order."""
    out = []

    def walk(node):
        for ch in node.children:
            if isinstance(ch, NavigableString):
                t = re.sub(r'\s+', ' ', str(ch)).strip()
                if t:
                    out.append(('text', t))
                continue
            if not isinstance(ch, Tag):
                continue
            if ch.name in ('script', 'style', 'svg', 'noscript', 'iframe', 'form', 'button', 'img', 'video', 'picture', 'template'):
                continue
            if ch.name in BLOCK and not ch.find(list(BLOCK - {ch.name}) if ch.name != 'li' else ['p', 'li', 'h1', 'h2', 'h3', 'h4']):
                t = _inline(ch)
                if t:
                    out.append((ch.name, t))
            elif ch.name == 'br':
                continue
            else:
                walk(ch)
    walk(root)
    return out


def to_md(bl):
    lines = []
    for tag, t in bl:
        if tag in ('h1', 'h2'):
            lines.append('## ' + t)
        elif tag in ('h3', 'h4', 'h5', 'h6'):
            lines.append('### ' + t)
        elif tag == 'li':
            lines.append('- ' + t)
        elif tag == 'blockquote':
            lines.append('> ' + t)
        else:
            lines.append(t)
    return '\n\n'.join(lines)


def soup(path):
    return BeautifulSoup(open(path, encoding='utf-8', errors='replace').read(), 'html.parser')


def national_main(path):
    """Return (title, meta, blocks) for a national.org.nz page with site chrome removed."""
    s = soup(path)
    m = s.find('main') or s.body
    bl = blocks(m)
    texts = [t for _, t in bl]
    # strip leading breadcrumb
    start = next((i for i, (tag, _) in enumerate(bl) if tag == 'h1'), 0)
    end = len(bl)
    for i, (tag, t) in enumerate(bl):
        if i > start and t in ('Latest News', 'More Policies', 'Related news', 'More news'):
            end = i
            break
    bl = bl[start:end]
    title = s.title.get_text(strip=True) if s.title else ''
    return title, bl


def beehive_main(path):
    s = soup(path)
    art = s.select_one('.ds-three-col__main') or s.select_one('article') or s.find('main')
    bl = blocks(art)
    end = len(bl)
    for i, (tag, t) in enumerate(bl):
        if t.lower().startswith(('share this', 'related ministers', 'related portfolios')):
            end = i; break
    h1 = s.find('h1')
    return (h1.get_text(' ', strip=True) if h1 else ''), bl[:end]


def rnz_main(path):
    s = soup(path)
    art = s.select_one('.article__body') or s.select_one('article') or s.find('main')
    h1 = s.find('h1')
    return (h1.get_text(' ', strip=True) if h1 else ''), blocks(art)


if __name__ == '__main__':
    p = sys.argv[1]
    f = beehive_main if 'beehive' in p else rnz_main if 'rnz.co.nz' in p else national_main
    t, bl = f(p)
    print('TITLE:', t)
    print(to_md(bl))

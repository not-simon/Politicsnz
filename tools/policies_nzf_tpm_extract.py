#!/usr/bin/env python3
"""Extract the verbatim body text of a Scoop press-release page (www.scoop.co.nz or community.scoop.co.nz)
as Markdown-ish plain text (whitespace normalised only).  Used by tools/policies_nzf_tpm_build.py.
CLI: python3 -I tools/policies_nzf_tpm_extract.py <file.html>"""
import re, sys
from bs4 import BeautifulSoup, NavigableString

BLOCKS = ["p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "tr", "div"]

def _clean(t):
    return re.sub(r"[ \t\r\f\v ]+", " ", t).strip()

def extract(html):
    s = BeautifulSoup(html, "html.parser")
    meta = {}
    art = s.find(id="article")
    if art is not None:  # www.scoop.co.nz story
        h1 = art.find("h1"); meta["title"] = _clean(h1.get_text(" ")) if h1 else ""
        by = art.find(class_="byline"); meta["byline"] = _clean(by.get_text(" ")) if by else ""
        top = art.find(class_="story-top")
        if top: top.decompose()
        for j in art.select(".article-left-box-wrapper, script, style, #story-footer, iframe, noscript, ins"):
            j.decompose()
        # cut everything after the "(c) Scoop Media" terms link
        term = art.find("a", href=re.compile(r"about/terms\.html"))
        if term:
            for el in list(term.find_all_next()):
                if el is not term: el.extract()
            for sib in list(term.next_siblings): sib.extract()
            term.extract()
        root = art
    else:  # community.scoop.co.nz (WordPress)
        h1 = s.find("h1"); meta["title"] = _clean(h1.get_text(" ")) if h1 else ""
        root = s.select_one(".entry-content") or s.select_one("article") or s.body
        tm = s.find("time"); meta["byline"] = _clean(tm.get_text(" ")) if tm else ""
        for j in root.select("script, style, .sharedaddy, .jp-relatedposts, iframe, noscript, .addtoany_share_save_container"):
            j.decompose()
    pdfs = sorted({a["href"] for a in root.find_all("a", href=True) if a["href"].lower().endswith(".pdf")})
    links = [(_clean(a.get_text(" ")), a["href"]) for a in root.find_all("a", href=True)]
    for br in root.find_all("br"): br.replace_with("\n")
    for li in root.find_all("li"): li.insert(0, NavigableString("⁣- "))
    for h in root.find_all(["h2", "h3", "h4", "h5", "h6"]): h.insert(0, NavigableString("⁣### "))
    for b in root.find_all(BLOCKS):
        b.insert(0, NavigableString("⁢")); b.append(NavigableString("⁢"))
    raw = root.get_text()
    paras = []
    for chunk in raw.split("⁢"):
        # inside a paragraph, single newlines from source wrapping are whitespace; explicit <br> are kept? Scoop wraps
        # source text at ~60 cols, so join lines.
        t = _clean(chunk.replace("\n", " "))
        t = t.replace("⁣", "")
        if t: paras.append(t)
    text = "\n\n".join(paras)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return meta, text, pdfs, links

if __name__ == "__main__":
    m, t, p, l = extract(open(sys.argv[1], encoding="utf-8", errors="replace").read())
    print(m); print(p); print(t)


def extract_nb(html):
    """Main content of a NationBuilder page (nzfirst.nz / maoriparty.org.nz Common Crawl capture), whitespace
    normalised. Removes share widgets, breadcrumbs, navigation, forms and scripts. Returns (title, text, links)."""
    s = BeautifulSoup(html, "html.parser")
    title = _clean(s.title.get_text(" ")) if s.title else ""
    root = s.find("main") or s.find(id="content") or s.body
    for j in root.find_all(True):
        if j.decomposed if hasattr(j, "decomposed") else False: continue
        attrs = " ".join([" ".join(j.get("class", []) or []), j.get("id", "") or ""]).lower()
        if j.name in ("script", "style", "nav", "form", "button", "noscript", "iframe", "svg", "select") or \
           re.search(r"share|breadcrumb|social|sharing|skip-link|signup-form|donate-form|pagination", attrs):
            j.decompose()
    links = [(_clean(a.get_text(" ")), a["href"]) for a in root.find_all("a", href=True)]
    for br in root.find_all("br"): br.replace_with("\n")
    for li in root.find_all("li"): li.insert(0, NavigableString("⁣- "))
    for h in root.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]): h.insert(0, NavigableString("⁣### "))
    for b in root.find_all(BLOCKS + ["section", "article", "header", "main"]):
        b.insert(0, NavigableString("⁢")); b.append(NavigableString("⁢"))
    paras = []
    for chunk in root.get_text().split("⁢"):
        t = _clean(chunk.replace("\n", " ")).replace("⁣", "")
        if t and t not in ("###", "-") and not (paras and paras[-1] == t):
            paras.append(t)
    return title, "\n\n".join(paras), links

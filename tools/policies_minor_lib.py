"""Shared helpers for the minor-party / TOP policy archive (tools/policies_minor_*).

Run with: python3 -I tools/policies_minor_<x>.py  (downloads are untrusted data).
Raw downloads -> raw/party-docs/<slug>/ ; documents -> parties/<slug>/policies/documents/.
"""
import hashlib, json, os, re, subprocess, sys
from urllib.parse import urljoin, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
RETRIEVED = "2026-10-23"


def raw_dir(slug):
    d = os.path.join(ROOT, "raw", "party-docs", slug)
    os.makedirs(d, exist_ok=True)
    return d


def safe_name(url, ext=None):
    p = urlparse(url)
    base = (p.netloc + p.path).strip("/").replace("/", "_") or "index"
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", base)[:150]
    if p.query:
        base += "_" + hashlib.md5(p.query.encode()).hexdigest()[:8]
    if ext and not base.lower().endswith(ext):
        base += ext
    return base


def fetch(url, slug, ext=".html", refresh=False, browser=False):
    """Download url into raw/party-docs/<slug>/ (cached). Returns (path, http_code)."""
    path = os.path.join(raw_dir(slug), safe_name(url, ext))
    if os.path.exists(path) and os.path.getsize(path) > 0 and not refresh:
        return path, 200
    if browser:
        env = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")
        r = subprocess.run(["timeout", "120", "node", os.path.join(ROOT, "tools", "fetch_page.js"), url, path],
                           env=env, capture_output=True, text=True)
        return (path if os.path.exists(path) else None), (200 if os.path.exists(path) else 0)
    import time
    for attempt in range(4):
        r = subprocess.run(["curl", "-sS", "-L", "--max-time", "60", "-A", UA, "-o", path, "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        code = int(r.stdout.strip() or 0)
        if code not in (0, 429, 502, 503):
            break
        time.sleep(6 * (attempt + 1))
    if code != 200:
        try:
            os.remove(path)
        except OSError:
            pass
        return None, code
    return path, code


def soup(path):
    from bs4 import BeautifulSoup
    return BeautifulSoup(open(path, encoding="utf-8", errors="replace").read(), "html.parser")


def links(path, base):
    s = soup(path)
    out = []
    for a in s.find_all("a", href=True):
        out.append((urljoin(base, a["href"]).split("#")[0], a.get_text(" ", strip=True)))
    return out


def html_to_md(el):
    """Convert a bs4 element to Markdown, keeping all text (only markup normalised)."""
    from markdownify import markdownify
    from bs4 import NavigableString, Comment
    for bad in el.find_all(["script", "style", "noscript", "form", "iframe", "svg", "button", "img", "picture", "video"]):
        bad.decompose()
    for c in el.find_all(string=lambda x: isinstance(x, Comment)):
        c.extract()
    for t in el.find_all(string=True):
        if isinstance(t, NavigableString) and not t.find_parent("pre") and "\n" in t:
            t.replace_with(re.sub(r"\s*\n\s*", " ", str(t)))
    md = markdownify(str(el), heading_style="ATX", bullets="-", strip=["img"], newline_style="backslash")
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"[ \t]{2,}", " ", md)
    return md.strip() + "\n"


def main_md(path, selectors=("main", "article", "#content", ".content", "body"), drop=("header", "nav", "footer")):
    s = soup(path)
    el = None
    for sel in selectors:
        el = s.select_one(sel)
        if el is not None and len(el.get_text(strip=True)) > 50:
            break
    if el is None:
        el = s.body or s
    for tag in drop:
        for t in el.select(tag):
            t.decompose()
    title = (s.title.get_text(strip=True) if s.title else "")
    return title, html_to_md(el)


def pdf_text(path, layout=False):
    r = subprocess.run(["pdftotext"] + (["-layout"] if layout else []) + [path, "-"], capture_output=True, text=True)
    t = r.stdout.replace("\u200b", "").replace("\f", "\n\n")
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{4,}", "\n\n\n", t)
    return t.strip() + "\n"


def write_doc(party, docslug, title, source_url, body, fmt="html", method="curl", note=None, extra=None):
    d = os.path.join(ROOT, "parties", party, "policies", "documents")
    os.makedirs(d, exist_ok=True)
    fm = ["---", f"title: {json.dumps(title, ensure_ascii=False)}", f"party: {party}",
          f"source_url: {source_url}", f"retrieved: {RETRIEVED}", f"format: {fmt}", f"fetch_method: {method}"]
    for k, v in (extra or {}).items():
        fm.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    fm.append("---")
    parts = ["\n".join(fm), "", f"# {title}", ""]
    if note:
        parts += [f"> Archive note: {note}", ""]
    if body is None:
        parts += ["## Full text", "", "**Not retrievable.** The full text could not be captured; see the archive note above. "
                  "Nothing in this file is a paraphrase of the original.", ""]
    else:
        parts += ["## Full text (verbatim)", "", body.strip(), ""]
    p = os.path.join(d, docslug + ".md")
    open(p, "w", encoding="utf-8").write("\n".join(parts))
    return "documents/" + docslug + ".md"


def write_json(party, policies):
    d = os.path.join(ROOT, "parties", party, "policies")
    os.makedirs(d, exist_ok=True)
    json.dump(policies, open(os.path.join(d, "policies.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    # quick CLI: python3 -I tools/policies_minor_lib.py links <slug> <url>
    cmd, slug, url = sys.argv[1:4]
    p, c = fetch(url, slug)
    print("code", c, p, file=sys.stderr)
    if p and cmd == "links":
        seen = set()
        host = urlparse(url).netloc
        for h, t in links(p, url):
            if h in seen:
                continue
            seen.add(h)
            if urlparse(h).netloc.endswith(host.replace("www.", "")) or h.lower().endswith(".pdf"):
                print(h, "|", t[:80])
    elif p and cmd == "md":
        print(main_md(p)[1])


def scoop_md(path):
    """Extract (title, date/byline, markdown body) of a Scoop press release."""
    from bs4 import Comment
    s = soup(path)
    art = s.select_one("#article")
    title = art.select_one("h1").get_text(" ", strip=True)
    by = art.select_one(".byline")
    byline = by.get_text(" ", strip=True) if by else ""
    top = art.select_one(".story-top")
    if top:
        top.decompose()
    for bq in art.find_all("blockquote"):
        bq.unwrap()
    for sel in [".article-left-box-wrapper", "#story-footer", "#byline-block", ".byline-block", "script", "style"]:
        for t in art.select(sel):
            t.decompose()
    for c in art.find_all(string=lambda x: isinstance(x, Comment)):
        c.extract()
    for a in art.find_all("a"):
        if "scoop.co.nz/about/terms" in (a.get("href") or ""):
            a.decompose()
    md = html_to_md(art)
    md = re.sub(r"(?m)^\s*>\s*$", "", md)
    # rejoin hard-wrapped lines inside paragraphs (Scoop wraps at ~60 chars)
    paras = re.split(r"\n\s*\n", md)
    out = []
    for p in paras:
        lines = p.split("\n")
        if all(not re.match(r"\s*([-*]|\d+\.|#|>|\|)", l) for l in lines[1:]):
            p = " ".join(l.strip() for l in lines)
        out.append(p.strip())
    md = "\n\n".join(x for x in out if x)
    return title, byline, md.strip() + "\n"


def pdf_md(path):
    """pdftotext -layout, lightly normalised to Markdown: bullets become '-', indentation removed,
    page-break form feeds become a horizontal rule. Words are unchanged."""
    r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
    t = r.stdout.replace("\u200b", " ")
    pages = t.split("\f")
    out_pages = []
    for pg in pages:
        lines = []
        for raw in pg.split("\n"):
            s = raw.rstrip()
            ind = len(s) - len(s.lstrip())
            s = s.strip()
            m = re.match(r"^([•●▪■◦○\-–])\s+(.*)$", s)
            if m and m.group(1) in "•●▪■":
                s = "- " + m.group(2)
            elif m and m.group(1) in "◦○":
                s = "    - " + m.group(2)
            s = re.sub(r"\s{2,}", " ", s)
            lines.append(s)
        txt = "\n".join(lines)
        txt = re.sub(r"\n{3,}", "\n\n", txt).strip()
        if txt:
            out_pages.append(txt)
    return ("\n\n---\n\n".join(out_pages)).strip() + "\n"


def soup_from_html(h):
    from bs4 import BeautifulSoup
    return BeautifulSoup("<div>" + h + "</div>", "html.parser").div


def wix_blog_md(path):
    """Wix blog posts keep their body in the 'wix-warmup-data' JSON (Ricos nodes). Returns markdown or None."""
    s = soup(path)
    tag = s.find("script", id="wix-warmup-data")
    if not tag:
        return None
    data = json.loads(tag.string)
    out = []

    def text_of(node):
        if node.get("type") == "TEXT":
            return node.get("textData", {}).get("text", "")
        return "".join(text_of(n) for n in node.get("nodes", []))

    def walk(node, depth=0):
        t = node.get("type")
        if t == "HTML":
            h = node.get("htmlData", {}).get("html")
            if h:
                from bs4 import BeautifulSoup
                hs = BeautifulSoup(h, "html.parser")
                body = hs.body or hs
                for x in body.select("style, script, head"):
                    x.decompose()
                for x in body.find_all(["td", "th"]):
                    x.name = "div"
                for x in body.find_all(["table", "tbody", "thead", "tr", "center"]):
                    x.unwrap()
                out.append(html_to_md(body))
            return
        if t == "HEADING":
            lvl = node.get("headingData", {}).get("level", 2)
            out.append("#" * min(lvl + 1, 6) + " " + text_of(node).strip())
            return
        if t == "PARAGRAPH":
            out.append(text_of(node).strip())
            return
        if t in ("BULLETED_LIST", "ORDERED_LIST"):
            for i, li in enumerate(node.get("nodes", []), 1):
                out.append(("- " if t == "BULLETED_LIST" else f"{i}. ") + text_of(li).strip())
            return
        for n in node.get("nodes", []):
            walk(n, depth + 1)

    def find_contents(o):
        if isinstance(o, dict):
            if "nodes" in o and isinstance(o["nodes"], list) and o.get("nodes") and isinstance(o["nodes"][0], dict) and "type" in o["nodes"][0]:
                yield o
                return
            for v in o.values():
                yield from find_contents(v)
        elif isinstance(o, list):
            for v in o:
                yield from find_contents(v)

    for c in find_contents(data):
        for n in c["nodes"]:
            walk(n)
    md = "\n\n".join(x for x in out if x and x.strip())
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n" if md.strip() else None

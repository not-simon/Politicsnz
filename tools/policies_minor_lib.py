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
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "60", "-A", UA, "-o", path, "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    code = int(r.stdout.strip() or 0)
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
    for bad in el.find_all(["script", "style", "noscript", "form", "iframe", "svg", "button"]):
        bad.decompose()
    md = markdownify(str(el), heading_style="ATX", bullets="-", strip=["img"])
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


def pdf_text(path):
    r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
    t = r.stdout
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

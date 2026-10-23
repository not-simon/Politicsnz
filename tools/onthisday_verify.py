#!/usr/bin/env python3
"""Check every draft 'On this day' entry against the raw Wikipedia wikitext in raw/onthisday/wikipedia/.

An entry passes when the article named in entry["verify"] (a Wikipedia title, or a list of titles) contains the
event date in one of the common wikitext forms ("14 October 2023", "October 14, 2023", "2023-10-14",
"{{start date|2023|10|14}}", "|2023|10|14", or "14 October" within 300 characters of "2023"). For a range
event, entry["verify_date"] may give the exact ISO date to test instead (e.g. the first day of polling).

Usage: python3 tools/onthisday_verify.py <draft.json> [--show-fail]
The draft format is the list-of-months format used by tools/onthisday_build.py.
"""
import json, os, re, sys, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, "raw", "onthisday", "wikipedia")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
_cache = {}


def wikitext(title):
    if title in _cache:
        return _cache[title]
    fn = urllib.parse.quote(title.replace(" ", "_"), safe="") + ".wikitext"
    p = os.path.join(W, fn)
    txt = open(p, encoding="utf-8").read() if os.path.exists(p) else None
    if txt is not None:
        txt = txt.replace("&nbsp;", " ").replace(" ", " ")
    _cache[title] = txt
    return txt


def date_found(txt, y, m, d):
    mon = MONTHS[m - 1]
    pats = [
        rf"\b{d} {mon},? {y}\b",
        rf"\b{mon} {d},? {y}\b",
        rf"\b{y}-{m:02d}-{d:02d}\b",
        rf"\|\s*{y}\s*\|\s*{m}\s*\|\s*{d}\s*[|}}]",
        rf"\|\s*{y}\s*\|\s*{m:02d}\s*\|\s*{d:02d}\s*[|}}]",
        rf"\b{d}(?:st|nd|rd|th)? (?:of )?{mon},? {y}\b",
        rf"\b{d}\s*[–-]\s*\d{{1,2}} {mon} {y}\b",   # "14–15 October 2023" (start of range)
        rf"\b\d{{1,2}}\s*[–-]\s*{d} {mon} {y}\b",   # end of range
    ]
    for p in pats:
        if re.search(p, txt):
            return True
    # "14 October" ... "2023" nearby
    for mm in re.finditer(rf"\b{d} {mon}\b|\b{mon} {d}\b", txt):
        s = max(0, mm.start() - 300)
        if re.search(rf"\b{y}\b", txt[s:mm.end() + 300]):
            return True
    return False


def check_entry(e):
    """Return (status, detail). status in ok / nopage / nodate."""
    ver = e.get("verify")
    if not ver:
        return "noverify", "no verify title"
    titles = ver if isinstance(ver, list) else [ver]
    iso = e.get("verify_date") or e.get("date")
    y, m, d = (int(x) for x in iso.split("-"))
    seen_page = False
    for t in titles:
        txt = wikitext(t)
        if txt is None:
            continue
        seen_page = True
        if date_found(txt, y, m, d):
            return "ok", t
    if not seen_page:
        return "nopage", ",".join(titles)
    return "nodate", ",".join(titles)


def main(argv):
    show = "--show-fail" in argv
    path = [a for a in argv if not a.startswith("--")][0]
    draft = json.load(open(path, encoding="utf-8"))
    entries = draft if isinstance(draft, list) else draft["entries"]
    counts = {}
    fails = []
    for e in entries:
        st, det = check_entry(e)
        counts[st] = counts.get(st, 0) + 1
        if st != "ok":
            fails.append((st, e.get("date"), e.get("title"), det))
    print(counts)
    if show:
        for f in fails:
            print("  ", *f)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

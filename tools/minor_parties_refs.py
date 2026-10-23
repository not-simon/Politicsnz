#!/usr/bin/env python3
"""Print the cited URLs in a Wikipedia wikitext file with ~120 chars of the preceding article text,
so claims can be traced to primary sources. Usage: python3 -I tools/minor_parties_refs.py <file.wikitext> [keyword]"""
import re, sys
t = open(sys.argv[1]).read()
kw = sys.argv[2].lower() if len(sys.argv) > 2 else None
for m in re.finditer(r"<ref[^>/]*>(.*?)</ref>", t, re.S):
    body = m.group(1)
    u = re.search(r"url\s*=\s*([^|\s}]+)", body)
    if not u: continue
    title = re.search(r"title\s*=\s*([^|}]+)", body)
    date = re.search(r"\|\s*date\s*=\s*([^|}]+)", body)
    pre = re.sub(r"<ref.*?(</ref>|/>)", "", t[max(0, m.start()-400):m.start()], flags=re.S)
    pre = re.sub(r"\s+", " ", pre)[-140:]
    line = f"- {pre!r}\n    {title.group(1).strip() if title else ''} ({date.group(1).strip() if date else ''}) {u.group(1)}"
    if kw is None or kw in line.lower():
        print(line)

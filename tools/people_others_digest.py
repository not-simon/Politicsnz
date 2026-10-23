#!/usr/bin/env python3
"""Print a compact digest of a cached Wikipedia article: meta, infobox key fields, extract, and cited URLs.
Usage: python3 -I tools/people_others_digest.py <cache basename> [maxchars]"""
import sys, json, re, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw", "people", "others", "wiki")
b = sys.argv[1]; mx = int(sys.argv[2]) if len(sys.argv) > 2 else 14000
m = json.load(open(f"{D}/{b}.meta.json")); w = open(f"{D}/{b}.wikitext").read(); t = open(f"{D}/{b}.txt").read()
print("META", m["title"], m["revid"], m["url"], "IMG:", m.get("pageimage"))
ib = re.search(r"\{\{Infobox.*?\n\}\}", w, re.S)
if ib:
    for line in ib.group(0).split("\n"):
        if re.match(r"\s*\|\s*(office|term_start|term_end|birth_date|death_date|party|otherparty|constituency|predecessor|successor|image|order|primeminister|leader|deputy)\w*\s*=", line):
            l = re.sub(r"<ref.*?(</ref>|/>)", "", line); l = re.sub(r"\[\[(?:[^|\]]+\|)?([^\]]+)\]\]", r"\1", l)
            if l.split("=",1)[1].strip(): print("  ", l.strip()[:160])
t = re.sub(r"\n== (References|Notes|External links|See also|Further reading) ==.*", "", t, flags=re.S)
print("TEXT", len(t)); print(t[:mx])
urls = re.findall(r"\|\s*title\s*=\s*([^|}]+?)\s*\|[^}]*?\burl\s*=\s*(https?://[^\s|}]+)|\burl\s*=\s*(https?://[^\s|}]+)[^}]*?\|\s*title\s*=\s*([^|}]+)", w)
print("REFS")
seen=set()
for a,b2,c,d in urls[:int(os.environ.get("NREF","25"))]:
    u=b2 or c; ti=a or d
    if u in seen: continue
    seen.add(u); print(" -", ti.strip()[:110], "|", u)

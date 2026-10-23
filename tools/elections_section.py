#!/usr/bin/env python3
"""Print cleaned text of a section of a raw/elections wikitext file. Usage: elections_section.py FILE 'Heading' [maxchars]"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elections_common import clean, RAW
f, h = sys.argv[1], sys.argv[2]; mx = int(sys.argv[3]) if len(sys.argv) > 3 else 6000
t = open(os.path.join(RAW, f) if not os.path.exists(f) else f).read()
m = re.search(r"^(=+)\s*" + re.escape(h) + r"\s*\1\s*$", t, re.M)
if not m: print("no heading"); sys.exit()
lvl = len(m.group(1))
rest = t[m.end():]
e = re.search(r"^={1,%d}[^=].*?={1,%d}\s*$" % (lvl, lvl), rest, re.M)
sec = rest[: e.start()] if e else rest
sec = re.sub(r"\{\|.*?\n\|\}", "[table]", sec, flags=re.S)
print(clean(re.sub(r"\n(=+)([^=]+)\1", r"\n## \2.", sec))[:mx])

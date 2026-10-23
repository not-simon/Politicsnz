#!/usr/bin/env python3
"""Find candidate events for a calendar day in the saved Wikipedia wikitext corpus.

Usage: python3 tools/onthisday_daygrep.py 01-06 [02-10 ...] [--all]
Prints sentences in raw/onthisday/wikipedia/*.wikitext containing "<day> <Month> <year>" for the given days,
filtered to lines with political keywords unless --all is given. Output is untrusted data for the editor to read.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, "raw", "onthisday", "wikipedia")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
KW = re.compile(r"elect|parliament|minister|premier|govern|party|referend|act\b|bill\b|treaty|tribunal|vote|"
                r"speaker|cabinet|coalition|resign|sworn|leader|māori|maori|suffrage|constitution|council|"
                r"mp\b|by-election|petition|protest|hīkoi|hikoi|royal assent|proclaim|legislat", re.I)


def main(argv):
    show_all = "--all" in argv
    days = [a for a in argv if not a.startswith("--")]
    corpus = []
    for f in sorted(glob.glob(os.path.join(W, "*.wikitext"))):
        t = open(f, encoding="utf-8").read().replace("&nbsp;", " ")
        t = re.sub(r"<ref[^>]*/>", "", t)
        t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S)
        t = re.sub(r"\{\{(?:cite|Cite)[^}]*\}\}", "", t)
        corpus.append((os.path.basename(f)[:-9], t))
    for day in days:
        m, d = int(day[:2]), int(day[3:])
        mon = MONTHS[m - 1]
        rx = re.compile(rf"\b{d} {mon},? (1[6-9]\d\d|20[0-2]\d)\b|\b{mon} {d},? (1[6-9]\d\d|20[0-2]\d)\b")
        print(f"\n===== {day} ({d} {mon})")
        seen = set()
        for name, t in corpus:
            for mm in rx.finditer(t):
                s = t.rfind("\n", 0, mm.start())
                s = max(s, mm.start() - 220)
                ctx = t[s:mm.end() + 180].replace("\n", " ")
                ctx = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", ctx)
                ctx = re.sub(r"\{\{[^}]*\}\}", "", ctx)
                ctx = re.sub(r"'''?", "", ctx)
                ctx = re.sub(r"\s+", " ", ctx).strip()
                if not show_all and not KW.search(ctx):
                    continue
                if ctx.count("|") > 3:
                    continue
                key = (mm.group(1) or mm.group(2), ctx[:50])
                if key in seen:
                    continue
                seen.add(key)
                print(f"  {mm.group(1) or mm.group(2)} [{name[:40]}] {ctx[:300]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

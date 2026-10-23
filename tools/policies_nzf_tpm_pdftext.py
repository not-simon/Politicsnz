#!/usr/bin/env python3
"""Extract text from a party policy PDF with `pdftotext -raw` (content-stream order, which keeps the designed
Te Pāti Māori manifesto chapters' words intact). Normalisation only: the bullet glyph (emitted as BEL on its own
line) becomes "• " joined to its item; private-use icon glyphs are dropped. No words are changed.
CLI: python3 -I tools/policies_nzf_tpm_pdftext.py <file.pdf>"""
import re, subprocess, sys

def pdf_text(path):
    out = subprocess.run(["pdftotext", "-raw", "-enc", "UTF-8", path, "-"], capture_output=True).stdout.decode("utf-8", "replace")
    pages = []
    for p in out.split("\f"):
        p = re.sub(r"[-]", "", p)
        p = re.sub(r"\x07[ \t]*\n?[ \t]*", "• ", p)
        p = re.sub(r"(?m)^•[ \t]*\n(?=•)", "", p)                       # empty bullet before a bullet
        p = re.sub(r"• ([A-ZĀĒĪŌŪ])\n• ([a-zāēīōū])", r"• \1\2", p)      # drop-cap split across bullets
        p = re.sub(r"[ \t]+\n", "\n", p)
        p = re.sub(r"\n{3,}", "\n\n", p).strip()
        if p: pages.append(p)
    return pages

if __name__ == "__main__":
    for n, p in enumerate(pdf_text(sys.argv[1]), 1):
        print(f"--- page {n} ---"); print(p)

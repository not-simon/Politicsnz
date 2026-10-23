#!/usr/bin/env python3
"""Refuse to commit files containing token-shaped strings (GitHub push protection would reject them anyway).
Usage: python3 tools/check_secrets.py  (scans staged files) — exit 1 if anything is found."""
import re, subprocess, sys
PATTERNS = [r"\bsk\.eyJ[\w-]{20,}", r"\bpk\.eyJ[\w-]{20,}", r"\bAKIA[0-9A-Z]{16}\b", r"\bghp_[A-Za-z0-9]{30,}", r"\bxox[baprs]-[A-Za-z0-9-]{10,}", r"AIza[0-9A-Za-z_-]{30,}", r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"]
files = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=AM"], capture_output=True, text=True).stdout.split()
bad = []
for f in files:
    try: t = open(f, "rb").read(2_000_000).decode("utf-8", "ignore")
    except Exception: continue
    for pat in PATTERNS:
        if re.search(pat, t): bad.append((f, pat)); break
if bad:
    print("Token-shaped strings found in staged files:"); [print("  ", f, "matches", pat) for f, pat in bad]; sys.exit(1)
print("no secrets in staged files")

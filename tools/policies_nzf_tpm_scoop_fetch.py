#!/usr/bin/env python3
"""Download Scoop press-release pages listed in raw/party-docs/<party>/scoop_index.json (excluding sidebar items
not issued by the party) into raw/party-docs/<party>/scoop/<code>.html.  Usage: python3 -I tools/policies_nzf_tpm_scoop_fetch.py"""
import json, os, re, subprocess, time
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36"
for party in ["nz-first", "te-pati-maori"]:
    idx = json.load(open(f"raw/party-docs/{party}/scoop_index.json"))
    os.makedirs(f"raw/party-docs/{party}/scoop", exist_ok=True)
    for o in idx:
        m = re.search(r"/stories/([A-Z]{2}\d{4})/(S\d+)/", o["url"]); code = m.group(1) + "-" + m.group(2)
        p = f"raw/party-docs/{party}/scoop/{code}.html"
        if os.path.exists(p) and os.path.getsize(p) > 20000: continue
        r = subprocess.run(["curl", "-sS", "-L", "-A", UA, "--max-time", "40", "-o", p, "-w", "%{http_code}", o["url"]], capture_output=True)
        print(party, code, r.stdout.decode(), o["title"][:70]); time.sleep(0.7)

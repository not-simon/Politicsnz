#!/usr/bin/env python3
"""Search raw/policy.nz/parties/*.json statements (+Why/How text) for a regex; print id, party, statement, source URLs.
Usage: python3 -I tools/quiz_grep_policynz.py <regex> [--full]"""
import json, glob, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pat = re.compile(sys.argv[1], re.I); full = '--full' in sys.argv
def orig(u):
    m = re.search(r'/web/\d+[a-z_]*/(https?://.*)', u or '')
    return m.group(1) if m else u
for f in sorted(glob.glob(os.path.join(ROOT, 'raw/policy.nz/parties/*.json'))):
    d = json.load(open(f))
    for p in d['policies']:
        txt = p['statement'] + ' ' + ' '.join(a.get('value', '') for a in p.get('attributes', []))
        if pat.search(txt):
            print(f"{p['reference']} [{os.path.basename(f)[:-5]}] {p['statement']}")
            for c in p.get('citations', [])[:3]: print('     ', orig(c.get('url')), '|', (c.get('title') or '')[:80])
            if full:
                for a in p.get('attributes', []): print('   ', a['name'], ':', a.get('value', '')[:700])

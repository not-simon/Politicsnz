#!/usr/bin/env python3
"""Compact a .wiki file: inline each <ref> as [url | title | date] so claims can be traced to sources.
Usage: python3 -I tools/record_green_tpm_compact.py file.wiki > out.txt"""
import sys, re
wt = open(sys.argv[1]).read()
named = {}
def summarise(body):
    def f(k):
        m = re.search(r'\|\s*' + k + r'\s*=\s*([^|}]*)', body)
        return m.group(1).strip() if m else ''
    url = f('url') or (re.search(r'https?://[^\s|\]}]+', body).group(0) if re.search(r'https?://[^\s|\]}]+', body) else '')
    return '[%s | %s | %s %s]' % (url, f('title')[:90], f('date'), f('work') or f('website') or f('newspaper') or f('publisher'))
def full(m):
    attrs, body = m.group(1), m.group(2)
    s = summarise(body)
    n = re.search(r'name\s*=\s*"?([^">/]+)"?', attrs or '')
    if n: named[n.group(1).strip()] = s
    return s
wt = re.sub(r'<ref([^>/]*)>(.*?)</ref>', full, wt, flags=re.S)
wt = re.sub(r'<ref\s+name\s*=\s*"?([^">/]+?)"?\s*/>', lambda m: named.get(m.group(1).strip(), '[ref:%s]' % m.group(1)), wt)
wt = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', wt)
wt = re.sub(r"'''?", '', wt)
print(wt)

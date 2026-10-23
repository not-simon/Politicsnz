#!/usr/bin/env python3
"""Render guide/how-to-vote.md from data/guide/howtovote.json so the two never drift apart.
Run: python3 tools/howtovote_render.py"""
import json, os, datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(ROOT, 'data', 'guide', 'howtovote.json')
OUT = os.path.join(ROOT, 'guide', 'how-to-vote.md')

d = json.load(open(SRC, encoding='utf-8'))

def nice_date(s):
    y, m, dd = (int(x) for x in s.split('-'))
    return datetime.date(y, m, dd).strftime('%a %-d %b %Y')

L = []
L.append('# How to vote in the 2026 General Election\n')
L.append(f"*Election day is **Saturday 7 November 2026**, 9am to 7pm. Enrolment closed at **midnight Sunday 25 October**. "
         f"Last checked against the Electoral Commission's pages on {nice_date(d['as_of'])}.*\n")
L.append('> **The rules changed this year.** ' + d['election']['law_change_note'] + '\n')
L.append('This page is generated from [`data/guide/howtovote.json`](../data/guide/howtovote.json). Every fact links to the '
         'Electoral Commission page (vote.nz / elections.nz), the Act, or the news report it came from. Where we could not verify '
         'something, we say so at the bottom. It is not legal advice. If your situation is unusual, call the Commission on '
         '**0800 36 76 56** (free, 24/7).\n')

# Checklist
L.append('## First-time voter checklist\n')
L.append('| # | Step | You are done when... | Link |')
L.append('|---|------|----------------------|------|')
for i, c in enumerate(d['checklist'], 1):
    L.append(f"| {i} | **{c['step']}** | {c['done_when']} | [link]({c['url']}) |")
L.append('')

# Key dates
L.append('## Key dates\n')
L.append('| Date | What happens | Source |')
L.append('|------|--------------|--------|')
for k in d['key_dates']:
    L.append(f"| {nice_date(k['date'])} | {k['event']} | [source]({k['source']}) |")
L.append('')

# Sections
for s in d['sections']:
    L.append(f"## {s['title']}\n")
    L.append('*For: ' + '; '.join(s['who_its_for']) + '.*\n')
    for st in s['steps']:
        date = f" *({nice_date(st['date'])})*" if st.get('date') else ''
        L.append(f"- {st['text']}{date} [[source]]({st['url']}) <sub>{st['source']}</sub>")
    if s.get('notes'):
        L.append('\n**Notes**\n')
        for n in s['notes']:
            L.append(f"- {n}")
    L.append('\n<details><summary>Sources for this section</summary>\n')
    for u in s['sources']:
        L.append(f"- <{u}>")
    L.append('\n</details>\n')

# Voting places
vp = d['voting_places']
L.append('## Finding your nearest voting place\n')
L.append(f"- **Official finder (map):** <{vp['official_finder']}>  ")
L.append(f"- **List by electorate and suburb:** <{vp['official_finder_list_view']}>  ")
L.append(f"- **Phone:** 0800 36 76 56\n")
L.append(f"{vp['deep_link_notes']}\n")
for c in vp['counts_from_commission']:
    L.append(f"- {c['fact']} " + ' '.join(f'[[source]]({u})' for u in c['sources']))
L.append('')
L.append(f"**Data and licence.** {vp['data_endpoint']} {vp['licence']} {vp['when_published']}\n")

# Contacts
L.append('## Contacts\n')
for k, v in d['contacts'].items():
    if k == 'sources':
        continue
    L.append(f"- **{k.replace('_', ' ').capitalize()}:** {v}")
L.append('')

# Could not verify
L.append('## What we could not verify\n')
for c in d['could_not_verify']:
    L.append(f"- {c}")
L.append('')
L.append(f"*Raw sources: {d['raw_sources_folder']}.*\n")
L.append('*Ballot Book NZ is independent and non-partisan. This page tells you how to vote, not who to vote for. '
         'See [docs/EDITORIAL_STANDARDS.md](../docs/EDITORIAL_STANDARDS.md).*')

open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('wrote', OUT, len('\n'.join(L)), 'chars')

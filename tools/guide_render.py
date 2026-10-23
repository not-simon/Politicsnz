#!/usr/bin/env python3
"""Render the plain-English guide (guide/parties.md, guide/issues.md) from data/guide/*.json.

Run after tools/guide_enrich.py:  python3 tools/guide_enrich.py && python3 tools/guide_render.py
Never edit the .md files by hand - edit the JSON and re-render.
"""
import json, pathlib, re
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
G = ROOT / 'data' / 'guide'
OUT = ROOT / 'guide'
guide = json.loads((G / 'parties.json').read_text())
issues = json.loads((G / 'issues.json').read_text())
PARTIES = guide['parties']
BY = {p['slug']: p for p in PARTIES}


def order_key(p):
    pa = p.get('polling_avg_2026') or {}
    return (-p['current_seats']['seats'], -(pa.get('average_pct') or 0), p['short_name'].lower())


ORDER = [p['slug'] for p in sorted(PARTIES, key=order_key)]
ICON = {'wallet': '👛', 'heart': '❤️', 'briefcase': '💼', 'home': '🏠', 'coins': '🪙', 'bolt': '⚡', 'hands': '🤝',
        'shield': '🛡️', 'leaf': '🌿', 'book': '📚', 'korowai': '🪶', 'road': '🛣️', 'plane': '✈️', 'clock': '⏳',
        'tractor': '🚜', 'globe': '🌏', 'ballot': '🗳️'}


def host(u):
    if not u.startswith('http'):
        return u
    h = urlparse(u).netloc.replace('www.', '')
    return h


def link(u):
    if u.startswith('http'):
        return f'[{host(u)}]({u})'
    return f'[`{u}`](../{u})'


def links(us):
    seen, out = set(), []
    for u in us or []:
        if u not in seen:
            seen.add(u)
            out.append(link(u))
    return ', '.join(out)


def ids(xs):
    return ' '.join(f'`{x}`' for x in xs)


def poll_text(p):
    pa = p.get('polling_avg_2026') or {}
    if pa.get('average_pct') is not None:
        return (f"{pa['average_pct']}% (average of {pa['polls']} polls, {pa['window'].replace(' to ', '–')}; "
                f"range {pa['min_pct']}–{pa['max_pct']}%)")
    if pa.get('policy_nz_figure'):
        return f"not polled separately (policy.nz: {pa['policy_nz_figure']})"
    return 'not polled separately'


def short_poll(p):
    pa = p.get('polling_avg_2026') or {}
    if pa.get('average_pct') is not None:
        return f"{pa['average_pct']}%"
    return (pa['policy_nz_figure'] + ' (policy.nz)') if pa.get('policy_nz_figure') else '–'


def names(slugs):
    return ', '.join(BY[s]['short_name'] for s in slugs) or '–'


def anchor(p):
    return p['slug']


def parties_md():
    L = []
    A = L.append
    A('# The parties: a plain-English guide (2026 election)\n')
    A(f"*Election day: **Saturday 7 November 2026** (advance voting from 26 October). Information as at "
      f"**{guide['as_of']}**. Built from [`data/guide/parties.json`](../data/guide/parties.json) by "
      f"`tools/guide_render.py`; see also the [issues guide](issues.md).*\n")
    A(f"{guide['party_count_note']} Every party below gets the same template: what it is about, its headline "
      "2026 policies, its own pitch, the main criticism (attributed to a named source), and the facts. "
      "\"They say\" and \"critics say\" are other people's words, not ours. Each card links to the full policy "
      "list, profile and track record for anyone who wants to go deeper.\n")
    A('**How to read this:**')
    A('- **Position** is the left–right label in the party\'s English Wikipedia infobox (retrieved 23 Oct 2026); where '
      'there is none we say so. ' + '')
    A('- **Polling** is a simple average of all published polls in the 30 days to 23 October 2026 '
      '(data: [`data/polls-2026.json`](../data/polls-2026.json)). Small parties are not polled separately. '
      'A party needs **5% of the party vote or one electorate seat** to get list seats.')
    A('- **Policy ids** (like `POL54642`) point to the full entries in `parties/<party>/policies/` (policy.nz ids or ids '
      'assigned in this archive).')
    A('- Parties are listed by current seats in Parliament, then by polling, then alphabetically.\n')
    A('## At a glance\n')
    A('| Party | Leader(s) | Wikipedia position | Seats now | Polling (avg) | Says it could work with | Has ruled out |')
    A('|---|---|---|---|---|---|---|')
    for s in ORDER:
        p = BY[s]
        cs = p['coalition_stance_2026']
        pos = p['position']['label']
        if pos.startswith('no '):
            pos = '–'
        A(f"| [{p['short_name']}](#{anchor(p)}) | {', '.join(l['name'] for l in p['leaders'])} | {pos} | "
          f"{p['current_seats']['seats']} | {short_poll(p)} | {names(cs.get('open_to', []))} | "
          f"{names(cs.get('rules_out', []))} |")
    A('\n*Coalition columns summarise public statements up to the date shown on each card; "–" means we found no '
      'statement. See each card for wording and sources.*\n')
    for s in ORDER:
        p = BY[s]
        A(f'---\n\n<a id="{anchor(p)}"></a>\n## {p["short_name"]} — {p["name"]}\n')
        A(f"> {p['tagline']}\n")
        A(f"**In a nutshell:** {p['in_a_nutshell']}\n")
        A('**Big ideas for 2026:**\n')
        for b in p['big_ideas']:
            ref = ids(b['policy_ids']) if b.get('policy_ids') else f"({link(b['source'])})"
            A(f"- {b['text']} {ref}")
        ts, cr = p['they_say'], p['critics_say']
        A(f"\n**They say:** {ts['text']} — *{ts['attribution']}* ({links(ts.get('sources'))})\n")
        A(f"**Critics say:** {cr['text']} — *{cr['attribution']}*"
          + (f" ({links(cr.get('sources'))})" if cr.get('sources') else '') + '\n')
        pos = p['position']
        postxt = pos['label'] if not pos['label'].startswith('no ') else pos['label'] + ('. ' + pos.get('description', ''))
        cs = p['coalition_stance_2026']
        co = p['costings']
        seats = p['current_seats']
        A('| | |\n|---|---|')
        A(f"| **Leader(s)** | {', '.join(l['name'] + (' (' + l['role'] + ')' if l.get('role') else '') for l in p['leaders'])} |")
        A(f"| **Founded** | {p['founded']} |")
        A(f"| **Position (Wikipedia)** | {postxt} ({link(pos['source'])}) |")
        A(f"| **Seats now** | {seats['seats']} of {seats['of']}" + (f" — {seats['note']}" if seats.get('note') else '') + ' |')
        A(f"| **Polling** | {poll_text(p)} |")
        A(f"| **Coalition stance** | {cs['summary']} *(as at {cs['as_of']})*" + (f" {links(cs.get('sources'))}" if cs.get('sources') else '') + ' |')
        A(f"| **Costed fiscal plan?** | {co['summary']}" + (f" {links(co.get('sources'))}" if co.get('sources') else '') + ' |')
        A(f"| **Track record** | {p['track_record_line']} |")
        A(f"| **Website** | [{host(p['website'])}]({p['website']}) |")
        deeper = [f"[profile](../parties/{s}/README.md)", f"[all 2026 policies](../parties/{s}/policies/README.md)"]
        if p.get('track_record_file'):
            deeper.append(f"[track record](../{p['track_record_file']})")
        if p.get('policy_nz'):
            deeper.append(f"[policy.nz]({p['policy_nz']})")
        A(f"| **Go deeper** | {' · '.join(deeper)} |\n")
        if p.get('notes'):
            A(f"*Note: {p['notes']}*\n")
        A(f"<sub>Sources: {links(p['sources'])}</sub>\n")
    A('---\n')
    A(f"*Party count sources: {links(guide['party_count_sources'])}.*")
    return '\n'.join(L) + '\n'


def issues_md():
    L = []
    A = L.append
    A('# The big issues: where the parties stand (2026 election)\n')
    A(f"*Information as at **{issues['as_of']}**. Built from [`data/guide/issues.json`](../data/guide/issues.json) by "
      f"`tools/guide_render.py`; see also the [party guide](parties.md).*\n")
    A('Issues were chosen from what voters say matters most in the 2026 Ipsos Issues Monitor surveys '
      '(cost of living, healthcare, the economy, unemployment, housing, fuel prices, poverty, crime, climate, education, '
      'with tax rising) plus the areas where party platforms differ most. For each issue: why it matters, a few '
      'sourced facts, and a one- or two-sentence summary of each party\'s published 2026 policy. A party is left out '
      'of an issue when we found no 2026 position on it. Summaries describe what parties propose, not whether it would work.\n')
    A('## Issues\n')
    for i in issues['issues']:
        A(f"- {ICON.get(i['icon'], '')} [{i['title']}](#{i['slug']})")
    A('')
    for i in issues['issues']:
        A(f'---\n\n<a id="{i["slug"]}"></a>\n## {ICON.get(i["icon"], "")} {i["title"]}\n')
        A(f"**Why it matters:** {i['why_it_matters']}\n")
        A('**Key facts:**\n')
        for f in i['key_facts']:
            A(f"- {f['fact']} ({links(f['sources'])})")
        A('\n**Where the parties stand:**\n')
        A('| Party | What they propose |')
        A('|---|---|')
        for s in ORDER:
            pos = i['positions'].get(s)
            if not pos:
                continue
            ref = []
            if pos.get('policy_ids'):
                ref.append(ids(pos['policy_ids']))
            if pos.get('sources'):
                ref.append(links(pos['sources']))
            A(f"| [{BY[s]['short_name']}](parties.md#{s}) | {pos['summary']} <sub>{' '.join(ref)}</sub> |")
        missing = [BY[s]['short_name'] for s in ORDER if s not in i['positions']]
        if missing:
            A(f"\n<sub>No 2026 position found for: {', '.join(missing)}.</sub>")
        A('')
    A('---\n')
    A(f"*Issue-ranking sources: {links(issues['issue_ranking_sources'])}.*")
    return '\n'.join(L) + '\n'


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / 'parties.md').write_text(parties_md())
    (OUT / 'issues.md').write_text(issues_md())
    print('wrote guide/parties.md and guide/issues.md')


if __name__ == '__main__':
    main()

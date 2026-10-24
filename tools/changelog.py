#!/usr/bin/env python3
"""The "What changed this week" log (data/changes.json) and the RSS feed (site/feed.xml).

    python3 tools/changelog.py                 # compare the data with the last snapshot, append new entries, write
                                               # data/changes.json, site/data/changes.json and site/feed.xml
    python3 tools/changelog.py --feed          # only rewrite site/feed.xml + site/data/changes.json from data/changes.json
    python3 tools/changelog.py --site "Title" [--summary "..."] [--url "#/route"]   # record a change to the site itself

Run after tools/refresh_policies.py (and after the polls and releases updates have landed). It compares, against the
snapshot stored in data/changes.json (`_snapshot`, written at the end of every run):
- policies: every parties/*/policies/policies.json record (new id -> policy-added; new wording, summary or sources ->
  policy-changed; newly marked `withdrawn` -> policy-withdrawn);
- candidates: the policy.nz party lists and electorate pages in raw/policy.nz/ (new -> candidate-added; list place,
  electorate, candidacy or questionnaire answers changed, or no longer listed -> candidate-changed). Home suburbs and
  email addresses are never compared or quoted;
- polls: data/polls-2026.json, by fieldwork end date + pollster (poll-added);
- party releases: data/releases.json, by URL, ministerial releases left out (release; headline + link only, as the
  newsroom shows them).
The first run has no snapshot: it records a baseline and seeds the log from the polls and releases of the last 60 days.
Entries older than 60 days are dropped. Re-running without new data adds nothing (entries are keyed by `id`).

Election-day rule (Electoral Act 1993 s 197; see docs/LEGAL_REVIEW.md): the feed never carries a poll or party-release
item dated 7 November before 7pm NZDT, and a feed built from midnight 6 November until 7pm 7 November (the copy that is
served on polling day) carries no poll or party-release items at all. The page applies the same rule in the browser.
"""
import argparse, datetime, email.utils, hashlib, json, pathlib, re, sys
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from partymap import PNZ_TO_REPO   # noqa: E402

NZ = ZoneInfo('Pacific/Auckland')
OUT = ROOT / 'data' / 'changes.json'
SITE_OUT = ROOT / 'site' / 'data' / 'changes.json'
FEED = ROOT / 'site' / 'feed.xml'
SITE = 'https://not-simon.github.io/Politicsnz/'
WINDOW = 60
FEED_N = 50
REPO_TO_PNZ = {v: k for k, v in PNZ_TO_REPO.items()}
EDAY_START = datetime.datetime(2026, 11, 7, 0, 0, tzinfo=NZ)
EDAY_END = datetime.datetime(2026, 11, 7, 19, 0, tzinfo=NZ)
FREEZE_START = datetime.datetime(2026, 11, 6, 0, 0, tzinfo=NZ)
HIDDEN_ON_ELECTION_DAY = ('poll-added', 'release')
KIND_WORDS = {'policy-added': 'new policy', 'policy-changed': 'policy updated', 'policy-withdrawn': 'policy withdrawn',
              'candidate-added': 'new candidate', 'candidate-changed': 'candidate update', 'release': 'press release'}
PRIVATE_ATTRS = {'Residence', 'Public email'}   # never compared, never quoted (docs/LEGAL_REVIEW.md M8/S9)


def load(p, default=None):
    try:
        return json.loads(pathlib.Path(p).read_text())
    except Exception:
        return default


def h(o):
    return hashlib.sha1(json.dumps(o, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:10]


def ws(s):
    return re.sub(r'\s+', ' ', s or '').strip()


def clip(s, n=240):
    s = ws(s)
    return s if len(s) <= n else s[:n - 1].rsplit(' ', 1)[0].rstrip(',;:') + '…'


def cap(s):
    return s[:1].upper() + s[1:]


def long_date(iso):
    d = datetime.date.fromisoformat(iso[:10])
    return f'{d.day} {d:%b %Y}'


# ---------------------------------------------------------------- current state
def policies_state():
    out = {}
    for f in sorted((ROOT / 'parties').glob('*/policies/policies.json')):
        party = f.parent.parent.name
        for r in load(f, []) or []:
            if not r.get('id') or not r.get('statement'):
                continue
            sm = r.get('summary') or {}
            urls = sorted({s.get('url') for s in r.get('sources') or [] if s.get('url')})
            out.setdefault(party, {})[r['id']] = {
                's': ws(r['statement']), 'm': h([ws(sm.get('why')), ws(sm.get('how')), ws(sm.get('text'))]), 'u': h(urls),
                'w': r.get('withdrawn'), 'src': next((s.get('url') for s in r.get('sources') or [] if s.get('url')), None),
                'sum': clip(sm.get('how') or sm.get('why') or sm.get('text') or '')}
    return out


def candidates_state():
    raw = ROOT / 'raw' / 'policy.nz'
    titles = {}
    els = {f.stem: load(f, {}) for f in sorted((raw / 'electorates').glob('*.json'))}
    for d in els.values():
        e = (d or {}).get('election') or {}
        if e.get('slug'):
            titles[e['slug']] = (e.get('title') or '').replace(' electorate', '')
    out = {}

    def rec(ps, c):
        repo = PNZ_TO_REPO.get(ps, ps)
        k = f"{repo}/{c.get('slug')}"
        pj = load(ROOT / 'parties' / repo / 'people' / c.get('slug', '') / 'person.json', {}) or {}
        r = out.setdefault(k, {'party': repo, 'pnz': ps, 'name': pj.get('name') or f"{c.get('firstName', '')} {c.get('lastName', '')}".strip(),
                               'rank': None, 'el': None, 'desc': None, 'q': []})
        return r

    def answers(c):
        return [[a.get('name'), ws(a.get('value'))] for a in c.get('attributes') or [] if a.get('name') not in PRIVATE_ATTRS and a.get('value')]
    for f in sorted((raw / 'parties').glob('*.json')):
        d = load(f, {}) or {}
        ps = (d.get('party') or {}).get('slug') or f.stem
        for c in d.get('partyList') or []:
            r = rec(ps, c)
            pa = c.get('partyAffiliation') or {}
            if (pa.get('listRank') or '').strip().isdigit():
                r['rank'] = int(pa['listRank'])
            r['el'] = titles.get(c.get('electorateElectionSlug')) or r['el']
            r['desc'] = pa.get('candidacyDescription') or r['desc']
            r['q'].append(answers(c))
    for es, d in els.items():
        for c in ((d or {}).get('election') or {}).get('candidates') or []:
            per = c.get('person') or {}
            ps = (per.get('party') or {}).get('slug') or 'independent'
            r = rec(ps, per)
            r['el'] = titles.get(es) or r['el']
            pa = per.get('partyAffiliation') or {}
            r['desc'] = r['desc'] or pa.get('candidacyDescription')
            r['q'].append([answers(per), [[x.get('statement'), [[a.get('name'), ws(a.get('value'))] for a in x.get('attributes') or []]] for x in c.get('policies') or []]])
    for r in out.values():
        r['q'] = h(sorted(json.dumps(x, ensure_ascii=False, sort_keys=True) for x in r['q']))
    return out


def polls_state():
    d = load(ROOT / 'data' / 'polls-2026.json', {}) or {}
    L = d.get('polls', []) if isinstance(d, dict) else d
    out = {}
    for p in L or []:
        if p.get('is_election_result') or not p.get('end_date') or not p.get('pollster'):
            continue
        out[f"{p['end_date']}|{p['pollster']}"] = p
    return out


def releases_state():
    """Party releases by URL; the same headline posted twice on one day (Scoop sometimes does) counts once."""
    d = load(ROOT / 'data' / 'releases.json', {}) or {}
    out, seen = {}, set()
    for i in sorted(d.get('items') or [], key=lambda x: x.get('url') or ''):
        if not i.get('url') or not i.get('party') or i['party'] == 'government' or i.get('ministerial'):
            continue
        k = (i['party'], ws(i.get('title')).lower(), str(i.get('date'))[:10])
        if k in seen:
            continue
        seen.add(k)
        out[i['url']] = i
    return out


# ---------------------------------------------------------------- entries
def entry(kind, date, title, url, source, party=None, summary='', key=None, when=None, **extra):
    e = {'id': f"{kind}:{party or '-'}:{key or title}" + (f':{date}' if kind.endswith('-changed') else ''), 'date': date, 'kind': kind,
         'party': party, 'title': ws(title), 'summary': ws(summary), 'url': url, 'source': source}
    if when:
        e['time'] = when
    e.update({k: v for k, v in extra.items() if v is not None})
    return e


def policy_entries(prev, cur, today, now):
    out = []
    for party, pols in cur.items():
        before = prev.get(party, {})
        route = f'#/parties/{party}/policies'
        for pid, p in pols.items():
            o = before.get(pid)
            src = p['src'] or (f"https://policy.nz/2026/party-vote/parties/{REPO_TO_PNZ[party]}" if party in REPO_TO_PNZ else None)
            if o is None:
                if not p['w']:
                    out.append(entry('policy-added', today, p['s'], route, src, party, p['sum'], pid, now, ref=pid))
                continue
            if p['w'] and not o.get('w'):
                out.append(entry('policy-withdrawn', today, p['s'], route, f"https://policy.nz/2026/party-vote/parties/{REPO_TO_PNZ.get(party, party)}",
                                 party, 'No longer listed on policy.nz. It stays in this archive, marked withdrawn.', pid, now, ref=pid))
                continue
            what = []
            if o.get('w') and not p['w']:
                what.append('listed on policy.nz again')
            if o.get('s') != p['s']:
                what.append(f"reworded (was “{clip(o.get('s'), 120)}”)")
            if o.get('m') != p['m']:
                what.append('summary updated')
            if o.get('u') != p['u']:
                what.append('sources updated')
            if what:
                out.append(entry('policy-changed', today, p['s'], route, src, party, cap('; '.join(what) + '.'), pid, now, ref=pid))
    return out


def candidate_entries(prev, cur, today, now):
    out = []
    for k, c in cur.items():
        o = prev.get(k)
        route = f"#/parties/{c['party']}/people"
        src = f"https://policy.nz/2026/party-vote/parties/{c['pnz']}"
        if o is None:
            bits = [x for x in (c['desc'], f"list place {c['rank']}" if c['rank'] and not (c['desc'] or '').lower().startswith('list') else None) if x]
            out.append(entry('candidate-added', today, c['name'], route, src, c['party'], '; '.join(bits) + ('.' if bits else ''), k, now))
            continue
        what = []
        if o.get('rank') != c['rank']:
            what.append(f"list place {o.get('rank') or 'none'} → {c['rank'] or 'none'}")
        if o.get('el') != c['el']:
            what.append(f"electorate {o.get('el') or 'none'} → {c['el'] or 'none'}")
        if o.get('desc') != c['desc'] and o.get('el') == c['el']:
            what.append(f"now “{c['desc']}”" if c['desc'] else 'candidacy description removed')
        if o.get('q') != c['q']:
            what.append('updated their policy.nz answers')
        if what:
            out.append(entry('candidate-changed', today, c['name'], route, src, c['party'], cap('; '.join(what) + '.'), k, now))
    for k, o in prev.items():
        if k not in cur:
            out.append(entry('candidate-changed', today, o.get('name') or k, f"#/parties/{o.get('party')}/people",
                             f"https://policy.nz/2026/party-vote/parties/{o.get('pnz')}", o.get('party'),
                             'No longer listed on policy.nz (checked today).', k, now))
    return out


def poll_entry(k, p, date, now):
    bits = [f"Fieldwork {p.get('date') or long_date(p['end_date'])}"]
    if p.get('sample_size'):
        bits.append(f"{int(p['sample_size']):,} people")
    if p.get('internal'):
        bits.append('internal (party-commissioned) poll')
    return entry('poll-added', date, p['pollster'], '#/seats/polls', p.get('source_url'), None, ', '.join(bits) + '.', k, now, poll_date=p['end_date'])


def release_entry(i):
    d = str(i.get('date') or '')
    return entry('release', d[:10], i['title'], f"#/parties/news/{i['party']}", i['url'], i['party'], '', i['url'], d if 'T' in d else None,
                 via=i.get('source'))


# ---------------------------------------------------------------- outputs
def public(doc):
    return {k: v for k, v in doc.items() if not k.startswith('_snapshot')}


def party_names():
    m = (load(ROOT / 'data' / 'parties-meta.json', {}) or {}).get('parties', {})
    return {k: v.get('short') or v.get('name') or k for k, v in m.items()}


def feed_title(e, names):
    pn = names.get(e.get('party'), (e.get('party') or '').replace('-', ' ').title())
    if e['kind'] == 'poll-added':
        return f"New poll: {e['title']}, {long_date(e.get('poll_date') or e['date'])}"
    if e['kind'] == 'site':
        return f"Ballot Book: {e['title']}"
    return f"{pn}: {KIND_WORDS.get(e['kind'], e['kind'])} — {e['title']}"


def when_of(e):
    if e.get('time'):
        try:
            t = datetime.datetime.fromisoformat(e['time'])
            return t if t.tzinfo else t.replace(tzinfo=NZ)
        except ValueError:
            pass
    return datetime.datetime.fromisoformat(e['date'] + 'T12:00:00').replace(tzinfo=NZ)


def feed_entries(entries, now):
    out = []
    frozen = FREEZE_START <= now < EDAY_END
    for e in entries:
        if e['kind'] in HIDDEN_ON_ELECTION_DAY:
            if frozen:
                continue
            w = when_of(e)
            if EDAY_START <= w < EDAY_END or e['date'] == '2026-11-07' and now < EDAY_END:
                continue
        out.append(e)
    return out[:FEED_N]


def write_feed(doc, now):
    names = party_names()
    ATOM = 'http://www.w3.org/2005/Atom'
    ET.register_namespace('atom', ATOM)
    rss = ET.Element('rss', {'version': '2.0'})
    ch = ET.SubElement(rss, 'channel')
    for k, v in (('title', 'Ballot Book NZ — what changed'), ('link', SITE + '#/about/changes'),
                 ('description', 'New and changed 2026 election policies and candidates (from policy.nz), new opinion polls and party '
                                 'press releases, as picked up by Ballot Book NZ, an independent, non-partisan guide to the 7 November 2026 '
                                 'New Zealand general election. Every item links to its source.'),
                 ('language', 'en-nz'), ('lastBuildDate', email.utils.format_datetime(now)), ('ttl', '720'),
                 ('generator', 'tools/changelog.py')):
        ET.SubElement(ch, k).text = v
    ET.SubElement(ch, f'{{{ATOM}}}link', {'href': SITE + 'feed.xml', 'rel': 'self', 'type': 'application/rss+xml'})
    for e in feed_entries(doc['entries'], now):
        it = ET.SubElement(ch, 'item')
        ET.SubElement(it, 'title').text = feed_title(e, names)
        ET.SubElement(it, 'link').text = SITE + (e.get('url') or '#/about/changes')
        ET.SubElement(it, 'guid', {'isPermaLink': 'false'}).text = 'ballotbook:' + e['id']
        ET.SubElement(it, 'pubDate').text = email.utils.format_datetime(when_of(e))
        ET.SubElement(it, 'category').text = e['kind']
        desc = e.get('summary') or ('Headline as published by the party.' if e['kind'] == 'release' else '')
        if e.get('source'):
            desc = (desc + ' ' if desc else '') + f"Source: {e['source']}"
        ET.SubElement(it, 'description').text = desc
        if e.get('source'):
            ET.SubElement(it, 'source', {'url': e['source']}).text = e.get('via') or re.sub(r'^https?://(www\.)?([^/]+).*$', r'\2', e['source'])
    ET.indent(rss)
    data = ET.tostring(rss, encoding='utf-8', xml_declaration=True) + b'\n'
    ET.fromstring(data)          # must parse
    if not FEED.exists() or FEED.read_bytes() != data:
        FEED.write_bytes(data)
    return len(ch.findall('item'))


def write_outputs(doc, now):
    t = json.dumps(doc, ensure_ascii=False, indent=1) + '\n'
    if not OUT.exists() or OUT.read_text() != t:
        OUT.write_text(t)
    SITE_OUT.parent.mkdir(parents=True, exist_ok=True)
    s = json.dumps(public(doc), ensure_ascii=False, separators=(',', ':'))
    if not SITE_OUT.exists() or SITE_OUT.read_text() != s:
        SITE_OUT.write_text(s)
    return write_feed(doc, now)


def sort_key(e):
    return (e['date'], e.get('time') or '', e['kind'], e.get('party') or '', e['title'])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--feed', action='store_true', help='only rewrite site/feed.xml and site/data/changes.json')
    ap.add_argument('--site', help='record a change to the site itself (title)')
    ap.add_argument('--summary', default='')
    ap.add_argument('--url', default='#/today')
    ap.add_argument('--now', help='override the time (ISO 8601), for testing')
    a = ap.parse_args()
    now = datetime.datetime.fromisoformat(a.now).astimezone(NZ) if a.now else datetime.datetime.now(NZ)
    today, stamp = now.date().isoformat(), now.isoformat(timespec='seconds')
    doc = load(OUT, None) or {}
    doc.setdefault('entries', [])
    if a.feed:
        print('feed items', write_outputs(doc, now))
        return
    snap = doc.get('_snapshot')
    cur = {'policies': policies_state(), 'candidates': candidates_state(), 'polls': polls_state(), 'releases': releases_state()}
    new = []
    cutoff = (now.date() - datetime.timedelta(days=WINDOW)).isoformat()
    if a.site:
        new.append(entry('site', today, a.site, a.url, SITE + a.url, None, a.summary, None, stamp))
    if not snap:
        print(f"no previous snapshot: recorded a baseline of {sum(len(v) for v in cur['policies'].values())} policies and "
              f"{len(cur['candidates'])} candidates; seeded the log from the polls and party releases of the last {WINDOW} days")
        new += [poll_entry(k, p, p['end_date'], None) for k, p in cur['polls'].items() if p['end_date'] >= cutoff]
        new += [release_entry(i) for i in cur['releases'].values()]
        if not any(e['kind'] == 'site' for e in doc['entries'] + new):
            new.append(entry('site', today, 'New: “What changed this week” page and RSS feed', '#/about/changes', SITE + 'feed.xml', None,
                             'Policy and candidate changes on policy.nz, new polls and party releases in one list, updated daily.', 'changes-page', stamp))
    else:
        new += policy_entries(snap.get('policies', {}), cur['policies'], today, stamp)
        new += candidate_entries(snap.get('candidates', {}), cur['candidates'], today, stamp)
        seen_polls = set(snap.get('polls', []))
        new += [poll_entry(k, p, today, stamp) for k, p in cur['polls'].items() if k not in seen_polls]
        seen_rel = set(snap.get('releases', []))
        new += [release_entry(i) for u, i in cur['releases'].items() if u not in seen_rel]
    have = {e['id'] for e in doc['entries']}
    added = [e for e in new if e['id'] not in have and e['date'] >= cutoff]
    entries = sorted([e for e in doc['entries'] + added if e['date'] >= cutoff], key=sort_key, reverse=True)
    status = load(ROOT / 'raw' / 'policy.nz' / 'refresh-status.json', {}) or {}
    out = {'_about': 'What changed: new and changed policies and candidates (policy.nz), new polls and party releases, newest first. '
                     f'Built by tools/changelog.py; last {WINDOW} days. Release entries are headline + link only. `_snapshot` is the '
                     'state the next run compares against (not published to the site).',
           'updated': stamp if added or not doc.get('updated') else doc['updated'], 'window_days': WINDOW,
           'policy_nz_checked': status.get('checked'), 'policy_nz_failures': len(status.get('requests_failed') or []),
           'counts': {k: sum(1 for e in entries if e['kind'] == k) for k in sorted({e['kind'] for e in entries})},
           'entries': entries,
           '_snapshot': {'taken': stamp, 'policies': {pa: {i: {k: v for k, v in r.items() if k in 'smuw'} for i, r in ps.items()} for pa, ps in cur['policies'].items()}, 'candidates': cur['candidates'],
                         'polls': sorted(cur['polls']), 'releases': sorted(cur['releases'])}}
    n = write_outputs(out, now)
    by = {}
    for e in added:
        by[e['kind']] = by.get(e['kind'], 0) + 1
    print(f'changes: {len(added)} new entries {by or ""}; {len(entries)} in the last {WINDOW} days; feed items {n}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Daily refresh of the 2026 policy.nz data: party policies, party lists and electorate candidates.

    python3 tools/refresh_policies.py              # fetch policy.nz, update raw/ + parties/, record what changed
    python3 tools/refresh_policies.py --dry-run    # fetch and report only; write nothing
    python3 tools/refresh_policies.py --offline    # no network: re-apply the cached raw/policy.nz data (reconcile)
    python3 tools/refresh_policies.py --from-dir D # use the policy.nz JSON in D (same layout as raw/policy.nz) as "new"

What it does (a thin wrapper around the original tools, not a second copy of them):
1. Fetches the same Next.js `__NEXT_DATA__` pages tools/scrape_policynz.py downloads (one party page for the election
   object with every party's policies, then each party page for its list, the electorates index and each electorate
   page for its candidates), with the same User-Agent, one request at a time and a pause between requests.
   A page that fails (after retries) or comes back implausibly empty keeps the previously stored copy, and the failure is
   logged in raw/policy.nz/refresh-status.json. A party whose policy count falls by more than half in one run is treated
   as a bad fetch (kept as it was, logged) unless --allow-mass-withdrawal is given.
2. Writes the fresh pages to raw/policy.nz/ in the original layout and format.
3. Merges the policy changes into parties/<party>/policies/policies.json (repo slugs via tools/partymap.py):
   - a new policy.nz policy is appended with policy.nz's summary, its citations as source links, `has_fulltext: false`
     and `added: <date>` (full texts are archived by the separate document tools, not here);
   - a changed policy gets the new policy.nz text where the archive still held policy.nz's old text (hand-edited
     statements are kept, the new wording is stored as `policy_nz_statement`), new topics and citations, and a
     `changes` history entry with the previous wording;
   - a policy that disappeared from policy.nz is never deleted: it is marked `withdrawn: <date>` (and un-marked, with
     `reinstated: <date>`, if it comes back).
   Then it rewrites a generated "Changes on policy.nz since 23 October" block in parties/<party>/policies/README.md
   (between <!-- GENERATED:policy-updates START/END --> markers; the rest of the README is never touched).
4. Candidates: for every candidate whose policy.nz record is new or changed, runs tools/build_candidates.py (in a
   scratch copy, so nothing else is rewritten) and copies back that candidate's person.json / README.md / photo.jpg,
   keeping a hand-corrected display name. A candidate no longer listed anywhere on policy.nz is kept and marked
   `policy_nz_unlisted: <date>`.
Idempotent: a run that finds nothing new changes no file except the timestamp in refresh-status.json.
tools/changelog.py turns the result into data/changes.json and site/feed.xml.
"""
import argparse, datetime, json, pathlib, re, shutil, subprocess, sys, tempfile, time, urllib.request
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / 'raw' / 'policy.nz'
sys.path.insert(0, str(ROOT / 'tools'))
from partymap import PNZ_TO_REPO                     # noqa: E402
import policies_minor_lib as L                       # noqa: E402  (write_json: the archive's policies.json format)
from policies_minor_build import GROUP_NAMES         # noqa: E402

UA = {'User-Agent': 'Mozilla/5.0 (PoliticsNZ personal research archive)'}   # as tools/scrape_policynz.py
BASE = 'https://policy.nz'
PAUSE = 1.5            # seconds between requests (one at a time)
NZ = ZoneInfo('Pacific/Auckland')
START, END = '<!-- GENERATED:policy-updates START -->', '<!-- GENERATED:policy-updates END -->'
CAPTURED = '23 October 2026'
log = []


def say(*a):
    print(*a, file=sys.stderr)


# ---------------------------------------------------------------- fetching
def page(path, tries=3):
    """pageProps of a policy.nz page, or None (logged)."""
    err = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(BASE + path, headers=UA)
            h = urllib.request.urlopen(req, timeout=45).read().decode('utf-8')
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S)
            if not m:
                raise ValueError('no __NEXT_DATA__ in page')
            return json.loads(m.group(1))['props']['pageProps']
        except Exception as e:      # network, HTTP, parse
            err = e
            time.sleep(PAUSE * 2 ** (attempt + 1))
        finally:
            time.sleep(PAUSE)
    log.append({'path': path, 'error': str(err)[:200]})
    say('FAILED', path, err)
    return None


def load(p, default=None):
    try:
        return json.loads(pathlib.Path(p).read_text())
    except Exception:
        return default


def canon(o):
    """Content only: policy.nz's CMS ids (_key/_ref) are regenerated on every publish, list order varies between page
    loads, and each electorate is reached through a randomly chosen candidate's page (index `path`, `candidateSlug`),
    so none of these counts as a change. (Fetching always uses the freshly read index.)"""
    if isinstance(o, dict):
        return {k: canon(v) for k, v in o.items() if k not in ('_key', '_ref', 'path', 'candidateSlug')}
    if isinstance(o, list):
        return sorted((canon(v) for v in o), key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False))
    return o


def dump_raw(p, obj):
    """Same format as tools/scrape_policynz.py; returns True if the file changed. A page whose content is unchanged
    (only ids or order differ) keeps the stored file byte-for-byte."""
    t = json.dumps(obj, ensure_ascii=False, indent=1)
    if p.exists() and (p.read_text() == t or canon(load(p)) == canon(obj)):
        return False
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t)
    return True


def read_raw(d):
    """{'election', 'parties': {slug: file}, 'index', 'electorates': {slug: file}} from a raw/policy.nz-style dir."""
    d = pathlib.Path(d)
    return {'election': load(d / 'party-vote-election.json'),
            'parties': {f.stem: load(f) for f in sorted((d / 'parties').glob('*.json'))},
            'index': load(d / 'elections-index.json'),
            'electorates': {f.stem: load(f) for f in sorted((d / 'electorates').glob('*.json'))}}


def fetch_all(old, allow_mass):
    """Fetch every page; anything that fails keeps its old copy. Returns the 'new' structure + per-source status."""
    new = {'election': None, 'parties': {}, 'index': None, 'electorates': {}}
    status = {'kept_old': [], 'suspect': []}
    order = ['national-party'] + [s for s in (old['parties'] or {}) if s != 'national-party']
    pages = {}
    for slug in order:   # the election object (all parties + all policies) is embedded in every party page
        pp = page(f'/2026/party-vote/parties/{slug}')
        if pp:
            pages[slug] = pp
        if pp and (pp.get('election') or {}).get('parties'):
            new['election'] = pp['election']
            break
    if not new['election']:
        new['election'] = old['election']
        status['kept_old'].append('party-vote-election.json (no party page could be read)')
    old_el = {p['party']['slug']: p for p in (old['election'] or {}).get('parties', [])}
    for p in new['election']['parties']:
        slug = p['party']['slug']
        o = old['parties'].get(slug) or {}
        pols = p.get('policies') or []
        n_old = len(o.get('policies') or [])
        if n_old >= 10 and len(pols) < n_old * 0.5 and not allow_mass:
            status['suspect'].append(f'{slug}: {n_old} -> {len(pols)} policies; kept the stored list')
            pols = o.get('policies') or []
            p['policies'] = pols
        pp = pages.get(slug) or page(f'/2026/party-vote/parties/{slug}')
        plist = (pp or {}).get('partyList')
        if pp is None or (not plist and o.get('partyList')):
            if pp is not None:
                status['suspect'].append(f'{slug}: empty party list; kept the stored list')
            plist = o.get('partyList')
            status['kept_old'].append(f'parties/{slug}.json partyList')
        new['parties'][slug] = {'party': p['party'], 'policies': pols, 'partyList': plist}
    for slug, o in old['parties'].items():   # a party that vanished from policy.nz entirely: keep its file
        if slug not in new['parties']:
            status['suspect'].append(f'{slug}: no longer in the policy.nz party list; kept the stored file')
            new['parties'][slug] = o
            if slug in old_el:
                new['election']['parties'].append(old_el[slug])
    els = page('/2026/elections')
    new['index'] = (els or {}).get('groupedElections') or old['index']
    if not els:
        status['kept_old'].append('elections-index.json')
    for e in (new['index'] or {}).get('elections', []):
        ep = page(e['path'])
        o = old['electorates'].get(e['slug'])
        ok = ep and (ep.get('election') or {}).get('slug') == e['slug']
        if ok and o and not ep['election'].get('candidates') and o['election'].get('candidates'):
            ok = False
            status['suspect'].append(f"{e['slug']}: no candidates; kept the stored page")
        if ok:
            new['electorates'][e['slug']] = ep
        elif o:
            new['electorates'][e['slug']] = o
            status['kept_old'].append(f"electorates/{e['slug']}.json")
    for slug, o in old['electorates'].items():
        new['electorates'].setdefault(slug, o)
    return new, status


def write_raw(new):
    changed = []
    if dump_raw(RAW / 'party-vote-election.json', new['election']):
        changed.append('party-vote-election.json')
    for slug, d in new['parties'].items():
        if dump_raw(RAW / 'parties' / f'{slug}.json', d):
            changed.append(f'parties/{slug}.json')
    if new['index'] and dump_raw(RAW / 'elections-index.json', new['index']):
        changed.append('elections-index.json')
    for slug, d in new['electorates'].items():
        if dump_raw(RAW / 'electorates' / f'{slug}.json', d):
            changed.append(f'electorates/{slug}.json')
    return changed


# ---------------------------------------------------------------- policies
def orig_url(u):
    """policy.nz cites archived copies; the archive links the original (as tools/policies_minor_build.py does)."""
    o = re.sub(r'^https?://web\.archive\.org/(web/\d+[a-z_]*|save)/', '', u or '')
    return re.sub(r'^/web/\d+[a-z_]*/', '', o).rstrip('/')


def ws(s):
    """Whitespace normalised only (the original builds collapsed policy.nz's double spaces)."""
    return re.sub(r'\s+', ' ', s or '').strip()


def attrs(p):
    return {a.get('name'): ws(a.get('value')) for a in p.get('attributes') or []}


def fp(p):
    """What counts as a change in a policy.nz policy (ignores policy.nz's internal _key ids)."""
    a = attrs(p)
    return json.dumps([ws(p.get('statement')), a.get('Why', ''), a.get('How', ''), sorted(set(p.get('topics') or [])),
                       sorted((c.get('url') or '', (c.get('title') or '').strip()) for c in p.get('citations') or [])], ensure_ascii=False)


def plain_topics(p):
    return [t for t in dict.fromkeys(p.get('topics') or []) if not t.startswith('key-policies-')]


def main_group(p, groups):
    t = p.get('topics') or []
    return next((x[len('key-policies-'):] for x in t if x.startswith('key-policies-')), None) or next((x for x in t if x in groups), None) \
        or 'community-and-inclusion'


def cite_sources(p):
    out, seen = [], set()
    for c in p.get('citations') or []:
        u = orig_url(c.get('url'))
        if not u or u in seen:
            continue
        seen.add(u)
        s = {'title': ws(c.get('title') or u), 'url': u, 'cited_by': 'policy.nz'}
        if c.get('url') and c['url'] != u and c['url'].startswith('http'):
            s['archived_url'] = c['url']
        out.append(s)
    return out


def group_field(records, groups):
    """The party's own grouping field (each original build used a different one) and whether it holds slugs or names."""
    for k in ('topic_group', 'primary_topic', 'primary_group', 'group'):
        vals = [r[k] for r in records if r.get(k)]
        if vals:
            return k, all(v in groups for v in vals)
    return 'topic_group', True


def new_record(p, pnz_slug, records, groups, today):
    gk, slugs = group_field(records, groups)
    g = main_group(p, groups)
    a = attrs(p)
    rec = {'id': p['reference'], 'statement': ws(p.get('statement')), 'topics': plain_topics(p),
           gk: g if slugs else GROUP_NAMES.get(g, g)}
    if not records or any('key_policy' in r for r in records):
        rec['key_policy'] = any(t.startswith('key-policies-') for t in p.get('topics') or [])
    rec['summary'] = {'why': a.get('Why') or None, 'how': a.get('How') or None}
    rec['summary_source'] = 'policy.nz'
    rec['sources'] = cite_sources(p) + [{'title': 'policy.nz party page', 'url': f'{BASE}/2026/party-vote/parties/{pnz_slug}', 'cited_by': 'policy.nz'}]
    rec['has_fulltext'] = False
    rec['added'] = today
    return rec


def update_record(rec, old, new, today):
    """Apply a policy.nz change to an archive record. Returns the list of fields that changed."""
    what, prev = [], {}
    so, sn = ws(old.get('statement')), ws(new.get('statement'))
    if so != sn:
        what.append('statement')
        if ws(rec.get('statement')) == so:
            prev['statement'] = so
            rec['statement'] = sn
            rec.pop('policy_nz_statement', None)
        else:                       # the archive had reworded it by hand: keep that, store policy.nz's new wording
            rec['policy_nz_statement'] = sn
    ao, an = attrs(old), attrs(new)
    if rec.get('summary_source') == 'policy.nz':
        sm = rec.setdefault('summary', {})
        for k, nk in (('why', 'Why'), ('how', 'How')):
            if ao.get(nk, '') != an.get(nk, ''):
                what.append(k)
                if ws(sm.get(k)) in ('', ao.get(nk, '')):
                    prev[k] = sm.get(k)
                    sm[k] = an.get(nk) or None
                    (rec.get('policy_nz_summary') or {}).pop(k, None)
                else:               # the archive's summary was edited: keep it, store policy.nz's new text beside it
                    rec.setdefault('policy_nz_summary', {})[k] = an.get(nk) or None
        if rec.get('policy_nz_summary') == {}:
            rec.pop('policy_nz_summary')
    to, tn = set(plain_topics(old)), plain_topics(new)
    if to != set(tn):
        what.append('topics')
        rec['topics'] = [t for t in rec.get('topics') or [] if t not in to - set(tn)] + [t for t in tn if t not in (rec.get('topics') or [])]
        if 'key_policy' in rec:
            rec['key_policy'] = any(t.startswith('key-policies-') for t in new.get('topics') or [])
    have = {orig_url(v) for s in rec.get('sources') or [] for k, v in s.items() if isinstance(v, str) and v.startswith(('http', '/web/'))}
    added = [s for s in cite_sources(new) if s['url'] not in have]
    if added:
        what.append('sources')
        rec.setdefault('sources', []).extend(added)     # sources are only ever added, never removed
    if what:
        rec['policy_nz_updated'] = today
        rec.setdefault('changes', []).append({'date': today, 'fields': what, **({'previous': prev} if prev else {})})
    return what


def is_pnz_record(rec):
    return rec.get('summary_source') == 'policy.nz' and re.match(r'^POL\d+$', str(rec.get('id') or ''))


def apply_policies(old, new, ok_parties, today, write=True):
    groups = (new['election'] or old['election'] or {}).get('topicsList') or list(GROUP_NAMES)
    report = {}
    for slug, d in sorted(new['parties'].items()):
        if slug not in ok_parties:
            continue
        repo = PNZ_TO_REPO.get(slug, slug)
        pj = ROOT / 'parties' / repo / 'policies' / 'policies.json'
        records = load(pj, []) or []
        before = json.dumps(records, ensure_ascii=False, indent=1)
        by_id = {r.get('id'): r for r in records}
        old_by = {p['reference']: p for p in (old['parties'].get(slug) or {}).get('policies') or [] if p.get('reference')}
        new_by = {p['reference']: p for p in d.get('policies') or [] if p.get('reference')}
        if not records and not new_by:
            continue
        ev = {'added': [], 'changed': [], 'withdrawn': [], 'reinstated': []}
        for ref, p in new_by.items():
            rec = by_id.get(ref)
            if rec is None:
                rec = new_record(p, slug, records, groups, today)
                records.append(rec)
                by_id[ref] = rec
                ev['added'].append(ref)
                continue
            if rec.get('withdrawn'):
                rec['reinstated'] = today
                rec.setdefault('changes', []).append({'date': today, 'fields': ['reinstated'], 'previous': {'withdrawn': rec.pop('withdrawn')}})
                ev['reinstated'].append(ref)
            if ref in old_by and fp(old_by[ref]) != fp(p):
                w = update_record(rec, old_by[ref], p, today)
                if w:
                    ev['changed'].append([ref, w])
        for rec in records:
            rid = rec.get('id')
            if rid not in new_by and (rid in old_by or is_pnz_record(rec)) and not rec.get('withdrawn'):
                rec['withdrawn'] = today
                ev['withdrawn'].append(rid)
        after = json.dumps(records, ensure_ascii=False, indent=1)
        if any(ev.values()):
            report[repo] = ev
        if write and after != before:
            L.write_json(repo, records)
        if write:
            write_readme_block(repo, records)
    return report


def nzdate(iso):
    d = datetime.date.fromisoformat(iso[:10])
    return f'{d.day} {d:%B %Y}'


def write_readme_block(repo, records):
    rp = ROOT / 'parties' / repo / 'policies' / 'README.md'
    added = [r for r in records if r.get('added') and not r.get('withdrawn')]
    changed = [r for r in records if r.get('policy_nz_updated') and not r.get('added') and not r.get('withdrawn')]
    gone = [r for r in records if r.get('withdrawn')]
    back = [r for r in records if r.get('reinstated') and not r.get('withdrawn')]
    txt = rp.read_text() if rp.exists() else f'# {repo} — 2026 election policies\n'
    if not (added or changed or gone or back):
        if START in txt:
            rp.write_text(re.sub(r'\n*' + re.escape(START) + '.*?' + re.escape(END) + r'\n*', '\n\n', txt, flags=re.S))
        return
    def srcs(r):
        out = []
        for s in r.get('sources') or []:
            if s.get('document'):
                out.append(f"[{s.get('title') or 'document'}]({s['document']})" + (f" ([original]({s['url']}))" if s.get('url') else ''))
            elif s.get('url'):
                out.append(f"[{s.get('title') or s['url']}]({s['url']})")
        return '; '.join(out) or '_none recorded_'
    def summ(r):
        sm = r.get('summary') or {}
        tag = 'policy.nz' if r.get('summary_source') == 'policy.nz' else 'archive'
        return ([f"**Why** (*{tag}*): {sm['why'].strip()}", ''] if sm.get('why') else []) + ([f"**How** (*{tag}*): {sm['how'].strip()}", ''] if sm.get('how') else [])
    B = [START, f'## Changes on policy.nz since {CAPTURED}', '',
         f'This archive captured the party\'s policy.nz policies on {CAPTURED}; policy.nz is re-checked daily by '
         '[`tools/refresh_policies.py`](../../../tools/refresh_policies.py). Nothing is deleted: a policy that is no longer on '
         'policy.nz stays in this archive marked *withdrawn*. Full texts of new sources are archived separately; until then the '
         'links go to the original pages. Where this block and the sections below differ, this block is the newer text.', '']
    if added:
        B += ['### New policies', '']
        for r in added:
            B += [f"#### {r['statement']} ({r['id']})", '', f"_Added on policy.nz, first seen {nzdate(r['added'])}._", ''] + summ(r) + \
                 [f'Sources: {srcs(r)}. Full text not yet archived.', '']
    if changed or back:
        B += ['### Updated policies', '']
        for r in sorted({id(x): x for x in changed + back}.values(), key=lambda x: x.get('policy_nz_updated') or x.get('reinstated') or ''):
            last = (r.get('changes') or [{}])[-1]
            what = ', '.join(last.get('fields') or [])
            B += [f"#### {r['statement']} ({r['id']})", '', f"_Updated on policy.nz, seen {nzdate(last.get('date') or r.get('policy_nz_updated') or r.get('reinstated'))}: {what}._", '']
            if r.get('policy_nz_statement'):
                B += [f"policy.nz now words it: \"{r['policy_nz_statement']}\"", '']
            prevst = (last.get('previous') or {}).get('statement')
            if prevst:
                B += [f'Previously: "{prevst}"', '']
            B += summ(r)
            for k, v in (r.get('policy_nz_summary') or {}).items():
                if v:
                    B += [f"policy.nz's updated **{k.title()}** text: {v}", '']
            B += [f'Sources: {srcs(r)}', '']
    if gone:
        B += ['### Withdrawn (no longer on policy.nz)', '']
        B += [f"- {r['statement']} ({r['id']}) — not listed on policy.nz from {nzdate(r['withdrawn'])}. Kept here for the record." for r in gone]
        B.append('')
    B.append(END)
    block = '\n'.join(B)
    if START in txt:
        out = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda m: block, txt, flags=re.S)
    else:   # before the first section heading, after the title and introduction
        m = re.search(r'^## ', txt, re.M)
        out = (txt[:m.start()] + block + '\n\n' + txt[m.start():]) if m else txt.rstrip() + '\n\n' + block + '\n'
    if out != txt:
        rp.write_text(out)


# ---------------------------------------------------------------- candidates
def cand_index(raw):
    """(pnz party slug, person slug) -> canonical JSON of everything tools/build_candidates.py reads for that person."""
    out = {}
    for ps, d in (raw['parties'] or {}).items():
        for c in (d or {}).get('partyList') or []:
            out.setdefault((ps, c['slug']), []).append(['list', c])
    for es, d in sorted((raw['electorates'] or {}).items()):
        for c in ((d or {}).get('election') or {}).get('candidates') or []:
            per = c.get('person') or {}
            ps = (per.get('party') or {}).get('slug') or 'independent'
            out.setdefault((ps, per.get('slug')), []).append(['electorate', es, per, c.get('policies')])
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in o.items() if k != '_key'}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    return {k: json.dumps(strip(v), ensure_ascii=False, sort_keys=True) for k, v in out.items()}


def cand_names(raw):
    """policy.nz's own 'First Last' for each candidate (to tell a hand-corrected name from policy.nz's)."""
    out = {}
    for ps, d in (raw['parties'] or {}).items():
        for c in (d or {}).get('partyList') or []:
            out[(ps, c['slug'])] = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
    for d in (raw['electorates'] or {}).values():
        for c in ((d or {}).get('election') or {}).get('candidates') or []:
            per = c.get('person') or {}
            out.setdefault(((per.get('party') or {}).get('slug') or 'independent', per.get('slug')), f"{per.get('firstName', '')} {per.get('lastName', '')}".strip())
    return out


def apply_candidates(old, new, ok, today, write=True):
    oi, ni = cand_index(old), cand_index(new)
    names = cand_names(old)
    touched = sorted(k for k in ni if oi.get(k) != ni[k])
    gone = sorted(k for k in oi if k not in ni)
    rep = {'new_or_changed': [f'{PNZ_TO_REPO.get(p, p)}/{s}' for p, s in touched], 'unlisted': []}
    if not write:
        rep['unlisted'] = [f'{PNZ_TO_REPO.get(p, p)}/{s}' for p, s in gone]
        return rep
    if touched:
        with tempfile.TemporaryDirectory() as td:
            td = pathlib.Path(td)
            (td / 'tools').mkdir()
            for f in ('build_candidates.py', 'partymap.py'):
                shutil.copy(ROOT / 'tools' / f, td / 'tools' / f)
            shutil.copytree(RAW, td / 'raw' / 'policy.nz')
            for pd in (ROOT / 'parties').iterdir():
                if (pd / 'people').is_dir():
                    shutil.copytree(pd / 'people', td / 'parties' / pd.name / 'people')
            r = subprocess.run([sys.executable, str(td / 'tools' / 'build_candidates.py')], capture_output=True, text=True, timeout=1800)
            if r.returncode:
                log.append({'path': 'tools/build_candidates.py', 'error': r.stderr[-400:]})
                say(r.stderr)
                return rep
            for ps, slug in touched:
                party = PNZ_TO_REPO.get(ps, ps)
                src, dst = td / 'parties' / party / 'people' / slug, ROOT / 'parties' / party / 'people' / slug
                if not (src / 'person.json').exists():
                    continue
                pj = load(src / 'person.json', {})
                ex = load(dst / 'person.json', None)
                if ex:
                    # keep a display name corrected by hand (build_candidates.py would reset it to policy.nz's)
                    old_name = names.get((ps, slug))
                    if ex.get('name') and ex.get('name') != old_name:
                        pj['name'] = ex['name']
                    pj.pop('policy_nz_unlisted', None)
                    pj = {**{k: pj[k] for k in ex if k in pj}, **{k: v for k, v in pj.items() if k not in ex}}   # keep key order
                dst.mkdir(parents=True, exist_ok=True)
                t = json.dumps(pj, ensure_ascii=False, indent=1)
                if not (dst / 'person.json').exists() or (dst / 'person.json').read_text() != t:
                    (dst / 'person.json').write_text(t)
                for f in ('README.md', 'photo.jpg'):
                    if (src / f).exists() and (not (dst / f).exists() or (dst / f).read_bytes() != (src / f).read_bytes()):
                        shutil.copy(src / f, dst / f)
    for ps, slug in gone:
        if ps not in ok:      # only when that party's pages were actually read this run
            continue
        dst = ROOT / 'parties' / PNZ_TO_REPO.get(ps, ps) / 'people' / slug / 'person.json'
        pj = load(dst, None)
        if pj and not pj.get('policy_nz_unlisted'):
            pj['policy_nz_unlisted'] = today
            dst.write_text(json.dumps(pj, ensure_ascii=False, indent=1))
            rep['unlisted'].append(f'{PNZ_TO_REPO.get(ps, ps)}/{slug}')
    return rep


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--offline', action='store_true', help='do not fetch; re-apply raw/policy.nz')
    ap.add_argument('--from-dir', help='read "new" policy.nz data from this directory instead of fetching')
    ap.add_argument('--allow-mass-withdrawal', action='store_true')
    ap.add_argument('--today', help='override the NZ date (YYYY-MM-DD), for testing')
    a = ap.parse_args()
    now = datetime.datetime.now(NZ)
    today = a.today or now.date().isoformat()
    old = read_raw(RAW)
    if not old['election']:
        raise SystemExit('raw/policy.nz/party-vote-election.json is missing: run tools/scrape_policynz.py once first.')
    if a.offline:
        new, status = read_raw(RAW), {'kept_old': [], 'suspect': []}
    elif a.from_dir:
        new, status = read_raw(a.from_dir), {'kept_old': [], 'suspect': []}
        for k in ('parties', 'electorates'):
            for s, v in old[k].items():
                new[k].setdefault(s, v)
        new['election'] = new['election'] or old['election']
        new['index'] = new['index'] or old['index']
    else:
        new, status = fetch_all(old, a.allow_mass_withdrawal)
    # parties whose policies we trust this run (fetched, or supplied): everything not kept-old or suspect
    bad = {s.split(':')[0] for s in status['suspect']} | ({p for p in new['parties']} if any('party-vote-election' in k for k in status['kept_old']) else set())
    ok = {s for s in new['parties'] if s not in bad}
    raw_changed = [] if a.dry_run else write_raw(new)
    pol = apply_policies(old, new, ok, today, write=not a.dry_run)
    cand = apply_candidates(old, new, {s for s in ok if f'parties/{s}.json partyList' not in status['kept_old']}, today, write=not a.dry_run)
    out = {'checked': now.isoformat(timespec='seconds'), 'date': today, 'mode': 'offline' if a.offline else 'dir' if a.from_dir else 'live',
           'requests_failed': log, 'kept_previous': status['kept_old'], 'suspect': status['suspect'], 'raw_files_changed': raw_changed,
           'policies': pol, 'candidates': cand,
           'counts': {s: len(d.get('policies') or []) for s, d in sorted(new['parties'].items())}}
    if not a.dry_run:
        (RAW / 'refresh-status.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    n = {k: sum(len(v[k]) for v in pol.values()) for k in ('added', 'changed', 'withdrawn', 'reinstated')}
    print(f"policy.nz refresh {today} ({out['mode']}): policies +{n['added']} new, {n['changed']} changed, {n['withdrawn']} withdrawn, "
          f"{n['reinstated']} reinstated; candidates {len(cand['new_or_changed'])} new/changed, {len(cand['unlisted'])} unlisted; "
          f"{len(raw_changed)} raw files changed; {len(log)} failed requests; {len(status['suspect'])} suspect sources")
    for repo, ev in pol.items():
        print(' ', repo, {k: v for k, v in ev.items() if v})
    if log or status['suspect']:
        print('  see raw/policy.nz/refresh-status.json for failures (old data kept for those sources)')


if __name__ == '__main__':
    main()

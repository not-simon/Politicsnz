#!/usr/bin/env python3
"""Refresh the poll series from Wikipedia's "Opinion polling for the <year> New Zealand general election" articles.

Usage:
  python3 tools/polls_update.py              # 2026 series + historical 2011-2023 (only re-fetches history if missing)
  python3 tools/polls_update.py --history    # force re-fetch of the historical articles too
  python3 tools/polls_update.py --offline    # re-parse the cached HTML in raw/forecast/ without any network access

Outputs (all idempotent - running twice produces identical files):
  data/polls-2026.json             merged: existing rows are preserved field-by-field, new Wikipedia rows appended,
                                   plus `pollsters` metadata, `electorate_polls` and `events`
  data/polls-history/<year>.json   2011, 2014, 2017, 2020, 2023 party-vote poll series + the official result,
                                   used by tools/forecast.py to calibrate polling error empirically
  raw/forecast/wiki_<year>.html    cached article HTML (gitignored) + raw/forecast/wiki_<year>.meta.json (revid, retrieved)

Why Wikipedia: it is the only place where every public NZ poll (1News-Verian, RNZ-Reid Research, Taxpayers' Union-Curia,
Roy Morgan, The Post/Freshwater Strategy, Talbot Mills, Anacta, ...) is tabulated with fieldwork dates, sample sizes and a
link to the pollster's or publisher's own release. We keep that source link on every row so each number can be checked.
The MediaWiki API is rate limited: requests are spaced out and retried, and a failed fetch leaves the existing files untouched.
"""
import argparse, datetime as dt, json, os, re, sys, time, urllib.request, urllib.parse
from bs4 import BeautifulSoup

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
RAW = os.path.join(ROOT, "raw", "forecast")
HIST_DIR = os.path.join(ROOT, "data", "polls-history")
OUT_2026 = os.path.join(ROOT, "data", "polls-2026.json")
UA = "PoliticsNZResearch/1.0 (personal research; polls_update.py)"
API = "https://en.wikipedia.org/w/api.php"
YEARS_HISTORY = [2011, 2014, 2017, 2020, 2023]
ELECTION_DATES = {2008: "2008-11-08", 2011: "2011-11-26", 2014: "2014-09-20", 2017: "2017-09-23",
                  2020: "2020-10-17", 2023: "2023-10-14", 2026: "2026-11-07"}

# Column header (as rendered, lower-cased, footnote markers stripped) -> party slug used across this repo.
PARTY_COLS = {
    "nat": "national", "national": "national",
    "lab": "labour", "labour": "labour",
    "grn": "green", "green": "green", "greens": "green",
    "act": "act",
    "nzf": "nz-first", "nz first": "nz-first", "nzfirst": "nz-first",
    "tpm": "te-pati-maori", "mri": "te-pati-maori", "māori": "te-pati-maori", "maori": "te-pati-maori", "māori party": "te-pati-maori",
    "opp": "opportunity", "top": "opportunity", "opportunities": "opportunity", "opportunity": "opportunity",
    "unf": "united-future", "united future": "united-future",
    "con": "conservative", "ncp": "conservative", "conservative": "conservative", "new conservative": "conservative",
    "mna": "mana", "mana": "mana", "internet mana": "internet-mana", "internet": "internet-party",
    "prog": "progressive", "progressive": "progressive",
    "anz": "advance-nz", "advance nz": "advance-nz",
    "ttt": "te-tai-tokerau-party", "ind": "independent", "others": "others", "other": "others",
}
NON_PARTY_COLS = {"date", "poll", "polling organisation", "sample size", "lead", "", "margin"}

# Who commissions / publishes each series, and how it is run. Sources: the pollsters' own method statements as linked
# from Wikipedia rows; Research Association NZ (RANZ) political polling code (https://www.researchassociation.org.nz/political-polling-code).
POLLSTER_META = {
    "1 News–Verian": {"commissioner": "TVNZ 1News", "fieldwork_company": "Verian (formerly Colmar Brunton / Kantar Public)",
                      "method": "Landline + mobile CATI and online panel, n≈1,000, max. sampling error ±3.1 pts at 95%", "type": "public-media",
                      "history": "Same series as 1 News–Colmar Brunton (to 2021) and 1 News–Kantar Public (2021–23)",
                      "aliases": ["1 News–Kantar Public", "1 News–Colmar Brunton", "One News Colmar Brunton", "Colmar Brunton"]},
    "RNZ–Reid Research": {"commissioner": "RNZ (previously Newshub, to 2024)", "fieldwork_company": "Reid Research",
                          "method": "Online panel + telephone, n≈1,000, ±3.1 pts", "type": "public-media",
                          "aliases": ["Newshub–Reid Research", "3 News Reid Research", "Newshub-Reid Research", "Reid Research"]},
    "Taxpayers' Union–Curia": {"commissioner": "New Zealand Taxpayers' Union (advocacy group)", "fieldwork_company": "Curia Market Research (David Farrar)",
                               "method": "Phone + online panel, n≈1,000, ±3.1 pts; Curia left RANZ in 2024", "type": "public-sponsored",
                               "aliases": ["Taxpayers' Union-Curia"]},
    "Roy Morgan": {"commissioner": "Roy Morgan Research (self-published)", "fieldwork_company": "Roy Morgan",
                   "method": "Telephone/online, fieldwork spans the whole month, n≈800–1,000", "type": "public-self",
                   "aliases": ["Roy Morgan Research"]},
    "The Post/Freshwater Strategy": {"commissioner": "The Post (Stuff)", "fieldwork_company": "Freshwater Strategy",
                                     "method": "Online panel, n≈1,000–1,500", "type": "public-media",
                                     "aliases": ["Post/Freshwater Strategy", "Freshwater Strategy"]},
    "Talbot Mills": {"commissioner": "Talbot Mills Research (corporate-client poll; also Labour's pollster, formerly UMR)",
                     "fieldwork_company": "Talbot Mills", "method": "Online panel, n≈1,000; results leaked/published irregularly",
                     "type": "internal-leaked", "aliases": ["Labour–Talbot Mills", "UMR", "UMR Research"]},
    "Labour–Talbot Mills": {"commissioner": "New Zealand Labour Party", "fieldwork_company": "Talbot Mills", "method": "Internal party poll, published selectively",
                            "type": "internal-party"},
    "Anacta": {"commissioner": "Anacta Consulting (corporate clients; has polled for Labour)", "fieldwork_company": "Anacta",
               "method": "Online, n≈1,300–1,700; published via NZ Herald / The Post", "type": "internal-leaked"},
    "Curia": {"commissioner": "Curia Market Research (National's pollster) - publicly released polls not sponsored by the Taxpayers' Union",
              "fieldwork_company": "Curia", "method": "Phone + online", "type": "internal-leaked"},
    "Herald–DigiPoll": {"commissioner": "NZ Herald (series ended 2017)", "fieldwork_company": "DigiPoll", "method": "Landline CATI", "type": "public-media"},
    "Fairfax Media–Ipsos": {"commissioner": "Fairfax Media / Stuff (2013–14; earlier Fairfax–Research International)", "fieldwork_company": "Ipsos", "method": "Landline CATI", "type": "public-media"},
    "Horizon Research": {"commissioner": "Horizon Research (self-published / client releases)", "fieldwork_company": "Horizon",
                         "method": "Online panel", "type": "public-self"},
}
INTERNAL_TYPES = {"internal-leaked", "internal-party"}

MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def log(*a):
    print(*a, file=sys.stderr)


def fetch_article(year, offline=False, force=False):
    """Return (html, meta) for the year's polling article, from cache or the MediaWiki API."""
    title = f"Opinion_polling_for_the_{year}_New_Zealand_general_election"
    os.makedirs(RAW, exist_ok=True)
    html_path, meta_path = os.path.join(RAW, f"wiki_{year}.html"), os.path.join(RAW, f"wiki_{year}.meta.json")
    if (offline or not force) and os.path.exists(html_path) and os.path.exists(meta_path):
        if offline or year != 2026:   # the current cycle is always re-fetched unless --offline
            return open(html_path, encoding="utf-8").read(), json.load(open(meta_path))
    if offline:
        raise FileNotFoundError(f"no cached copy of {title}")
    params = {"action": "parse", "page": title, "prop": "text|revid", "format": "json", "formatversion": "2", "disabletoc": "1"}
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read().decode("utf-8")
            data = json.loads(body)
            if "parse" not in data:
                raise RuntimeError(str(data)[:200])
            html = data["parse"]["text"]
            meta = {"title": title, "url": f"https://en.wikipedia.org/wiki/{title}", "revid": data["parse"].get("revid"),
                    "retrieved": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
            open(html_path, "w", encoding="utf-8").write(html)
            json.dump(meta, open(meta_path, "w"), indent=1)
            time.sleep(2.0)   # be polite: the API rate-limits bursts
            return html, meta
        except Exception as e:   # noqa: BLE001
            log(f"  fetch {title} attempt {attempt + 1} failed: {e}")
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"could not fetch {title}")


def clean(s):
    return re.sub(r"\s+", " ", s).strip()


def header_key(th):
    t = clean(th.get_text(" ", strip=True))
    t = re.sub(r"\[.*?\]", "", t).strip().lower()
    return t


def num(s):
    s = s.replace(",", "").replace("~", "").replace("<", "").strip()
    m = re.match(r"^(\d+(?:\.\d+)?)", s)
    return float(m.group(1)) if m else None


def parse_date_text(txt, year_hint=None):
    """Last fieldwork day from strings like '17–30 Nov 2008', '29 Sep – 12 Oct 2014', '14 Oct 2023', 'Sep 2026'."""
    t = txt.replace("–", "-").replace("—", "-")
    ms = re.findall(r"(\d{1,2})?\s*([A-Za-z]{3})[a-z]*\.?\s+(\d{4})", t)
    if not ms:
        return None
    d, mon, y = ms[-1]
    mon = MONTHS.get(mon.lower()[:3])
    if not mon:
        return None
    day = int(d) if d else None
    if day is None:   # month only: use the end of the month
        nxt = dt.date(int(y) + (mon == 12), (mon % 12) + 1, 1)
        return (nxt - dt.timedelta(days=1)).isoformat()
    try:
        return dt.date(int(y), mon, day).isoformat()
    except ValueError:
        return None


def pick_main_table(soup):
    """The party-vote table: the biggest wikitable whose header has a poll/date column and >=3 party columns."""
    best = None
    for t in soup.select("table.wikitable"):
        tr = t.find("tr")
        if not tr:
            continue
        hdr = [header_key(th) for th in tr.find_all(["th", "td"])]
        parties = [h for h in hdr if h in PARTY_COLS and PARTY_COLS[h] != "others"]
        if len(parties) >= 3 and any(h.startswith("date") for h in hdr) and any(h.startswith("poll") for h in hdr):
            n = len(t.find_all("tr"))
            if best is None or n > best[0]:
                best = (n, t)
    return best[1] if best else None


def parse_party_table(table):
    """Parse one Wikipedia party-vote table into poll rows + event rows. Handles the 2011–2026 layouts."""
    for s in table.select("sup.reference, span.mw-editsection"):
        s.decompose()
    trs = table.find_all("tr")
    hdr = [header_key(th) for th in trs[0].find_all(["th", "td"])]
    idx_date = next(i for i, h in enumerate(hdr) if h.startswith("date"))
    idx_poll = next(i for i, h in enumerate(hdr) if h.startswith("poll"))
    idx_n = next((i for i, h in enumerate(hdr) if h.startswith("sample")), None)
    polls, events = [], []
    for tr in trs[1:]:
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue
        txt = [clean(c.get_text(" ", strip=True)) for c in cells]
        if all(t == "" for t in txt):
            continue
        if [t.lower().split("[")[0].strip() for t in txt[:2]] in (["poll", "date"], ["date", "poll"], ["date", "polling organisation"]):
            continue   # repeated header at the bottom
        if len(cells) <= 2 and any(c.has_attr("colspan") for c in cells):   # event rows
            ev = txt[-1]
            m = re.match(r"^(\d{1,2}(?:[–-]\d{1,2})?\s+\w{3,9}\s+\d{4})\s*[–-]\s*(.*)$", ev)
            events.append({"date": m.group(1) if m else txt[0], "event": m.group(2) if m else ev,
                           "end_date": parse_date_text(m.group(1) if m else txt[0])})
            continue
        if len(cells) < len(hdr) - 2:
            continue
        dcell, pcell = cells[idx_date], cells[idx_poll]
        pollster = txt[idx_poll]
        sort = dcell.get("data-sort-value")
        end_date = sort if sort and re.match(r"^\d{4}-\d{2}-\d{2}$", sort) else parse_date_text(txt[idx_date])
        a = pcell.find("a", href=True)
        href = a["href"] if a else None
        if href and href.startswith("//"):
            href = "https:" + href
        if href and not href.startswith("http"):
            href = "https://en.wikipedia.org" + href if href.startswith("/wiki/") else None
        row = {"date": txt[idx_date], "end_date": end_date, "pollster": pollster, "source_url": href,
               "sample_size": int(num(txt[idx_n])) if idx_n is not None and idx_n < len(txt) and num(txt[idx_n]) else None,
               "results": {}}
        if "election result" in pollster.lower():
            row["is_election_result"] = True
            m = re.search(r"(\d{4})", pollster)
            if m and m.group(1) in {str(y) for y in ELECTION_DATES}:
                row["end_date"] = ELECTION_DATES[int(m.group(1))]
        for h, c in zip(hdr, cells):
            slug = PARTY_COLS.get(h)
            if not slug or h in NON_PARTY_COLS:
                continue
            v = num(clean(c.get_text(" ", strip=True)))
            if v is None:
                continue
            if slug == "others":
                row["others"] = v
            else:
                row["results"][slug] = v
        if len(row["results"]) >= 2:
            polls.append(row)
    return polls, events


def parse_electorate_tables(soup):
    """2026 article: per-electorate tables (party vote / electorate vote sub-rows). Returns a flat list."""
    out = []
    h2 = None
    for h in soup.find_all(["h2", "h3", "h4"]):
        if h.get_text(strip=True).lower().startswith("electorate polling"):
            h2 = h
            break
    if not h2:
        return out
    for t in soup.select("table.wikitable"):
        head = t.find_previous(["h2"])
        if head is None or head.get_text(strip=True).lower() != "electorate polling":
            # tables inside h3/h4 under the Electorate polling h2: find_previous h2 must be that heading
            continue
        for s in t.select("sup.reference"):
            s.decompose()
        name = t.find_previous(["h3", "h4"]).get_text(strip=True)
        trs = t.find_all("tr")
        hdr = [header_key(th) for th in trs[0].find_all(["th", "td"])]
        party_idx = [(i, PARTY_COLS[h]) for i, h in enumerate(hdr) if h in PARTY_COLS and h not in NON_PARTY_COLS]
        if not party_idx:
            continue
        kind_col = hdr.index("") if "" in hdr else 3
        current = None
        for tr in trs[1:]:
            cells = tr.find_all(["td", "th"])
            txt = [clean(c.get_text(" ", strip=True)) for c in cells]
            if not txt:
                continue
            if len(cells) >= len(hdr) - 1:   # full row: date, pollster, n, kind, values...
                a = cells[1].find("a", href=True)
                current = {"electorate": name, "date": txt[0], "end_date": parse_date_text(txt[0]), "pollster": txt[1],
                           "sample_size": int(num(txt[2])) if num(txt[2]) else None,
                           "source_url": a["href"] if a and a["href"].startswith("http") else None}
                kind, vals = txt[kind_col], txt[kind_col + 1:]
                offset = kind_col + 1
            else:   # continuation row: kind + values (pollster/date cells rowspan'd)
                if current is None:
                    continue
                kind, vals = txt[0], txt[1:]
                offset = kind_col + 1
            res = {}
            for (i, slug) in party_idx:
                j = i - offset
                if 0 <= j < len(vals):
                    v = num(vals[j])
                    if v is not None:
                        res[slug] = v
            if res and kind:
                row = dict(current)
                row["vote"] = "electorate" if "electorate" in kind.lower() else "party"
                row["results"] = res
                out.append(row)
    return out


def norm_pollster(name):
    n = name.replace("-", "–").replace("—", "–")
    n = re.sub(r"\s+", " ", n).strip()
    n = n.replace("1News", "1 News").replace("Taxpayers’", "Taxpayers'")
    return n


def pollster_canonical(name):
    """Group series that changed name (Colmar Brunton -> Kantar Public -> Verian; 3 News/Newshub/RNZ Reid Research, ...)."""
    n = norm_pollster(re.sub(r"\[.*?\]|Archived.*$|\(.*?\)", "", name))
    n = re.sub(r"\s+", " ", n).strip(" –-")
    low = n.lower()
    if "election result" in low:
        return n
    for canon, meta in POLLSTER_META.items():
        if n == canon or n in meta.get("aliases", []):
            return canon
    rules = [("taxpayer", "Taxpayers' Union–Curia"), ("colmar", "1 News–Verian"), ("kantar", "1 News–Verian"), ("verian", "1 News–Verian"),
             ("reid research", "RNZ–Reid Research"), ("roy morgan", "Roy Morgan"), ("digipoll", "Herald–DigiPoll"),
             ("ipsos", "Fairfax Media–Ipsos"), ("research international", "Fairfax Media–Ipsos"), ("freshwater", "The Post/Freshwater Strategy"),
             ("talbot", "Talbot Mills"), ("umr", "Talbot Mills"), ("anacta", "Anacta"), ("horizon", "Horizon Research")]
    for key, canon in rules:
        if key in low:
            if canon == "Talbot Mills" and "labour" in low:
                return "Labour–Talbot Mills"
            return canon
    if low == "curia":
        return "Curia"
    return n


def row_key(p):
    return (pollster_canonical(p["pollster"]), p.get("end_date"), p.get("is_election_result", False))


def merge_2026(existing, fresh_polls, fresh_events, electorate_polls, meta):
    """Preserve every existing row/field; add new rows; fill blanks from Wikipedia; never delete."""
    ex_rows = existing.get("polls", []) if existing else []
    by_key = {row_key(p): p for p in ex_rows}
    added, updated = 0, 0
    for p in fresh_polls:
        p = dict(p)
        p["pollster"] = norm_pollster(p["pollster"])
        k = row_key(p)
        if k in by_key:
            e = by_key[k]
            for fld in ("source_url", "sample_size", "others", "date"):
                if e.get(fld) in (None, "") and p.get(fld) not in (None, ""):
                    e[fld] = p[fld]; updated += 1
            for party, v in p["results"].items():
                if party not in e["results"]:
                    e["results"][party] = v; updated += 1
        else:
            by_key[k] = p; added += 1
    rows = list(by_key.values())
    for p in rows:
        canon = pollster_canonical(p["pollster"])
        p["pollster_key"] = canon
        t = POLLSTER_META.get(canon, {}).get("type")
        p["internal"] = bool(t in INTERNAL_TYPES)
    rows.sort(key=lambda p: (p.get("end_date") or "", p.get("is_election_result", False), p["pollster"]), reverse=True)
    out = dict(existing) if existing else {}
    out.setdefault("title", "Opinion polls (party vote) for the 2026 New Zealand general election, since the 14 Oct 2023 election")
    out["source"] = meta["url"]
    out["source_revid"] = meta.get("revid")
    out["retrieved"] = meta["retrieved"][:10]
    out.setdefault("parties", {"NAT": "national", "LAB": "labour", "GRN": "green", "ACT": "act", "NZF": "nz-first", "TPM": "te-pati-maori", "OPP": "opportunity"})
    out["notes"] = ("Percentages as published (decided voters; undecided excluded by every pollster). 'end_date' is the sort date used by Wikipedia "
                    "(last fieldwork day or release date). Rows are newest first. 'others' = combined minor parties where listed. "
                    "'pollster_key' groups series that changed name; 'internal' marks party/corporate-client polls that are published selectively. "
                    "Poll sources: each row's source_url as linked on Wikipedia. Refreshed by tools/polls_update.py.")
    out["count"] = len([p for p in rows if not p.get("is_election_result")])
    out["polls"] = rows
    out["pollsters"] = {k: {kk: vv for kk, vv in v.items() if kk != "aliases"} | {"n_polls": sum(1 for p in rows if p.get("pollster_key") == k and not p.get("is_election_result"))}
                        for k, v in POLLSTER_META.items() if any(p.get("pollster_key") == k for p in rows)}
    if fresh_events:
        out["events"] = fresh_events
    if electorate_polls:
        out["electorate_polls"] = electorate_polls
        out["electorate_polls_note"] = ("Electorate-level polls from the same Wikipedia article (section 'Electorate polling'). "
                                        "'vote' = party or electorate (candidate) vote. Small samples (n≈400–800); treat as indicative only.")
    return out, added, updated


def write_json(path, obj):
    new = json.dumps(obj, ensure_ascii=False, indent=1) + "\n"
    if os.path.exists(path) and open(path, encoding="utf-8").read() == new:
        return False
    open(path, "w", encoding="utf-8").write(new)
    return True


def build_history(year, html, meta):
    soup = BeautifulSoup(html, "lxml")
    table = pick_main_table(soup)
    if table is None:
        raise RuntimeError(f"{year}: party-vote table not found")
    polls, events = parse_party_table(table)
    for p in polls:
        p["pollster"] = norm_pollster(p["pollster"])
        p["pollster_key"] = pollster_canonical(p["pollster"])
    polls.sort(key=lambda p: (p.get("end_date") or "", p.get("is_election_result", False)), reverse=True)
    result = next((p for p in polls if p.get("is_election_result") and p["end_date"] == ELECTION_DATES[year]), None)
    official = None
    ep = os.path.join(ROOT, "data", "elections", f"{year}.json")
    if os.path.exists(ep):
        e = json.load(open(ep))
        official = {p["party"]: p["party_vote_pct"] for p in e["parties"] if p.get("party_vote_pct") is not None}
    return {"title": f"Opinion polls (party vote) for the {year} New Zealand general election",
            "source": meta["url"], "source_revid": meta.get("revid"), "retrieved": meta["retrieved"][:10],
            "election_date": ELECTION_DATES[year],
            "notes": "Parsed from Wikipedia by tools/polls_update.py. Rows newest first; 'end_date' = last fieldwork day where known "
                     "(2011/2014 tables give no sample sizes). 'result' = official party vote from data/elections/<year>.json.",
            "count": len([p for p in polls if not p.get("is_election_result")]),
            "result": official or (result["results"] if result else None),
            "polls": polls, "events": events}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--history", action="store_true", help="re-fetch the 2011-2023 articles even if cached")
    ap.add_argument("--offline", action="store_true", help="parse cached HTML only")
    args = ap.parse_args()
    changed = []
    # 1. current cycle
    try:
        html, meta = fetch_article(2026, offline=args.offline, force=True)
    except Exception as e:   # noqa: BLE001
        log(f"2026 fetch failed, leaving data/polls-2026.json untouched: {e}")
        html = None
    if html:
        soup = BeautifulSoup(html, "lxml")
        table = pick_main_table(soup)
        polls, events = parse_party_table(table)
        electorate_polls = parse_electorate_tables(BeautifulSoup(html, "lxml"))
        existing = json.load(open(OUT_2026)) if os.path.exists(OUT_2026) else None
        out, added, updated = merge_2026(existing, polls, events, electorate_polls, meta)
        if write_json(OUT_2026, out):
            changed.append(OUT_2026)
        log(f"2026: {len(polls)} rows parsed, {added} added, {updated} fields filled, {len(electorate_polls)} electorate-poll rows; total {out['count']} polls")
    # 2. history
    os.makedirs(HIST_DIR, exist_ok=True)
    for y in YEARS_HISTORY:
        path = os.path.join(HIST_DIR, f"{y}.json")
        if os.path.exists(path) and not args.history and not args.offline:
            continue
        try:
            html, meta = fetch_article(y, offline=args.offline, force=args.history)
            hist = build_history(y, html, meta)
            if write_json(path, hist):
                changed.append(path)
            log(f"{y}: {hist['count']} polls, result {'ok' if hist['result'] else 'MISSING'}")
        except Exception as e:   # noqa: BLE001
            log(f"{y}: failed ({e}); existing file kept")
    print("\n".join(os.path.relpath(c, ROOT) for c in changed) if changed else "no changes")


if __name__ == "__main__":
    main()

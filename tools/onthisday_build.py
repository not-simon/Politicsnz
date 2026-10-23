#!/usr/bin/env python3
"""Build data/onthisday.json and guide/on-this-day.md from curated draft modules, verifying every date
against the raw Wikipedia wikitext saved in raw/onthisday/wikipedia/ (see tools/onthisday_verify.py).

Usage:
  python3 tools/onthisday_build.py --drafts draft_q1.py draft_q2.py ... [--check-only] [--show-fail]

Each draft module defines E = [(date, title, text, tags, verify, party, person, extra), ...]
  date   ISO yyyy-mm-dd (the day the event is filed under; for approx entries, extra["exact_date"] holds the real date)
  verify Wikipedia title or list of titles whose wikitext must contain the date
  party  repo party slug (parties/<slug>) or None; person: repo people slug or None
  extra  dict or None: approx_day, exact_date, note, nzhistory (url), todo

Entries flagged extra["todo"] are dropped. Entries whose date cannot be verified are reported and (unless
--allow-unverified) dropped, so nothing unverified reaches data/onthisday.json.
"""
import calendar, importlib.util, json, os, sys, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import onthisday_verify as V  # noqa: E402

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
WIKI_INDEX = json.load(open(os.path.join(ROOT, "raw", "onthisday", "wikipedia", "_index.json"), encoding="utf-8"))

LICENCE_NOTES = {
    "summary": "Every entry's text was written for this guide in plain English; no sentence is copied from a source. "
               "Dates were checked against the English Wikipedia article named in source_url (raw wikitext saved under "
               "raw/onthisday/wikipedia/, retrieval date in raw/onthisday/wikipedia/_index.json). Wikipedia is used as a "
               "finding aid; its articles cite the primary sources (NZHistory, Te Ara, Parliament, Electoral Commission, "
               "newspapers). The nzhistory_day_url on each day points to NZHistory's own 'Today in history' page for that "
               "date for readers who want the Ministry for Culture and Heritage's account.",
    "wikipedia": {
        "licence": "Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0) for article text; our text is original and "
                   "only facts/dates were taken.",
        "url": "https://en.wikipedia.org/wiki/Wikipedia:Copyrights",
    },
    "nzhistory": {
        "name": "NZHistory (nzhistory.govt.nz), Ministry for Culture and Heritage / Manatū Taonga",
        "licence_as_reported": "Creative Commons Attribution-NonCommercial 3.0 New Zealand (CC BY-NC 3.0 NZ) for text and "
                               "audio podcasts, and for individual images only where stated; attribution to the Ministry for "
                               "Culture and Heritage is required; commercial use needs separate permission; many images are "
                               "third-party and excluded.",
        "licence_url": "https://nzhistory.govt.nz/copyright",
        "licence_deed": "https://creativecommons.org/licenses/by-nc/3.0/nz/",
        "verification_status": "NOT fetched directly. On 23 October 2026 nzhistory.govt.nz (and teara.govt.nz, mch.govt.nz) "
                               "returned HTTP 403 Cloudflare challenge pages to curl, headless Chromium and the WebFetch "
                               "tool from this environment. The licence wording above is as summarised in web-search "
                               "results for https://nzhistory.govt.nz/copyright and should be re-checked against the live "
                               "page before any reuse of NZHistory text or images. No NZHistory text or images are "
                               "reproduced in this dataset; only links are given.",
        "attribution_if_reused": "Text: 'Ministry for Culture and Heritage', licensed under CC BY-NC 3.0 NZ "
                                 "(https://creativecommons.org/licenses/by-nc/3.0/nz/).",
        "warning": "nzhistory.net.nz (the site's former domain, still cited in older references) now serves unrelated "
                   "gambling content and must not be used as a source or mirror.",
    },
    "te_ara": {
        "name": "Te Ara – the Encyclopedia of New Zealand (teara.govt.nz)",
        "licence_as_reported": "CC BY-NC 3.0 NZ for text and some images (per Te Ara's Creative Commons licensing page as "
                               "summarised in search results); not fetched directly (HTTP 403 from this environment).",
        "status": "No Te Ara text reproduced.",
    },
    "parliament_nz": {"status": "Reachable (HTTP 200) but not used as a per-entry source in this dataset."},
    "elections_nz": {"status": "Reachable (HTTP 200) but not used as a per-entry source in this dataset."},
}


def load_draft(path):
    spec = importlib.util.spec_from_file_location("draft", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.E


def wiki_url(title):
    return "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))


def to_entry(t):
    date, title, text, tags, verify, party, person, extra = t
    extra = extra or {}
    e = {"date": date, "title": title, "text": text, "tags": tags, "verify": verify,
         "party": party, "person": person, "extra": extra}
    if extra.get("approx_day") and extra.get("exact_date"):
        e["verify_date"] = extra["exact_date"]
    return e


def repo_slugs():
    parties = {p for p in os.listdir(os.path.join(ROOT, "parties"))
               if os.path.isdir(os.path.join(ROOT, "parties", p))}
    people = {}
    for p in parties:
        d = os.path.join(ROOT, "parties", p, "people")
        if os.path.isdir(d):
            for s in os.listdir(d):
                if os.path.isdir(os.path.join(d, s)):
                    people.setdefault(s, []).append(p)
    return parties, people


def main(argv):
    drafts = []
    check_only = "--check-only" in argv
    show = "--show-fail" in argv
    allow_unverified = "--allow-unverified" in argv
    if "--drafts" in argv:
        drafts = [a for a in argv[argv.index("--drafts") + 1:] if not a.startswith("--")]
    entries = []
    for d in drafts:
        entries += [to_entry(t) for t in load_draft(d)]
    parties, people = repo_slugs()

    problems = []
    kept = []
    for e in entries:
        if e["extra"].get("todo"):
            problems.append(("todo", e["date"], e["title"]))
            continue
        if len(e["text"]) > 240:
            problems.append(("toolong", e["date"], e["title"], len(e["text"])))
        st, det = V.check_entry(e)
        if st != "ok":
            problems.append((st, e["date"], e["title"], det))
            if not allow_unverified:
                continue
        if e["party"] and e["party"] not in parties:
            problems.append(("badparty", e["date"], e["title"], e["party"]))
            e["party"] = None
        if e["person"] and e["person"] not in people:
            problems.append(("badperson", e["date"], e["title"], e["person"]))
            e["person"] = None
        kept.append(e)

    # day coverage
    days = {}
    for e in kept:
        key = e["date"][5:]
        days.setdefault(key, []).append(e)
    all_days = [f"{m:02d}-{d:02d}" for m in range(1, 13) for d in range(1, calendar.monthrange(2024, m)[1] + 1)]
    missing = [d for d in all_days if d not in days]
    over = [(d, len(v)) for d, v in days.items() if len(v) > 3]

    counts = {}
    for p in problems:
        counts[p[0]] = counts.get(p[0], 0) + 1
    print("entries in drafts:", len(entries), "kept:", len(kept), "problems:", counts)
    print("days covered:", len(days), "/", len(all_days), "missing:", missing)
    if over:
        print("days with >3 entries:", over)
    if show:
        for p in problems:
            print("  ", *p)
    if check_only:
        return 0

    # ---- write data/onthisday.json
    out_days = {}
    for key in all_days:
        if key not in days:
            continue
        lst = []
        for e in sorted(days[key], key=lambda x: x["date"]):
            ver = e["verify"] if isinstance(e["verify"], list) else [e["verify"]]
            src_title = None
            for t in ver:
                if V.wikitext(t) is not None:
                    src_title = t
                    break
            idx = WIKI_INDEX.get(src_title, {})
            item = {
                "year": int(e["date"][:4]),
                "title": e["title"],
                "text": e["text"],
                "tags": e["tags"],
                "source_url": wiki_url(idx.get("redirect_to", src_title)),
                "source_name": "Wikipedia",
                "source_retrieved": idx.get("retrieved"),
                "related": {"party": e["party"], "person": e["person"]},
            }
            if e["extra"].get("approx_day"):
                item["approx_day"] = True
                item["exact_date"] = e["extra"].get("exact_date", e["date"])
                if e["extra"].get("note"):
                    item["note"] = e["extra"]["note"]
            if e["extra"].get("nzhistory"):
                item["nzhistory_url"] = e["extra"]["nzhistory"]
            lst.append(item)
        m, d = int(key[:2]), int(key[3:])
        out_days[key] = lst
    nz_day_urls = {k: f"https://nzhistory.govt.nz/timeline/{int(k[3:])}/{int(k[:2])}" for k in all_days}
    data = {
        "title": "On this day in New Zealand politics",
        "generated": "2026-10-23",
        "description": "One to three dated events from New Zealand political and constitutional history for every day of "
                       "the year, written in plain English for the Ballot Book NZ voter guide.",
        "licence_notes": LICENCE_NOTES,
        "fields": {
            "year": "year of the event", "title": "short headline", "text": "one or two plain sentences, max 240 chars",
            "tags": "topic tags", "source_url": "Wikipedia article whose text contains the date (finding aid)",
            "source_retrieved": "date the wikitext was saved", "related.party": "parties/<slug> in this repo or null",
            "related.person": "parties/*/people/<slug> in this repo or null",
            "approx_day": "true when the entry is filed on a nearby day because no political event was found; exact_date "
                          "gives the real date",
            "nzhistory_day_url (per day)": "NZHistory 'Today in history' page for the day (not fetched; see licence_notes)",
        },
        "nzhistory_day_url": nz_day_urls,
        "days": out_days,
    }
    with open(os.path.join(ROOT, "data", "onthisday.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    # ---- write guide/on-this-day.md
    lines = ["# On this day in New Zealand politics", "",
             "One to three events from New Zealand's political and constitutional history for every day of the year, "
             "written in plain English. Data: [`data/onthisday.json`](../data/onthisday.json). Each entry links to the "
             "Wikipedia article used to check the date (Wikipedia is a finding aid; its articles cite the primary sources). "
             "Each day also links to NZHistory's own \"Today in history\" page (Ministry for Culture and Heritage, "
             "text CC BY-NC 3.0 NZ as reported; see licence notes in the JSON). Entries marked *approx.* are filed on a "
             "nearby day because no political event was found for that date; the exact date is given.", "",
             "Jump to: " + " · ".join(f"[{MONTHS[m-1]}](#{MONTHS[m-1].lower()})" for m in range(1, 13)), ""]
    for m in range(1, 13):
        lines.append(f"## {MONTHS[m-1]}")
        lines.append("")
        for d in range(1, calendar.monthrange(2024, m)[1] + 1):
            key = f"{m:02d}-{d:02d}"
            lines.append(f"### {d} {MONTHS[m-1]}")
            lines.append("")
            for item in out_days.get(key, []):
                approx = f" *(approx. — exact date {item['exact_date']})*" if item.get("approx_day") else ""
                rel = []
                if item["related"]["party"]:
                    rel.append(f"[{item['related']['party']}](../parties/{item['related']['party']}/README.md)")
                if item["related"]["person"]:
                    p = item["related"]["party"] or ""
                    rel.append(f"[{item['related']['person']}](../parties/{p}/people/{item['related']['person']}/README.md)"
                               if p else item["related"]["person"])
                relstr = f" Related: {', '.join(rel)}." if rel else ""
                lines.append(f"- **{item['year']} — {item['title']}**{approx} {item['text']} "
                             f"[[source]]({item['source_url']}){relstr}")
            lines.append(f"- NZHistory for this day: <{nz_day_urls[key]}>")
            lines.append("")
    with open(os.path.join(ROOT, "guide", "on-this-day.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote data/onthisday.json and guide/on-this-day.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

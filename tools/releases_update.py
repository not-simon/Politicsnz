#!/usr/bin/env python3
"""Party newsroom feed (data/releases.json) and politicians' follow directory (data/guide/follow.json).

Usage:
  python3 tools/releases_update.py              # fetch Scoop + Beehive, merge into data/releases.json (60-day window)
  python3 tools/releases_update.py --offline    # re-parse the cached pages in raw/releases/cache/ without network access
  python3 tools/releases_update.py --no-scoop   # Beehive + party newsroom links only (see the Scoop terms note below)
  python3 tools/releases_update.py --follow     # rebuild data/guide/follow.json from parties/*/people/*/person.json (no network)

Outputs (idempotent: a run that finds nothing new leaves the files byte-identical, so the hourly Action commits only on change):
  data/releases.json          {"updated", "window_days", "terms_note", "sources": [...], "items": [...]}
  data/guide/follow.json      {"parties": {slug: {accounts}}, "people": [{slug, party, name, folder, accounts}]}
  raw/releases/cache/*        last fetched copy of every page/feed (gitignored; used by --offline)
  raw/releases/scoop_terms_2026-10-23.txt   the Scoop terms as retrieved, kept for the record

Where the releases come from
  * Scoop (scoop.co.nz) publishes every party's press releases verbatim. Scoop's RSS feeds are per *section*
    (Parliament = s.c=PA, Politics = s.c=PO: https://www.scoop.co.nz/about/rss.html) and carry no organisation field, so a
    party cannot be identified from the feed alone. Scoop's organisation InfoPages (https://info.scoop.co.nz/<Org>) list the
    organisation's latest 20 releases (headline, date, byline, Scoop's own one-paragraph teaser) but have no RSS of their own
    (checked 2026-10-23: the only feed links on an InfoPage are the section feeds). So: one request per party InfoPage for
    attribution, plus the two section feeds for the description text where Scoop provides one. Nothing beyond headline, link,
    date and the first ~200 characters of Scoop's teaser is stored; release bodies are never fetched.
  * Beehive (beehive.govt.nz/rss.xml) for ministerial releases: tagged party "government", ministerial true. Ministers'
    releases are government communications, not party releases, and are shown as such.
  * Each party's own newsroom URL is recorded as the fallback link (several party sites block automated access).

Terms (see TERMS_NOTE below and raw/releases/scoop_terms_2026-10-23.txt). Scoop's terms allow free use by "personal and
private users" with attribution and no commercial purpose, and require a licence for organisational/commercial use and for
"media monitoring" redistribution. Headline + link + short attributed snippet is what RSS is published for, and this guide is a
non-commercial volunteer project, but the terms are not written with that case in mind: confirm with licensing@scoop.co.nz
before any wider deployment, and use --no-scoop if in doubt. The copyright in each release itself belongs to the party.

Politeness: one GET per feed/page per run, a fixed User-Agent, 20 s timeout, ~0.7 s between requests; a failed fetch leaves
the previously stored items for that source untouched and records the error in `sources`.
"""
import argparse, datetime as dt, glob, hashlib, html, json, os, re, sys, time, urllib.error, urllib.request
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "data", "releases.json")
FOLLOW_OUT = os.path.join(ROOT, "data", "guide", "follow.json")
CACHE = os.path.join(ROOT, "raw", "releases", "cache")
UA = "PoliticsNZResearch/1.0 (personal research; releases_update.py)"
NZ = ZoneInfo("Pacific/Auckland")
WINDOW_DAYS = 60
SUMMARY_CHARS = 200
PAUSE = 0.7

SCOOP_TERMS_URL = "https://www.scoop.co.nz/about/terms.html"
SCOOP_RSS_PAGE = "https://www.scoop.co.nz/about/rss.html"
SCOOP_SECTION_FEEDS = {"PA": "https://www.scoop.co.nz/storyindex/index.rss?s.c=PA",   # Parliament
                       "PO": "https://www.scoop.co.nz/storyindex/index.rss?s.c=PO"}   # Politics
BEEHIVE_FEED = "https://www.beehive.govt.nz/rss.xml"

TERMS_NOTE = (
    "Scoop: headlines, links, dates and the first ~200 characters of Scoop's own teaser are taken from Scoop's public "
    "InfoPages and section RSS feeds (" + SCOOP_RSS_PAGE + "), with attribution to Scoop on every item; release text is not "
    "reproduced. Scoop's terms (" + SCOOP_TERMS_URL + ", retrieved 2026-10-23; copy in raw/releases/scoop_terms_2026-10-23.txt) "
    "license Scoop content 'freely to personal and private users' who attribute Scoop and have 'no commercial purposes' "
    "(cl. 3.1), restrict unlicensed use 'in any professional capacity' by organisations including not-for-profits (cl. 3.3), "
    "count 'direct linking' and automated extraction as 'use' (cl. 3.3.2) and prohibit unlicensed media-monitoring "
    "redistribution (cl. 4). The feeds' own copyright line is 'Scoop Media Ltd and/or its contributors'. This guide is a "
    "non-commercial volunteer project showing headline + link + short attributed snippet, which is the use RSS is published "
    "for; whether that falls under cl. 3.1 or needs a licence has not been confirmed with Scoop (licensing@scoop.co.nz). "
    "The Scoop channel can be switched off with --no-scoop, leaving Beehive and the parties' own newsroom links. "
    "Beehive: ministerial releases are Crown copyright; beehive.govt.nz says its content is released under a Creative Commons "
    "Attribution licence, but the copyright page could not be re-read by script on 2026-10-23 (it returned a script-only "
    "response), so check https://www.beehive.govt.nz/copyright. The copyright in each party release belongs to the party that "
    "issued it. Items are never fact-checked: they are the party's or minister's own words."
)

# The 17 parties registered for the 7 November 2026 election (data/guide/parties.json). `scoop` is the InfoPage name
# (None = no InfoPage found on 2026-10-23 after trying the obvious names); `newsroom` is the party's own news page,
# `newsroom_verified` records whether that URL returned 200 on 2026-10-23 (some sites block automated access: 403).
PARTIES = [
    {"slug": "national", "name": "New Zealand National Party", "scoop": "New_Zealand_National_Party",
     "website": "https://www.national.org.nz/", "newsroom": "https://www.national.org.nz/news", "newsroom_verified": True},
    {"slug": "labour", "name": "New Zealand Labour Party", "scoop": "New_Zealand_Labour_Party",
     "website": "https://www.labour.org.nz/", "newsroom": "https://www.labour.org.nz/news", "newsroom_verified": True},
    {"slug": "green", "name": "Green Party of Aotearoa New Zealand", "scoop": "Green_Party",
     "website": "https://www.greens.org.nz/", "newsroom": "https://www.greens.org.nz/news", "newsroom_verified": False},
    {"slug": "act", "name": "ACT New Zealand", "scoop": "ACT_New_Zealand",
     "website": "https://www.act.org.nz/", "newsroom": "https://www.act.org.nz/news", "newsroom_verified": True},
    {"slug": "nz-first", "name": "New Zealand First", "scoop": "New_Zealand_First_Party",
     "website": "https://www.nzfirst.nz/", "newsroom": "https://www.nzfirst.nz/news", "newsroom_verified": False},
    {"slug": "te-pati-maori", "name": "Te Pāti Māori", "scoop": "Te_Pati_Maori",
     "website": "https://www.maoriparty.org.nz/", "newsroom": "https://www.maoriparty.org.nz/", "newsroom_verified": False},
    {"slug": "opportunity", "name": "Opportunity Party", "scoop": "The_Opportunity_Party",   # the older The_Opportunities_Party page stops at June 2025
     "website": "https://www.opportunity.org.nz/", "newsroom": "https://www.opportunity.org.nz/", "newsroom_verified": False},
    {"slug": "nz-loyal", "name": "New Zealand Loyal", "scoop": "NZ_Loyal",
     "website": "https://nzloyal.com/", "newsroom": "https://nzloyal.com/", "newsroom_verified": False},
    {"slug": "nz-outdoors-freedom", "name": "NZ Outdoors & Freedom Party", "scoop": "NZ_Outdoors_and_Freedom_Party",
     "website": "https://freedom.kiwi/", "newsroom": "https://freedom.kiwi/media", "newsroom_verified": True},
    {"slug": "legalise-cannabis", "name": "Aotearoa Legalise Cannabis Party", "scoop": "Aotearoa_Legalise_Cannabis_Party",
     "website": "https://alcp.org.nz/", "newsroom": "https://alcp.org.nz/news", "newsroom_verified": True},
    {"slug": "animal-justice", "name": "Animal Justice Party Aotearoa New Zealand", "scoop": None,
     "website": "https://animaljustice.org.nz/", "newsroom": "https://animaljustice.org.nz/news/", "newsroom_verified": True},
    {"slug": "alliance", "name": "Alliance Party of Aotearoa New Zealand", "scoop": None,
     "website": "https://allianceparty.nz/", "newsroom": "https://allianceparty.nz/news/", "newsroom_verified": True},
    {"slug": "conservative", "name": "Conservative Party NZ", "scoop": "Conservative_Party",
     "website": "https://www.conservatives.nz/", "newsroom": "https://www.conservatives.nz/news", "newsroom_verified": True},
    {"slug": "womens-rights", "name": "Women's Rights Party", "scoop": "Women%27s_Rights_Party",
     "website": "https://womensrightsparty.nz/", "newsroom": "https://womensrightsparty.nz/news/", "newsroom_verified": True},
    {"slug": "vision-nz", "name": "Vision New Zealand", "scoop": "Vision_NZ",
     "website": "https://vision.org.nz/", "newsroom": "https://vision.org.nz/news", "newsroom_verified": True},
    {"slug": "free-palestine", "name": "Free Palestine (Palestine Free from the River to the Sea Party)", "scoop": "Free_Palestine_Party",
     "website": "https://palfree.nz/", "newsroom": "https://palfree.nz/", "newsroom_verified": True},
    {"slug": "te-tai-tokerau-party", "name": "Te Tai Tokerau Party", "scoop": "Te_Tai_Tokerau_Party",
     "website": "https://tetaitokerauparty.org.nz/", "newsroom": "https://tetaitokerauparty.org.nz/", "newsroom_verified": True},
]
PARTY_SLUGS = {p["slug"] for p in PARTIES}

# Official party accounts for data/guide/follow.json. `verified` = the URL was read from the party's own website on 2026-10-23
# ("site"); "wikidata" = taken from the party's Wikidata item (P856/P2002/P2003/P2013/P2397/P7085/P4264) because the site blocks
# automated access, so it is listed but marked unverified; null = no official account found in either source.
# nzloyal.org.nz (Wikidata) returned HTTP 402 and freepalestineparty.com (Wikidata) is an unrelated European group: both ignored.
PARTY_ACCOUNTS = {
    "national": {"website": ("https://www.national.org.nz/", "site"), "facebook": ("https://www.facebook.com/NZNATS", "site"),
                 "instagram": ("https://www.instagram.com/nznationalparty", "site"), "x": ("https://x.com/NZNationalParty", "wikidata"),
                 "tiktok": ("https://www.tiktok.com/@newzealandnationalparty", "site"), "youtube": None,
                 "linkedin": ("https://www.linkedin.com/company/national-party", "site")},
    "labour": {"website": ("https://www.labour.org.nz/", "site"), "facebook": ("https://www.facebook.com/NZLabourParty/", "site"),
               "instagram": ("https://www.instagram.com/nzlabour/", "site"), "x": ("https://x.com/nzlabour", "site"),
               "tiktok": ("https://www.tiktok.com/@nzlabour", "site"), "youtube": ("https://www.youtube.com/c/labournz", "site"), "linkedin": None},
    "green": {"website": ("https://www.greens.org.nz/", "wikidata"), "facebook": ("https://www.facebook.com/10779081371", "wikidata"),
              "instagram": ("https://www.instagram.com/nzgreenparty", "wikidata"), "x": ("https://x.com/NZGreens", "wikidata"),
              "tiktok": None, "youtube": ("https://www.youtube.com/channel/UCHMJ7z-9wxGvWVljzfntFVQ", "wikidata"), "linkedin": None},
    "act": {"website": ("https://www.act.org.nz/", "site"), "facebook": ("https://www.facebook.com/actparty/", "site"),
            "instagram": ("https://www.instagram.com/actnewzealand", "site"), "x": ("https://x.com/actparty", "site"),
            "tiktok": ("https://www.tiktok.com/@actnewzealand", "site"), "youtube": ("https://www.youtube.com/c/ACTNewZealand", "site"), "linkedin": None},
    "nz-first": {"website": ("https://www.nzfirst.nz/", "wikidata"), "facebook": ("https://www.facebook.com/NZFirst", "wikidata"),
                 "instagram": ("https://www.instagram.com/newzealandfirst", "wikidata"), "x": ("https://x.com/nzfirst", "wikidata"),
                 "tiktok": None, "youtube": None, "linkedin": None},
    "te-pati-maori": {"website": ("https://www.maoriparty.org.nz/", "wikidata"), "facebook": ("https://www.facebook.com/MaoriParty", "wikidata"),
                      "instagram": ("https://www.instagram.com/maori_party", "wikidata"), "x": ("https://x.com/Maori_Party", "wikidata"),
                      "tiktok": None, "youtube": None, "linkedin": None},
    "opportunity": {"website": ("https://www.opportunity.org.nz/", "wikidata"), "facebook": None,
                    "instagram": ("https://www.instagram.com/top.nz", "wikidata"), "x": None, "tiktok": None, "youtube": None, "linkedin": None},
    "nz-loyal": {"website": ("https://nzloyal.com/", "guide"), "facebook": None, "instagram": None, "x": None, "tiktok": None, "youtube": None, "linkedin": None},
    "nz-outdoors-freedom": {"website": ("https://freedom.kiwi/", "site"), "facebook": ("https://www.facebook.com/FreedomDotKiwi/", "site"),
                            "instagram": None, "x": ("https://x.com/FreedomDotKiwi", "site"), "tiktok": ("https://www.tiktok.com/@freedomdotkiwi", "site"),
                            "youtube": ("https://www.youtube.com/channel/UC4EbgWXRT_NQggLEpGj6gxA", "site"), "linkedin": None},
    "legalise-cannabis": {"website": ("https://alcp.org.nz/", "site"), "facebook": ("https://www.facebook.com/AotearoaLCP", "site"),
                          "instagram": None, "x": None, "tiktok": None, "youtube": None, "linkedin": None},
    "animal-justice": {"website": ("https://animaljustice.org.nz/", "site"), "facebook": ("https://www.facebook.com/AnimalJusticePartyNZ", "site"),
                       "instagram": ("https://www.instagram.com/AnimalJusticeNZ/", "site"), "x": None, "tiktok": None,
                       "youtube": ("https://www.youtube.com/@AnimalJusticePartyNZ", "site"), "linkedin": None},
    "alliance": {"website": ("https://allianceparty.nz/", "site"), "facebook": ("https://www.facebook.com/alliancepartynz", "site"),
                 "instagram": ("https://www.instagram.com/alliancepartyaotearoa/", "site"), "x": None, "tiktok": None,
                 "youtube": ("https://www.youtube.com/@AlliancePartyNZ", "site"), "linkedin": None},
    "conservative": {"website": ("https://www.conservatives.nz/", "site"), "facebook": None, "instagram": None, "x": None, "tiktok": None, "youtube": None, "linkedin": None},
    "womens-rights": {"website": ("https://womensrightsparty.nz/", "site"), "facebook": None, "instagram": None, "x": None, "tiktok": None, "youtube": None, "linkedin": None},
    "vision-nz": {"website": ("https://vision.org.nz/", "site"), "facebook": ("https://www.facebook.com/VisionNZparty", "site"),
                  "instagram": ("https://www.instagram.com/visionnewzealand/", "site"), "x": ("https://x.com/Visionnzparty", "site"),
                  "tiktok": ("https://www.tiktok.com/@visionnzparty", "site"), "youtube": None, "linkedin": None},
    "free-palestine": {"website": ("https://palfree.nz/", "site"), "facebook": None, "instagram": None, "x": None, "tiktok": None, "youtube": None, "linkedin": None},
    "te-tai-tokerau-party": {"website": ("https://tetaitokerauparty.org.nz/", "site"),
                             "facebook": ("https://www.facebook.com/KapaKingi", "site"),   # the page the party site links to (its leader's page)
                             "instagram": ("https://www.instagram.com/tetaitokerauparty", "site"), "x": None, "tiktok": None, "youtube": None, "linkedin": None},
}
ACCOUNT_FIELDS = ["website", "facebook", "instagram", "x", "tiktok", "youtube", "linkedin"]


def log(*a): print(*a, file=sys.stderr, flush=True)


def fetch(url, cache_name, offline=False):
    """One GET with our UA; returns (bytes, error). Caches to raw/releases/cache/<cache_name>; --offline reads the cache."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, cache_name)
    if offline:
        if os.path.exists(path): return open(path, "rb").read(), None
        return None, "not cached"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/html;q=0.9, */*;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        open(path, "wb").write(data)
        time.sleep(PAUSE)
        return data, None
    except urllib.error.HTTPError as e:
        time.sleep(PAUSE); return None, f"HTTP {e.code}"
    except Exception as e:
        time.sleep(PAUSE); return None, type(e).__name__


def clean_text(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s*More\s*>>\s*$", "", s).strip()
    return s


def snippet(s, n=SUMMARY_CHARS):
    s = clean_text(s)
    if len(s) <= n: return s
    cut = s[:n].rsplit(" ", 1)[0].rstrip(" ,;:-–—")
    return cut + "…"


def nz_date(s):
    """'Friday, 23 October 2026,  1:44 pm' (Scoop InfoPage, NZ local time) -> ISO 8601 with offset."""
    s = re.sub(r"\s+", " ", s).strip()
    d = dt.datetime.strptime(s, "%A, %d %B %Y, %I:%M %p")
    return d.replace(tzinfo=NZ).isoformat(timespec="minutes")


def rfc822(s):
    from email.utils import parsedate_to_datetime
    try: return parsedate_to_datetime(s).astimezone(NZ).isoformat(timespec="minutes")
    except Exception: return None


def parse_infopage(data, party):
    """Scoop InfoPage -> items. Blocks look like:
       <div class="article-sections"><h3><a href="URL">Title</a></h3><p class="release">Friday, 23 October 2026,  1:44 pm | Org</p><p>teaser <a>More >></a></p></div>"""
    t = data.decode("utf-8", "ignore")
    items = []
    for blk in re.findall(r'<div class="article-sections">(.*?)</div>', t, flags=re.S):
        m = re.search(r'<h3>\s*<a href="(https?://www\.scoop\.co\.nz/stories/[^"]+)">(.*?)</a>\s*</h3>', blk, flags=re.S)
        r = re.search(r'<p class="release">(.*?)</p>', blk, flags=re.S)
        if not m or not r: continue
        when, _, byline = clean_text(r.group(1)).partition("|")
        try: date = nz_date(when)
        except ValueError: continue
        teaser = ""
        tm = re.search(r'<p class="release">.*?</p>\s*<p>(.*?)</p>', blk, flags=re.S)
        if tm: teaser = tm.group(1)
        items.append({"party": party["slug"], "title": clean_text(m.group(2)), "date": date, "url": m.group(1).strip(),
                      "summary": snippet(teaser), "source": "Scoop", "ministerial": False, "byline": byline.strip()})
    return items


def parse_rss(data):
    root = ET.fromstring(data)
    out = []
    for it in root.iter("item"):
        g = lambda tag: (it.findtext(tag) or "").strip()
        out.append({"title": clean_text(g("title")), "url": g("link"), "date": rfc822(g("pubDate")), "description": g("description")})
    return out


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f: return json.load(f)
    except (OSError, ValueError): return default


def content_key(doc):
    d = {k: v for k, v in doc.items() if k != "updated"}
    return hashlib.sha256(json.dumps(d, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def write_if_changed(path, doc, old):
    if old and content_key(old) == content_key(doc):
        log(f"{os.path.relpath(path, ROOT)}: no change"); return False
    doc["updated"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1); f.write("\n")
    log(f"{os.path.relpath(path, ROOT)}: written"); return True


# ----------------------------------------------------------------------------------------------------------------------- releases

def update_releases(offline=False, use_scoop=True):
    old = load_json(OUT, {})
    old_items = {i["url"]: i for i in old.get("items", []) if isinstance(i, dict) and i.get("url")}
    old_sources = {s["id"]: s for s in old.get("sources", []) if isinstance(s, dict) and s.get("id")}
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = (now - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    new_items = {}
    sources = []

    def src(id_, **kw):
        s = {"id": id_, **kw}
        sources.append(s); return s

    # 1. Scoop InfoPages, one per party (attribution: the page is the organisation's own listing).
    if use_scoop:
        for p in PARTIES:
            if not p["scoop"]:
                src(f"scoop:{p['slug']}", party=p["slug"], source="Scoop", feed_url=None, feed_type="none",
                    status="no Scoop InfoPage found for this party (names tried 2026-10-23)", items_in_feed=0,
                    newsroom_url=p["newsroom"], newsroom_verified=p["newsroom_verified"],
                    licence_or_terms_note="n/a; link to the party's own newsroom")
                continue
            url = f"https://info.scoop.co.nz/{p['scoop']}"
            data, err = fetch(url, f"scoop_{p['slug']}.html", offline)
            items = parse_infopage(data, p) if data else []
            if data and not items and b"Latest News" not in data: err = err or "page layout not recognised"
            for it in items: new_items.setdefault(it["url"], it)
            prev = old_sources.get(f"scoop:{p['slug']}", {})
            src(f"scoop:{p['slug']}", party=p["slug"], source="Scoop", feed_url=url, feed_type="html-infopage (no per-organisation RSS exists)",
                status="ok" if not err else f"error: {err} (kept previously stored items)", items_in_feed=len(items) if not err else prev.get("items_in_feed", 0),
                newsroom_url=p["newsroom"], newsroom_verified=p["newsroom_verified"],
                licence_or_terms_note="Scoop terms " + SCOOP_TERMS_URL + " (cl. 3.1 personal/non-commercial use with attribution; see terms_note)")
            log(f"scoop {p['slug']:22s} {('ok' if not err else err):28s} {len(items)} items")

        # 2. Scoop section RSS feeds: description text for items we can attribute (by URL) to a party.
        for sec, url in SCOOP_SECTION_FEEDS.items():
            data, err = fetch(url, f"scoop_section_{sec}.rss", offline)
            feed = []
            if data:
                try: feed = parse_rss(data)
                except ET.ParseError: err = "XML parse error"
            matched = 0
            for it in feed:
                tgt = new_items.get(it["url"]) or old_items.get(it["url"])
                if tgt is None: continue
                matched += 1
                if not tgt.get("summary") and it["description"]: tgt["summary"] = snippet(it["description"])
            src(f"scoop:section:{sec}", party=None, source="Scoop", feed_url=url, feed_type="rss (section feed; no organisation field)",
                status="ok" if not err else f"error: {err}", items_in_feed=len(feed), items_matched_to_a_party=matched,
                licence_or_terms_note="Scoop terms " + SCOOP_TERMS_URL + "; feed copyright line 'Scoop Media Ltd and/or its contributors'")
            log(f"scoop section {sec}: {('ok' if not err else err)} {len(feed)} items, {matched} matched to a party")

    # 3. Beehive: ministerial releases, tagged government.
    data, err = fetch(BEEHIVE_FEED, "beehive.rss", offline)
    feed = []
    if data:
        try: feed = parse_rss(data)
        except ET.ParseError: err = "XML parse error"
    n = 0
    for it in feed:
        if "/release/" not in it["url"] or not it["date"]: continue   # the feed also carries speeches
        n += 1
        new_items.setdefault(it["url"], {"party": "government", "title": it["title"], "date": it["date"], "url": it["url"],
                                         "summary": snippet(it["description"]), "source": "Beehive", "ministerial": True, "byline": "beehive.govt.nz"})
    src("beehive", party="government", source="Beehive", feed_url=BEEHIVE_FEED, feed_type="rss",
        status="ok" if not err else f"error: {err} (kept previously stored items)", items_in_feed=n,
        newsroom_url="https://www.beehive.govt.nz/releases", newsroom_verified=True,
        licence_or_terms_note="Crown copyright; beehive.govt.nz states a Creative Commons Attribution licence for its content (re-check https://www.beehive.govt.nz/copyright); headline + link + <=200-char snippet only")
    log(f"beehive: {('ok' if not err else err)} {n} releases")

    # 4. Merge: keep stored fields for known URLs (stability), add new ones, drop anything outside the window, de-dup by URL.
    merged = {}
    for url, it in old_items.items():
        merged[url] = it
    for url, it in new_items.items():
        if url in merged:
            cur = merged[url]
            if not cur.get("summary") and it.get("summary"): cur["summary"] = it["summary"]
            if not cur.get("title") and it.get("title"): cur["title"] = it["title"]
        else:
            merged[url] = it
    items = [i for i in merged.values() if i.get("date") and i["date"] >= cutoff and (i.get("party") == "government" or i.get("party") in PARTY_SLUGS)]
    for i in items:
        i["ministerial"] = bool(i.get("ministerial"))
        i["summary"] = i.get("summary") or ""
    items.sort(key=lambda i: (i["date"], i["url"]), reverse=True)

    per_party = {}
    for i in items: per_party[i["party"]] = per_party.get(i["party"], 0) + 1
    doc = {
        "updated": old.get("updated"),
        "_about": "Party press releases and ministerial releases: the party's or minister's own words, not fact-checked. Headline, date, link and a "
                  "short attributed snippet only; follow the link for the release. Default display should be equal slots per party (e.g. latest 3 "
                  "each), with a chronological view second, because large parties issue many times more releases than small ones. "
                  f"Items are kept for {WINDOW_DAYS} days and de-duplicated by URL. Built by tools/releases_update.py.",
        "window_days": WINDOW_DAYS,
        "election_date": "2026-11-07",
        "terms_note": TERMS_NOTE,
        "parties": {p["slug"]: {"name": p["name"], "website": p["website"], "newsroom_url": p["newsroom"], "newsroom_verified": p["newsroom_verified"],
                                "scoop_infopage": (f"https://info.scoop.co.nz/{p['scoop']}" if p["scoop"] else None)} for p in PARTIES},
        "counts": {"items": len(items), "per_party": dict(sorted(per_party.items()))},
        "sources": sources,
        "items": items,
    }
    return write_if_changed(OUT, doc, old)


# ------------------------------------------------------------------------------------------------------------------------- follow

JUNK = {"", "-", "–", "n/a", "na", "none", "no", "nil", "nope", "no < 3", "tbc", "coming soon"}
FIELD_MAP = {"website": "website", "facebook": "facebook", "instagram": "instagram", "twitter": "x", "x": "x", "tiktok": "tiktok",
             "youtube": "youtube", "linkedin": "linkedin"}
DOMAIN_FIELD = [("facebook.com", "facebook"), ("fb.com", "facebook"), ("fb.me", "facebook"), ("instagram.com", "instagram"),
                ("x.com", "x"), ("twitter.com", "x"), ("tiktok.com", "tiktok"), ("youtube.com", "youtube"), ("youtu.be", "youtube"),
                ("linkedin.com", "linkedin")]
TYPO_FIXES = [(r"^(?:https?:/*)?(?:www\.)?(?=https?:)", ""), (r"^(https?:/*)+", "https://"), (r"^https?//", "https://"), (r"^https?:(?!//)", "https://"),
              (r"^(https://)?(www\.)?labour\.co\.nz", "https://www.labour.org.nz"),
              (r"https://www\.instagram/", "https://www.instagram.com/"), (r"instgram\.com", "instagram.com"),
              (r"^(https://(?:www\.)?(?:facebook|instagram|x|twitter|tiktok|linkedin|youtube)\.com)(?=[A-Za-z0-9@_])", r"\1/"), (r"\?$", "")]
HANDLE_BASE = {"x": "https://x.com/{}", "instagram": "https://www.instagram.com/{}", "tiktok": "https://www.tiktok.com/@{}",
               "facebook": "https://www.facebook.com/{}"}
SOCIAL_DOMAIN_RE = re.compile(r"(^|[/.])(facebook|fb|instagram|x|twitter|tiktok|youtube|linkedin)\.(com|me)(/|$)", re.I)
SOCIAL_FIELDS = {"facebook", "instagram", "x", "tiktok", "youtube", "linkedin"}


def norm_url(raw, field):
    """Turn a questionnaire value into (field, https URL) or (None, None). The field is decided by the URL's domain, not by the
    questionnaire slot it was typed into. Bare @handles are expanded for X/Instagram/TikTok (the handle->URL mapping is exact);
    for Facebook only slash-free, space-free vanity names are expanded. Free text, pseudo-domains and 'n/a' answers are dropped."""
    v = (raw or "").strip().strip("<>").split(";")[0].strip()
    if v.lower() in JUNK or len(v) < 3 or " " in v: return None, None
    for pat, rep in TYPO_FIXES: v = re.sub(pat, rep, v)
    if not v.startswith("http"):
        if SOCIAL_DOMAIN_RE.search(v.split("/")[0]): v = "https://" + v           # www.facebook.com/x -> https://...
        elif field == "website" and re.match(r"^(www\.)?([a-z0-9-]+\.)+[a-z]{2,}(/|$)", v, flags=re.I): v = "https://" + v
    if v.startswith("https://"):
        for dom, f in DOMAIN_FIELD:
            if re.match(r"https://(www\.|m\.|mobile\.)?" + re.escape(dom) + r"(/|$)", v, flags=re.I):
                if f == "x": v = re.sub(r"https://(www\.|mobile\.)?(twitter|x)\.com", "https://x.com", v, flags=re.I)
                if "profile.php" not in v: v = v.split("?")[0].split("#")[0]      # drop ?hl=, ?stkn= tracking parameters
                if f == "x" and not re.match(r"^https://x\.com/[A-Za-z0-9_]{1,15}/?$", v): return None, None   # not a real X handle
                return f, v
        return ("website", v) if field == "website" else ("other", v)   # a social slot holding a personal site, Bluesky, Substack...
    if field not in HANDLE_BASE or "/" in v: return None, None
    h = v.lstrip("@")
    if re.match(r"^[A-Za-z0-9_]{1,15}$" if field == "x" else r"^[A-Za-z0-9_.]+$", h): return field, HANDLE_BASE[field].format(h)
    return None, None


def build_follow():
    people = []
    stats = {"people": 0, "with_any_account": 0, "fields": {f: 0 for f in ACCOUNT_FIELDS}, "other": 0, "email": 0, "dropped_values": 0,
             "by_status": {}}
    for pj in sorted(glob.glob(os.path.join(ROOT, "parties", "*", "people", "*", "person.json"))):
        d = load_json(pj, None)
        if not isinstance(d, dict): continue
        status = d.get("status", "")
        if status not in ("candidate-2026", "current-mp-standing-2026", "current-mp-retiring"): continue
        party = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(pj))))
        q = d.get("questionnaire_2026") if isinstance(d.get("questionnaire_2026"), dict) else {}
        acc = {f: None for f in ACCOUNT_FIELDS}; other = []
        for k, v in q.items():
            f = FIELD_MAP.get(k.strip().lower())
            if not f or not isinstance(v, str): continue
            nf, url = norm_url(v, f)
            if not url:
                if v.strip().lower() not in JUNK: stats["dropped_values"] += 1
                continue
            if nf == "other": other.append(url)
            elif acc.get(nf) is None: acc[nf] = url
            elif url.rstrip("/").lower() != acc[nf].rstrip("/").lower(): other.append(url)   # second account on the same platform
        email = (q.get("Public email") or "").strip()
        email = email if re.match(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", email, flags=re.I) else None
        rec = {"slug": d.get("slug") or os.path.basename(os.path.dirname(pj)), "party": party, "name": d.get("name", ""),
               "folder": os.path.relpath(os.path.dirname(pj), ROOT), "status": status,
               "electorate_2026": d.get("electorate_2026"), "list_rank_2026": d.get("list_rank_2026"),
               "accounts": acc, "other": sorted({o for o in other if o.rstrip("/").lower() not in {u.rstrip("/").lower() for u in acc.values() if u}}),
               "email": email,
               "source": "policy.nz 2026 candidate questionnaire (candidate-supplied), via person.json" if q else "no questionnaire on file",
               "verified": False}
        people.append(rec)
        stats["people"] += 1; stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        if any(acc.values()) or other: stats["with_any_account"] += 1
        for f in ACCOUNT_FIELDS:
            if acc[f]: stats["fields"][f] += 1
        stats["other"] += len(rec["other"]); stats["email"] += 1 if email else 0
    people.sort(key=lambda r: (r["name"].split()[-1].lower() if r["name"] else "", r["name"].lower()))

    parties = {}
    for p in PARTIES:
        a = PARTY_ACCOUNTS[p["slug"]]
        parties[p["slug"]] = {"name": p["name"], "newsroom_url": p["newsroom"],
                              "accounts": {f: (a[f][0] if a.get(f) else None) for f in ACCOUNT_FIELDS},
                              "verified": {f: (a[f][1] == "site" if a.get(f) else None) for f in ACCOUNT_FIELDS},
                              "account_sources": {f: (a[f][1] if a.get(f) else None) for f in ACCOUNT_FIELDS}}
    doc = {
        "updated": None,
        "_about": "Outbound links to official accounts only: the same fields for every party and every 2026 candidate / current MP, "
                  "alphabetical by surname, no follower counts, no embeds. Party accounts were read from the party's own website on "
                  "2026-10-23 where it could be reached (verified true); where the site blocks automated access the account comes from "
                  "the party's Wikidata item and is marked verified false. People's accounts are the ones they supplied to the policy.nz "
                  "2026 candidate questionnaire (via person.json), normalised to https URLs, not independently verified; free-text and "
                  "'n/a' answers are dropped. A platform outside the fixed set (Bluesky, Mastodon, Substack...) goes in `other`. "
                  "Report a wrong link with the Correction issue template. Built by tools/releases_update.py --follow.",
        "fields": ACCOUNT_FIELDS,
        "parties": parties,
        "people": people,
        "coverage": stats,
    }
    old = load_json(FOLLOW_OUT, {})
    return write_if_changed(FOLLOW_OUT, doc, old)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--offline", action="store_true", help="re-parse raw/releases/cache/ without network access")
    ap.add_argument("--no-scoop", action="store_true", help="skip Scoop; Beehive + newsroom links only")
    ap.add_argument("--follow", action="store_true", help="rebuild data/guide/follow.json instead of the releases feed")
    a = ap.parse_args()
    if a.follow:
        build_follow()
    else:
        update_releases(offline=a.offline, use_scoop=not a.no_scoop)


if __name__ == "__main__":
    main()

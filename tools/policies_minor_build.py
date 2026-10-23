"""Build parties/<party>/policies/policies.json and README.md for TOP (opportunity) and every minor party /
electorate-only group, from tools/policies_minor_catalog.py + the documents written by
tools/policies_minor_opportunity_fetch.py and tools/policies_minor_sites_fetch.py.
Run: python3 -I tools/policies_minor_build.py
"""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policies_minor_lib as L
from policies_minor_catalog import CATALOG, META, OPP_RELATED

ROOT = L.ROOT
GROUPS = json.load(open(os.path.join(ROOT, "raw", "policy.nz", "party-vote-election.json")))["topicsList"]
GROUP_NAMES = {
    "community-and-inclusion": "Community & inclusion", "defence-and-foreign-affairs": "Defence & foreign affairs",
    "economy": "Economy", "education": "Education", "environment": "Environment", "health": "Health",
    "housing": "Housing", "incomes-and-employment": "Incomes & employment",
    "law-justice-and-government": "Law, justice & government", "media-culture-and-recreation": "Media, culture & recreation",
    "migration": "Migration", "te-ao-maori": "Te ao Māori", "transport-and-infrastructure": "Transport & infrastructure"}
TOPIC_ALIASES = {"animal-welfare": "community-and-inclusion"}


def front_matter(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", txt, re.S)
    fm = {}
    for line in (m.group(1).split("\n") if m else []):
        k, _, v = line.partition(": ")
        v = v.strip()
        if v.startswith('"'):
            try:
                v = json.loads(v)
            except Exception:
                pass
        fm[k] = v
    fm["_retrievable"] = "**Not retrievable.**" not in txt
    fm["_words"] = len(txt.split())
    return fm


def docs_of(party):
    d = os.path.join(ROOT, "parties", party, "policies", "documents")
    out = {}
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".md"):
                out[f[:-3]] = front_matter(os.path.join(d, f))
    return out


def anchor(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def group_of(p):
    for t in p["topics"]:
        if t in GROUPS:
            return t
    return TOPIC_ALIASES.get(p["topics"][0], "community-and-inclusion")


def src(docs, slug):
    fm = docs[slug]
    return {"title": fm.get("title", slug), "url": fm.get("source_url"), "document": f"documents/{slug}.md"}


def build_party(party, policies, docs, meta, pnz_count=0):
    json_out = []
    for p in policies:
        e = {"id": p["id"], "statement": p["statement"], "topics": p["topics"], "topic_group": p.get("topic_group") or group_of(p),
             "key_policy": bool(p.get("key")), "summary": {"why": p.get("why"), "how": p.get("how")},
             "summary_source": p.get("summary_source", "archive"),
             "sources": p.get("sources") or [src(docs, s) for s in p["docs"]]}
        for k in ("policy_nz_citations", "note"):
            if p.get(k):
                e[k] = p[k]
        json_out.append(e)
    L.write_json(party, json_out)
    write_readme(party, json_out, docs, meta, pnz_count)
    return len(json_out)


def write_readme(party, pols, docs, meta, pnz_count):
    name = meta["name"]
    n_ret = sum(1 for d in docs.values() if d["_retrievable"])
    n_unret = len(docs) - n_ret
    Lr = [f"# {name} — 2026 election policies", ""]
    counts = f"**{len(pols)} policies** listed"
    if pnz_count:
        counts += f" ({pnz_count} from [policy.nz](https://policy.nz/2026/party-vote/parties/opportunity-party), {len(pols) - pnz_count} added by this archive from the party's own documents)"
    Lr.append(f"Every policy of **{name}** for the 7 November 2026 general election that this archive could find: {counts}, "
              f"backed by **{n_ret} full-text source document{'s' if n_ret != 1 else ''}**"
              + (f" and {n_unret} documented-as-unretrievable source{'s' if n_unret != 1 else ''}" if n_unret else "") + ".")
    Lr.append("")
    facts = []
    if meta.get("website"):
        facts.append(f"Party website: <{meta['website']}>")
    if meta.get("registered"):
        facts.append(f"Registration: {meta['registered']}")
    if facts:
        Lr += ["- " + f for f in facts] + [""]
    Lr += ["## About this list", "", meta["intro"], ""]
    Lr += ["**Method.** Pages and PDFs were downloaded on 2026-10-23 by "
           "[`tools/policies_minor_sites_fetch.py`](../../../tools/policies_minor_sites_fetch.py) / "
           "[`tools/policies_minor_opportunity_fetch.py`](../../../tools/policies_minor_opportunity_fetch.py) "
           "(raw copies in `raw/party-docs/" + party + "/`) and reduced to their main text in [`documents/`](documents/) "
           "(markup and whitespace normalised only). The list and summaries are built by "
           "[`tools/policies_minor_build.py`](../../../tools/policies_minor_build.py) from "
           "[`tools/policies_minor_catalog.py`](../../../tools/policies_minor_catalog.py).", ""]
    if pnz_count:
        Lr += ["Summaries marked *policy.nz* are policy.nz's neutral \"This party says…\" text, reproduced unchanged. "
               "Summaries marked *archive* were written for this archive from the linked full text: one to three neutral "
               "sentences; \"Why\" is the party's own stated reason, \"How\" what it says it would do.", ""]
    else:
        Lr += ["policy.nz publishes no policy statements for this party, so every summary here is marked *archive*: "
               "written for this archive from the linked full text in one to three neutral sentences (\"Why\" = the "
               "party's own stated reason, attributed; \"How\" = what it says it would do). Party claims (costs, "
               "statistics) are reported as the party's claims, not verified.", ""]
    if meta.get("gaps"):
        Lr += ["**Gaps and caveats.** " + meta["gaps"], ""]
    keys = [p for p in pols if p["key_policy"]]
    if keys:
        Lr += ["## Headline policies", ""]
        Lr += [f"- [{p['statement']}](#{anchor(p['statement'] + ' ' + p['id'])}) — {GROUP_NAMES.get(p['topic_group'], p['topic_group'])}" for p in keys]
        Lr.append("")
    grouped = collections.OrderedDict((g, []) for g in GROUPS)
    for p in pols:
        grouped.setdefault(p["topic_group"], []).append(p)
    grouped = collections.OrderedDict((g, ps) for g, ps in grouped.items() if ps)
    if pols:
        Lr += ["## Contents by topic", ""]
        for g, ps in grouped.items():
            Lr.append(f"- [{GROUP_NAMES.get(g, g)}](#{anchor(GROUP_NAMES.get(g, g))}) ({len(ps)})")
        Lr.append("")
        for g, ps in grouped.items():
            Lr += [f"## {GROUP_NAMES.get(g, g)}", ""]
            for p in ps:
                Lr += [f"### {p['statement']} ({p['id']})", ""]
                tag = "policy.nz" if p["summary_source"] == "policy.nz" else "archive"
                if p["summary"].get("why"):
                    Lr += [f"**Why** (*{tag}*): {p['summary']['why'].strip()}", ""]
                if p["summary"].get("how"):
                    Lr += [f"**How** (*{tag}*): {p['summary']['how'].strip()}", ""]
                if p.get("note"):
                    Lr += [f"*Note:* {p['note']}", ""]
                links = []
                for s in p["sources"]:
                    if s.get("document"):
                        links.append(f"[{s['title']}]({s['document']}) ([original]({s['url']}))" if s.get("url") else f"[{s['title']}]({s['document']})")
                    else:
                        links.append(f"[{s['title']}]({s['url']})")
                Lr += ["Full text: " + "; ".join(links), ""]
    else:
        Lr += ["## Policies", "", "_No published policy statements could be found for this group (see Gaps above)._", ""]
    Lr += ["## Source documents", "", "| Document | Original | Words | Status |", "| --- | --- | --- | --- |"]
    for slug, d in docs.items():
        st = "full text" if d["_retrievable"] else "**not retrievable**"
        Lr.append(f"| [{d.get('title', slug)}](documents/{slug}.md) | [link]({d.get('source_url')}) | {d['_words']} | {st} |")
    Lr.append("")
    Lr += ["---", "", "_Summaries describe what the party says it would do; they are not endorsements or fact-checks._", ""]
    p = os.path.join(ROOT, "parties", party, "policies", "README.md")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write("\n".join(Lr))


def opportunity():
    party = "opportunity"
    docs = docs_of(party)
    idx = json.load(open(os.path.join(L.raw_dir(party), "doc-index.json")))
    url2slug = {u: d.split("/")[-1][:-3] for u, d in idx.items()}
    d = json.load(open(os.path.join(ROOT, "raw/policy.nz/parties/opportunity-party.json")))
    pols = []
    for pol in d["policies"]:
        attrs = {a["name"]: a["value"] for a in pol.get("attributes", [])}
        topics = list(dict.fromkeys(pol["topics"]))
        key = any(t.startswith("key-policies-") for t in topics)
        tg = next((t[len("key-policies-"):] for t in topics if t.startswith("key-policies-")), None) or next((t for t in topics if t in GROUPS), None)
        sources, seen = [], set()
        for c in pol.get("citations", []):
            orig = re.sub(r"^https?://web\.archive\.org/web/\d+/", "", c["url"])
            orig = re.sub(r"^/web/\d+/", "", orig).rstrip("/")
            slug = url2slug.get(orig) or url2slug.get(orig.replace("%20", " "))
            if not slug:
                for u, s in url2slug.items():
                    if u.rstrip("/").split("/")[-1].lower() == orig.split("/")[-1].lower():
                        slug = s
            if slug and slug in docs:
                if slug not in seen:
                    seen.add(slug)
                    sources.append({"title": c["title"], "url": orig, "document": f"documents/{slug}.md", "cited_by": "policy.nz"})
            else:
                sources.append({"title": c["title"], "url": orig, "cited_by": "policy.nz",
                                "note": "cited by policy.nz; not a TOP document (or not archived here)"})
        for slug in OPP_RELATED.get(pol["reference"], []):
            if slug not in seen:
                seen.add(slug)
                sources.append(dict(src(docs, slug), cited_by="archive"))
        pols.append({"id": pol["reference"], "statement": pol["statement"].strip(), "topics": [t for t in topics if not t.startswith("key-policies-")],
                     "topic_group": tg, "key": key, "why": attrs.get("Why", "").strip() or None, "how": attrs.get("How", "").strip() or None,
                     "summary_source": "policy.nz", "sources": sources, "docs": []})
    n_pnz = len(pols)
    for p in CATALOG.get(party, []):
        pols.append(dict(p, sources=[dict(src(docs, s), cited_by="archive") for s in p["docs"]]))
    return build_party(party, pols, docs, META[party], pnz_count=n_pnz)


def main():
    counts = {}
    counts["opportunity"] = opportunity()
    for party, meta in META.items():
        if party == "opportunity":
            continue
        docs = docs_of(party)
        pols = CATALOG.get(party, [])
        for p in pols:
            for s in p["docs"]:
                assert s in docs, (party, p["id"], s)
        counts[party] = build_party(party, pols, docs, meta)
    for k, v in counts.items():
        print(f"{k}: {v} policies, {len(docs_of(k))} documents")


if __name__ == "__main__":
    main()

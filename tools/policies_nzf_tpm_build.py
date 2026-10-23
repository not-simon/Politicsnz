#!/usr/bin/env python3
"""Build parties/{nz-first,te-pati-maori}/policies/{policies.json,README.md,documents/*.md}.

Inputs: raw/policy.nz/parties/{nz-first,te-pati-maori}.json, raw/party-docs/<party>/scoop/*.html (party press
releases mirrored on Scoop), raw/party-docs/<party>/*.pdf, and tools/policies_nzf_tpm_config.py.
Run: python3 -I tools/policies_nzf_tpm_build.py   (from the repo root)
"""
import json, os, re, sys, datetime
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import policies_nzf_tpm_config as C
from policies_nzf_tpm_extract import extract
from policies_nzf_tpm_pdftext import pdf_text

PARTIES = {
    "nz-first": dict(name="New Zealand First", short="NZ First", pnz="nz-first", scoop=C.NZF_SCOOP, pdfs=C.NZF_PDFS,
                     map=C.NZF_MAP, extra=C.NZF_EXTRA, headline=C.NZF_HEADLINE, signature=C.NZF_SIGNATURE,
                     site="nzfirst.nz", scoop_org="https://info.scoop.co.nz/New_Zealand_First_Party"),
    "te-pati-maori": dict(name="Te Pāti Māori", short="Te Pāti Māori", pnz="te-pati-maori", scoop=C.TPM_SCOOP,
                          pdfs=C.TPM_PDFS, map=C.TPM_MAP, extra=C.TPM_EXTRA, headline=C.TPM_HEADLINE,
                          signature=C.TPM_SIGNATURE, site="maoriparty.org.nz",
                          scoop_org="https://info.scoop.co.nz/Te_Pati_Maori"),
}
BLOCK_REASON = ("{site} returns HTTP 403 (Cloudflare bot challenge) to direct requests and to a headless Chromium "
                "browser (tools/fetch_page.js), tested 23 October 2026. The Internet Archive (web.archive.org) "
                "snapshot cited by policy.nz could not be fetched either: connections to web.archive.org are reset "
                "by this environment's network proxy. No other copy of this page's text was found.")

def slugify(s, n=70):
    s = s.lower()
    for a, b in {"ā": "a", "ē": "e", "ī": "i", "ō": "o", "ū": "u", "’": "", "'": "", "“": "", "”": ""}.items():
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:n].rstrip("-")

def gh_anchor(s):
    """GitHub heading anchor: lowercase, drop punctuation (keep letters incl. macrons, digits, space, -, _), spaces -> -."""
    return re.sub(r"[^\w\- ]", "", s.lower(), flags=re.UNICODE).replace(" ", "-")

def orig_url(u):
    u = u.strip()
    m = re.search(r"(?:web\.archive\.org)?/(?:web/\d+[a-z_]*|save)/(https?://.+)$", u)
    if m and "/save/" in u:     # a "save page now" request URL, not an archived snapshot
        return m.group(1).strip(), None
    return (m.group(1) if m else u).strip(), (u if m else None)

def yaml_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'

def front(d):
    return "---\n" + "".join(f"{k}: {yaml_str(v)}\n" for k, v in d.items() if v is not None) + "---\n\n"

def parse_byline_date(b):
    m = re.search(r"(\d{1,2}) (\w+) (\d{4})", b)
    return datetime.datetime.strptime(" ".join(m.groups()), "%d %B %Y").date().isoformat() if m else ""

def build(party):
    P = PARTIES[party]
    base = os.path.join(ROOT, "parties", party, "policies"); docdir = os.path.join(base, "documents")
    os.makedirs(docdir, exist_ok=True)
    for f in os.listdir(docdir):        # rebuild: remove files this script generated earlier
        if f.endswith(".md"): os.remove(os.path.join(docdir, f))
    docs = OrderedDict()   # key -> dict(slug,title,url,kind,date)

    # --- Scoop press releases / speeches
    for code in P["scoop"]:
        html = open(os.path.join(ROOT, "raw/party-docs", party, "scoop", code + ".html"), encoding="utf-8", errors="replace").read()
        meta, text, pdfs, links = extract(html)
        byline = " ".join(meta["byline"].split())
        date = parse_byline_date(byline)
        kind = "Speech" if "Speech:" in byline else "Press release"
        m = re.search(r'URL:(\S+)', html)
        path = m.group(1) if m else code.replace("-", "/")
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        url = canon.group(1) if canon else f"https://www.scoop.co.nz/stories/{path}"
        slug = f"{date}-{slugify(meta['title'], 60)}"
        docs["scoop:" + code] = dict(slug=slug, title=meta["title"], url=url, date=date, kind=kind)
        body = front(OrderedDict(title=meta["title"], party=party, source_url=url, published=date,
                                 retrieved=C.RETRIEVED, format="html", fetch_method="curl (direct HTTP GET of scoop.co.nz)",
                                 mirror="scoop.co.nz",
                                 note=f"{kind} issued by {P['name']} and republished verbatim by Scoop; the text is the party's own. "
                                      f"The party's own website ({P['site']}) blocks automated access, so Scoop is used as the mirror."))
        body += f"# {meta['title']}\n\n*{byline}* — [{url}]({url})\n\n"
        if pdfs:
            body += "Attachments linked in the release: " + ", ".join(f"[{p.strip()}]({p.strip()})" for p in pdfs) + "\n\n"
        body += "## Full text\n\n" + text.strip() + "\n"
        open(os.path.join(docdir, slug + ".md"), "w").write(body)

    # --- PDFs
    for fn, (title, url, note) in P["pdfs"].items():
        pages = pdf_text(os.path.join(ROOT, "raw/party-docs", party, fn))
        slug = "pdf-" + slugify(os.path.splitext(fn)[0].replace("drive-", ""), 60)
        docs["pdf:" + fn] = dict(slug=slug, title=title, url=url, date="", kind="PDF")
        body = front(OrderedDict(title=title, party=party, source_url=url, retrieved=C.RETRIEVED, format="pdf",
                                 fetch_method="curl download; text extracted with `pdftotext -raw` (tools/policies_nzf_tpm_pdftext.py)",
                                 local_copy=f"raw/party-docs/{party}/{fn}", note=note))
        body += f"# {title}\n\nSource: [{url}]({url}). {note}\n\n"
        body += ("> Extraction notes: text is reproduced in the PDF's content-stream order, page by page. Only whitespace and "
                 "glyph markup were normalised (bullet glyphs shown as •, decorative icons removed). Designed layouts mean "
                 "page headers, side labels and table cells can appear out of visual order; consult the PDF for layout. "
                 "No words were added, removed or reworded.\n\n")
        body += "## Full text\n\n"
        for n, pg in enumerate(pages, 1):
            body += f"### Page {n}\n\n```text\n{pg}\n```\n\n"
        open(os.path.join(docdir, slug + ".md"), "w").write(body)

    # --- policy.nz items
    pnz = json.load(open(os.path.join(ROOT, "raw/policy.nz/parties", P["pnz"] + ".json")))
    blocked = OrderedDict()
    policies = []
    for p in pnz["policies"]:
        pid = p["reference"]
        group, dockeys, note = P["map"][pid]
        attrs = {a["name"]: a["value"].strip() for a in p.get("attributes") or []}
        topics = list(OrderedDict.fromkeys(t for t in (p.get("topics") or [])))
        sources = []
        used = set()
        for c in p.get("citations") or []:
            title = " ".join((c.get("title") or "").split())
            o, arch = orig_url(c.get("url") or "")
            src = {"title": title, "url": o}
            if arch: src["archived_url"] = ("https://web.archive.org" + arch) if arch.startswith("/web") else arch
            host = re.sub(r"^https?://(www\.)?", "", o).split("/")[0]
            direct = None
            for k, d in docs.items():
                if k.startswith("scoop:") and k[6:].replace("-", "/") in o:
                    direct = k
                if k.startswith("pdf:") and (d["url"].rstrip("/") == o.rstrip("/") or (("drive.google.com" in o) and k[4:].split("-")[-1].split(".")[0] in o)):
                    direct = k
            if "community.scoop.co.nz" in o:
                src["note"] = "Same release as the Scoop copy listed below."
            elif direct:
                src["document"] = "documents/" + docs[direct]["slug"] + ".md"; used.add(direct)
            elif host in (P["site"],):
                bslug = "not-retrieved-" + slugify(host.split(".")[0] + "-" + o.split(host, 1)[1], 70)
                blocked.setdefault(o, dict(slug=bslug, title=title, arch=src.get("archived_url"), policies=[]))["policies"]
                if pid not in blocked[o]["policies"]: blocked[o]["policies"].append(pid)
                src["document"] = "documents/" + bslug + ".md"; src["retrieved"] = False
            else:
                src["note"] = "Not an %s source (cited by policy.nz); not archived here." % P["short"]
            sources.append(src)
        for k in dockeys:
            if k in used: continue
            d = docs[k]
            sources.append({"title": f"{d['title']} ({d['kind']}{', ' + d['date'] if d['date'] else ''})", "url": d["url"],
                            "document": "documents/" + d["slug"] + ".md",
                            "note": "Party's own text on this policy (found by this archive; not cited by policy.nz)."})
        policies.append(OrderedDict(id=pid, statement=p["statement"].strip(), topics=topics, group=group,
                                    summary={"why": attrs.get("Why", ""), "how": attrs.get("How", "")},
                                    summary_source="policy.nz", sources=sources, **({"note": note} if note else {})))
    for x in P["extra"]:
        sources = []
        for k in x["docs"]:
            d = docs[k]
            sources.append({"title": f"{d['title']} ({d['kind']}{', ' + d['date'] if d['date'] else ''})", "url": d["url"],
                            "document": "documents/" + d["slug"] + ".md"})
        for t, u in C.EXTRA_LINKS.get(x["id"], []):
            sources.append({"title": t, "url": u, "note": "News coverage (not party text)."})
        e = OrderedDict(id=x["id"], statement=x["statement"], topics=x["topics"], group=x["group"],
                        summary={"why": x["why"], "how": x["how"]}, summary_source="archive", sources=sources)
        if x.get("note"): e["note"] = x["note"]
        policies.append(e)

    # --- not-retrieved documents
    for o, b in blocked.items():
        body = front(OrderedDict(title=b["title"], party=party, source_url=o, retrieved=C.RETRIEVED, format="html",
                                 fetch_method="not-retrieved", archived_url=b["arch"]))
        body += f"# {b['title']}\n\nSource page: <{o}>" + (f"  \nArchived copy cited by policy.nz: <{b['arch']}>" if b["arch"] else "") + "\n\n"
        body += "## Full text\n\n**Not retrieved.** " + BLOCK_REASON.format(site=P["site"]) + "\n\n"
        body += "The full text of this page is therefore **not** reproduced here, and nothing in this file is a paraphrase of it.\n\n"
        related = OrderedDict()
        for pol in policies:
            if pol["id"] in b["policies"]:
                for s in pol["sources"]:
                    if s.get("document") and not s["document"].startswith("documents/not-retrieved"):
                        related[s["document"]] = s["title"]
        body += "Policies that cite this page: " + ", ".join(f"`{i}`" for i in b["policies"]) + ".\n\n"
        if related:
            body += "Other party-published texts on the same policies that *were* retrieved (they may differ from this page):\n\n"
            body += "".join(f"- [{t}]({d[len('documents/'):]})\n" for d, t in related.items())
        else:
            body += "No other party-published text on these policies was found.\n"
        open(os.path.join(docdir, b["slug"] + ".md"), "w").write(body)

    json.dump(policies, open(os.path.join(base, "policies.json"), "w"), ensure_ascii=False, indent=1)
    write_readme(party, P, policies, docs, blocked, base)
    return policies, docs, blocked

def write_readme(party, P, policies, docs, blocked, base):
    n_pnz = sum(1 for p in policies if p["summary_source"] == "policy.nz")
    n_arc = len(policies) - n_pnz
    with_text = [p for p in policies if any(s.get("document") and "not-retrieved" not in s["document"] for s in p["sources"])]
    no_text = [p for p in policies if p not in with_text]
    groups = OrderedDict()
    for p in policies: groups.setdefault(p["group"], []).append(p)
    groups = OrderedDict(sorted(groups.items()))
    byid = {p["id"]: p for p in policies}
    anchor = lambda p: gh_anchor(f"{p['id']}: {p['statement']}")
    L = []
    L.append(f"# {P['name']} — 2026 election policies\n")
    L.append(f"Every 2026 policy of {P['name']} that this archive could find, with a short neutral summary (**Why** — the "
             f"reason the party gives; **How** — what it would do) and links to the **full verbatim text** of the party's own "
             f"documents in [`documents/`](documents/). Election day: 7 November 2026. Compiled 23 October 2026.\n")
    L.append("## At a glance\n")
    L.append(f"- **{len(policies)} policies** listed: {n_pnz} from [policy.nz](https://policy.nz) (all of its {n_pnz} {P['short']} "
             f"statements, with its Why/How summaries) + {n_arc} more found in the party's own releases, speeches and policy PDFs "
             f"(marked *archive*; summaries written for this archive).")
    L.append(f"- **{len(docs)} full-text documents** archived ({sum(1 for d in docs.values() if d['kind']!='PDF')} press releases/speeches, "
             f"{sum(1 for d in docs.values() if d['kind']=='PDF')} PDFs) + {len(blocked)} placeholder files for cited pages that could not be retrieved.")
    L.append(f"- {len(with_text)} policies have at least one retrieved party text; {len(no_text)} rely only on a page that could not be retrieved.\n")
    L.append("## Method & sources\n")
    L.append(f"1. Started from policy.nz's {P['short']} data (`raw/policy.nz/parties/{P['pnz']}.json`): statement, Why/How, citations.")
    L.append(f"2. {P['site']} blocks automated access (Cloudflare 403, also with a headless browser) and web.archive.org is unreachable "
             f"from this environment, so the cited party web pages could not be fetched.")
    L.append(f"3. Instead, every {P['name']} press release and speech from late 2025 to 23 Oct 2026 was collected from Scoop's "
             f"organisation page ({P['scoop_org']}); Scoop republishes party releases as issued, so their text is the party's own. "
             f"Policy PDFs the party attached to releases (img.scoop.co.nz) or linked from its site (Google Drive) were downloaded "
             f"and text-extracted.")
    L.append("4. Each policy links (a) the page policy.nz cited and (b) the party's own retrieved text on the same policy. Where policy.nz "
             "cited a blocked page, a `documents/not-retrieved-*.md` file records the URL and the reason; it contains no paraphrase.")
    L.append("5. Policies found in party texts but missing from policy.nz were added with neutral summaries (`summary_source: archive`). "
             "Calls on the current government and positions (e.g. opposing a bill) are included where the party presents them as what it stands for, and are labelled as such.\n")
    L.append("### Retrieval gaps (read this)\n")
    L.append(f"- **{len(blocked)} {P['site']} pages cited by policy.nz were not retrieved** (403 / archive unreachable). "
             "Where a party release covers the same policy it is linked, but the website page may contain details the release does not.")
    for o, b in blocked.items():
        L.append(f"  - [{b['title']}](documents/{b['slug']}.md) — <{o}> (policies: {', '.join(b['policies'])})")
    if party == "te-pati-maori":
        L.append("- The party's 2026 *Policy Manifesto* appears to be published as separate chapter PDFs (the Tax and Justice chapters carry "
                 "\"Te Pāti Māori Policy Manifesto 2026\" headers and page numbers 3–7 and 27–30). Only the Tax, Justice, Te Tiriti Entrenchment, "
                 "Energy Sovereignty and Kai Sovereignty documents were found; other chapters (health, housing, education, disability, "
                 "climate, foreign affairs, te reo, etc.) were not locatable without access to maoriparty.org.nz.")
        L.append("- No Te Pāti Māori statement of formal coalition \"bottom lines\" was retrieved (NZ First's leader said TPM called its tax policy a \"bottom line\"). The web-search budget for this session ran out before further news coverage could be checked.")
    else:
        L.append("- The $100bn Future Fund and Paris Agreement withdrawal announcements were found only as references in the leader's speeches; "
                 "no stand-alone release or policy page for them was retrievable.")
        L.append("- Member's bill texts on parliament.nz / legislation.govt.nz (e.g. Māori seats referendum, IMSB disestablishment, fireworks, "
                 "container return) could not be fetched (bot-protection); the party releases describing them are archived instead. "
                 "The two bill drafts NZ First attached to releases (anti-scam; accessibility) are archived as PDFs.")
        L.append("- policy.nz's citation for POL55077 (nutrition-guidelines review) points to an unrelated NZ First release (Mill Road); the correct party text is linked as well.")
    L.append("")
    L.append("## Headline commitments & stated conditions\n")
    for h, q, d in P["headline"]:
        ds = d if isinstance(d, list) else [d]
        L.append(f"- **{h}:** {q} — " + ", ".join(f"[source](documents/{docs[k]['slug']}.md)" for k in ds))
    L.append("\n**Signature policies:** " + "; ".join(f"[{byid[i]['statement']}](#{anchor(byid[i])})" for i in P["signature"] if i in byid) + ".\n")
    L.append("## Contents\n")
    for g, ps in groups.items():
        L.append(f"- [{g}](#{gh_anchor(g)}) ({len(ps)})")
    L.append("- [Document index](#document-index)\n")
    for g, ps in groups.items():
        L.append(f"## {g}\n")
        for p in ps:
            L.append(f"### {p['id']}: {p['statement']}\n")
            L.append(f"**Statement:** {p['statement']}  ")
            shown = [t for t in p['topics'] if not t.startswith('key-policies')]
            L.append(f"*Summary source: {p['summary_source']}* · topics: {', '.join(shown[:6])}\n")
            L.append(f"- **Why:** {p['summary']['why'] or '—'}")
            L.append(f"- **How:** {p['summary']['how'] or '—'}")
            if p.get("note"): L.append(f"- **Note:** {p['note']}")
            L.append("- **Sources:**")
            for s in p["sources"]:
                line = f"  - [{s['title']}]({s['url']})"
                if s.get("document"):
                    line += (" — full text **not retrieved** ([why](%s))" % s["document"]) if s.get("retrieved") is False else (f" — [full text]({s['document']})")
                if s.get("archived_url"): line += f" · [archived copy cited by policy.nz]({s['archived_url']})"
                if s.get("note") and "Party's own text" not in s["note"]: line += f" — {s['note']}"
                L.append(line)
            L.append("")
    L.append("## Document index\n")
    L.append("| Date | Type | Document | Original |\n|---|---|---|---|")
    for k, d in sorted(docs.items(), key=lambda kv: kv[1]["date"] or "0"):
        L.append(f"| {d['date'] or '—'} | {d['kind']} | [{d['title']}](documents/{d['slug']}.md) | [link]({d['url']}) |")
    for o, b in blocked.items():
        L.append(f"| — | Not retrieved | [{b['title']}](documents/{b['slug']}.md) | [link]({o}) |")
    L.append("")
    open(os.path.join(base, "README.md"), "w").write("\n".join(L))

if __name__ == "__main__":
    for party in PARTIES:
        pol, docs, blocked = build(party)
        print(party, "policies", len(pol), "policy.nz", sum(p["summary_source"] == "policy.nz" for p in pol),
              "archive", sum(p["summary_source"] == "archive" for p in pol), "docs", len(docs), "not-retrieved", len(blocked))

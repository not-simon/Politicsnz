"""Fetch the full text of every 2026 policy page/PDF published by the minor parties and electorate-only groups,
and write parties/<slug>/policies/documents/*.md (verbatim, markup normalised only).

Run: python3 -I tools/policies_minor_sites_fetch.py [party ...]
Raw downloads are cached in raw/party-docs/<slug>/. A doc index (url -> document path, title) is written to
raw/party-docs/<slug>/doc-index.json for the catalogue builder (tools/policies_minor_build.py).
"""
import html, json, os, re, subprocess, sys
from urllib.parse import urljoin
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policies_minor_lib as L

UA_NOTE = "curl (desktop Chrome user-agent)"


def slugify(s, n=70):
    s = html.unescape(s).lower()
    s = re.sub(r"[āàáâä]", "a", s); s = re.sub(r"[ēèéêë]", "e", s); s = re.sub(r"[īìíîï]", "i", s)
    s = re.sub(r"[ōòóôö]", "o", s); s = re.sub(r"[ūùúûü]", "u", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:n].strip("-")


def wp_json(base, route, slug):
    url = f"{base}/wp-json/wp/v2/{route}"
    path, code = L.fetch(url, slug, ext=".json")
    if not path:
        raise SystemExit(f"{url}: HTTP {code}")
    return json.load(open(path, encoding="utf-8"))


def page_doc(party, docslug, url, title=None, selectors=("main", "article", "#content", ".content", "body"),
             drop=("header", "nav", "footer"), note=None, method=UA_NOTE, cut_after=None, cut_before=None):
    path, code = L.fetch(url, party)
    if not path:
        L.write_doc(party, docslug, title or url, url, None, note=f"Could not be retrieved: HTTP {code} on {L.RETRIEVED}.")
        return None
    t, md = L.main_md(path, selectors=selectors, drop=drop)
    if cut_before and cut_before in md:
        md = md[md.index(cut_before):]
    if cut_after and cut_after in md:
        md = md[:md.index(cut_after)]
    rel = L.write_doc(party, docslug, title or t, url, md, method=method, note=note)
    return {"url": url, "doc": rel, "title": title or t}


def pdf_doc(party, docslug, url, title, note=None):
    path, code = L.fetch(url, party, ext=".pdf")
    if not path:
        L.write_doc(party, docslug, title, url, None, fmt="pdf", note=f"Could not be retrieved: HTTP {code} on {L.RETRIEVED}.")
        return None
    rel = L.write_doc(party, docslug, title, url, L.pdf_md(path), fmt="pdf", method="curl + pdftotext -layout",
                      note=(note or "") + " Text extracted from the party's PDF with pdftotext; bullets normalised to "
                      "Markdown, page breaks shown as horizontal rules; images/graphics not reproduced.")
    return {"url": url, "doc": rel, "title": title}


def save_index(party, items):
    items = [i for i in items if i]
    json.dump(items, open(os.path.join(L.raw_dir(party), "doc-index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(party, len(items), "documents")


# ---------------------------------------------------------------- Animal Justice (WordPress, CPT "policies")
def animal_justice():
    P, base = "animal-justice", "https://animaljustice.org.nz"
    items = []
    items.append(page_doc(P, "election-2026-manifesto", base + "/election-2026/election-manifesto/", "Election 2026 Manifesto",
                          selectors=("#brx-content", "main")))
    for sl, ti in [("policy-framework", "Policy Framework"), ("what-shapes-our-policy", "What Shapes Our Policy")]:
        items.append(page_doc(P, sl, f"{base}/policy/{sl}/", ti, selectors=("#brx-content", "main")))
    pols = wp_json(base, "policies?per_page=100", P)
    try:
        cats = {c["id"]: html.unescape(c["name"]) for c in wp_json(base, "policy-category?per_page=100", P)}
    except SystemExit:
        cats = {}
    meta = []
    for p in pols:
        title = html.unescape(p["title"]["rendered"])
        link = p["link"]
        docslug = "policy-" + slugify(p["slug"] if not re.match(r"^\d", p["slug"]) else title)
        web_md = L.html_to_md(L.soup_from_html(p["content"]["rendered"]))
        # the rendered page holds the 'View PDF Version' link
        hp, _ = L.fetch(link, P)
        pdfs = []
        if hp:
            for h, t in L.links(hp, link):
                if h.lower().endswith(".pdf") and "animaljustice.org.nz/wp-content" in h and h not in pdfs:
                    pdfs.append(h)
        body = ["### Web page text", "", web_md.strip()]
        for u in pdfs:
            pp, code = L.fetch(u, P, ext=".pdf")
            body += ["", f"### PDF version: {u}", ""]
            body.append(L.pdf_md(pp).strip() if pp else f"**PDF not retrievable (HTTP {code}).**")
        rel = L.write_doc(P, docslug, title, link, "\n".join(body), method="WordPress REST API (content.rendered) + curl for linked PDF",
                          note="Web text is the policy post body from animaljustice.org.nz/wp-json/wp/v2/policies; the PDF "
                               "version linked from the page (if any) follows, extracted with pdftotext -layout.",
                          extra={"published": p["date"], "modified": p["modified"],
                                 "categories": [cats.get(c, c) for c in p.get("policy-category", [])]})
        meta.append({"url": link, "doc": rel, "title": title, "slug": p["slug"], "pdfs": pdfs,
                     "categories": [cats.get(c, c) for c in p.get("policy-category", [])], "modified": p["modified"]})
    save_index(P, items + meta)


# ---------------------------------------------------------------- Alliance (WordPress posts)
ALLIANCE_POLICY_POSTS = [
    "alliance-tax-plan-first-20000-income-tax-free", "alliance-full-employment-35-hour-week-workers-rights-policy",
    "alliance-environment-climate-sustainable-economy-policy", "alliance-health-policy-free-gp-dental-optical-audiology",
    "alliance-national-transport-strategy", "alliance-plan-to-rebuild-universal-social-security",
    "alliance-52-weeks-paid-parental-leave-gender-equality", "alliance-small-business-local-enterprise-cooperatives",
    "alliance-justice-policy-three-strikes-into-treatment", "alliance-plan-to-eliminate-child-poverty",
    "the-right-to-a-roof-alliance-housing-policy", "alliance-retirement-aged-care-kiwisaver-policy",
    "alliance-te-tiriti-democracy-constitutional-policy", "open-not-owned-alliance-trade-policy",
    "alliance-public-ownership-economic-democracy-policy", "alliance-foreign-affairs-defence-international-relations-policy",
    "alliance-calls-for-universal-child-benefit", "alliance-party-prepares-for-2026-general-election-campaign-at-conference",
    "we-are-back-to-fight-for-working-people-in-2026",
]


def alliance():
    P, base = "alliance", "https://allianceparty.nz"
    items = []
    posts = {p["slug"]: p for p in wp_json(base, "posts?per_page=100", P)}
    pages = {p["slug"]: p for p in wp_json(base, "pages?per_page=100", P)}
    for sl in ["what-we-stand-for", "health-policy"]:
        p = pages[sl]
        md = L.html_to_md(L.soup_from_html(p["content"]["rendered"]))
        rel = L.write_doc(P, "page-" + sl, html.unescape(p["title"]["rendered"]), p["link"], md,
                          method="WordPress REST API (content.rendered)", extra={"modified": p["modified"]})
        items.append({"url": p["link"], "doc": rel, "title": html.unescape(p["title"]["rendered"])})
    for sl in ALLIANCE_POLICY_POSTS:
        p = posts[sl]
        title = html.unescape(p["title"]["rendered"])
        md = L.html_to_md(L.soup_from_html(p["content"]["rendered"]))
        rel = L.write_doc(P, "post-" + p["date"][:10] + "-" + slugify(sl, 50), title, p["link"], md,
                          method="WordPress REST API (content.rendered)", extra={"published": p["date"], "modified": p["modified"]})
        items.append({"url": p["link"], "doc": rel, "title": title, "date": p["date"][:10]})
    save_index(P, items)


# ---------------------------------------------------------------- simple single/multi page sites
def legalise_cannabis():
    P = "legalise-cannabis"
    items = [page_doc(P, "full-spectrum-policy", "https://www.alcp.org.nz/policy", "Full Spectrum Policy (ALCP policy page)")]
    save_index(P, items)


def vision_nz():
    P = "vision-nz"
    items = [page_doc(P, "vision-policies", "https://www.vision.org.nz/visionpolicies", "Vision NZ — Our Policies")]
    save_index(P, items)


def te_tai_tokerau():
    P = "te-tai-tokerau-party"
    items = [page_doc(P, "ttp-pataka-policy", "https://tetaitokerauparty.org.nz/our-policies/", "TTP Pātaka Policy (Our Policies)")]
    save_index(P, items)


def conservative():
    P, b = "conservative", "https://www.conservatives.nz"
    pages = [("policy", "Our Policies"), ("we-stand-for", "What We Stand For"), ("principles", "Our Principles"),
             ("small-government", "Smaller Government"), ("familybuilder-old", "Family Values"),
             ("news/new-policies-announcement", None), ("news/police-policy-announcement", None),
             ("news/has-new-zealand-failed-its-oceans", None), ("news/has-new-zealand-lost-control-of-its-own-government", None),
             ("news/policy-clarification-on-rural%2C-environmental%2C-and-agricultural-issues", None),
             ("news/press-release---improving-access-to-justice-for-self-represented-litigants", None),
             ("news/sharpening-the-teeth-of-the-ipca", None)]
    items = []
    for sl, ti in pages:
        items.append(page_doc(P, slugify(sl.replace("news/", "news-").replace("%2C", "")), f"{b}/{sl}", ti))
    save_index(P, items)


def womens_rights():
    P, b = "womens-rights", "https://womensrightsparty.nz"
    items = [page_doc(P, "policy", b + "/policy/", "Policy"), page_doc(P, "our-priorities", b + "/our-priorities/", "Our Priorities")]
    lp, _ = L.fetch(b + "/policy/", P)
    props = []
    for h, t in L.links(lp, b + "/policy/"):
        if "/policy-proposal/" in h and h.rstrip("/") != b + "/policy-proposal" and h not in props:
            props.append(h)
    for u in props:
        items.append(page_doc(P, "proposal-" + slugify(u.rstrip("/").split("/")[-1], 60), u))
    docx = b + "/wp-content/uploads/2025/11/POLICY-Womens-Rights-Party-2025-041125.docx"
    dp, code = L.fetch(docx, P, ext=".docx")
    if dp:
        md = subprocess.run(["pandoc", "-f", "docx", "-t", "gfm", "--wrap=none", dp], capture_output=True, text=True).stdout
        items.append({"url": docx, "title": "Women's Rights Party Full Policy (Word document, Nov 2025)",
                      "doc": L.write_doc(P, "full-policy-docx-2025", "Women's Rights Party Full Policy (Word document, 4 Nov 2025)",
                                         docx, md, fmt="docx", method="curl + pandoc docx->gfm",
                                         note="The party's downloadable full policy document, converted to Markdown with pandoc.")})
    save_index(P, items)


def outdoors_freedom():
    P, b = "nz-outdoors-freedom", "https://freedom.kiwi"
    items = [page_doc(P, "home", b + "/", "freedom — home page (core platform)"),
             page_doc(P, "policies", b + "/policies", "Policies")]
    lp, _ = L.fetch(b + "/policies", P)
    seen = []
    skip = ("home", "our-", "2026-c", "wise", "actions", "media", "submis", "petit", "discus", "the-kiwi", "shop",
            "contact", "join", "donate", "user_", "policies")
    for h, t in L.links(lp, b + "/policies"):
        tail = h.replace(b + "/", "")
        if h.startswith(b + "/") and tail and not tail.startswith(skip) and "@" not in tail and h not in seen:
            seen.append(h)
            items.append(page_doc(P, slugify(tail), h, t or None))
    save_index(P, items)


def free_palestine():
    P = "free-palestine"
    items = [page_doc(P, "palfree-home-objectives-principles", "https://palfree.nz/",
                      "Palestine Free from the River to the Sea Party — Objectives and Founding Principles",
                      cut_after="Take Action",
                      note="Captured from the party's one-page website. The page continues after the principles with a "
                           "membership form, electoral-enrolment instructions and donation bank details; those non-policy "
                           "sections are omitted here (see source_url).")]
    items.append(pdf_doc(P, "constitution-june-2026", "https://elections.nz/assets/Party-rules/FPP-Constitution-June-2026.pdf",
                         "Free Palestine Party Constitution (June 2026, as lodged with the Electoral Commission)"))
    sp, code = L.fetch("https://www.scoop.co.nz/stories/PO2608/S00073/the-free-palestine-party-the-newest-political-party-in-aotearoa.htm", P)
    if sp:
        t, by, md = L.scoop_md(sp)
        items.append({"url": "https://www.scoop.co.nz/stories/PO2608/S00073/the-free-palestine-party-the-newest-political-party-in-aotearoa.htm",
                      "title": t, "doc": L.write_doc(P, "release-2026-08-newest-political-party", t,
                      "https://www.scoop.co.nz/stories/PO2608/S00073/the-free-palestine-party-the-newest-political-party-in-aotearoa.htm",
                      md, method="curl (scoop.co.nz)", note=f"Press release as published on Scoop. Byline: {by}.")})
    save_index(P, items)


def nz_loyal():
    P = "nz-loyal"
    rnz = "https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election"
    note = ("NZ Loyal's registered website, nzloyal.com, returns HTTP 403 (Cloudflare bot challenge) to curl and to "
            "headless Chromium on 2026-10-23; newzealandloyal.com only redirects to a parking 'lander' page; "
            "web.archive.org is unreachable from this environment. The party's own policy pages could therefore NOT be "
            "captured. The only verbatim party wording available is the list RNZ quoted from the party website "
            "(12 Oct 2026), reproduced below exactly as RNZ printed it.")
    path, code = L.fetch(rnz, "_shared")
    s = L.soup(path)
    txt = s.select_one("article").get_text("\n", strip=True)
    m = re.search(r"New Zealand Loyal\nWhat they say about themselves\n?: ?(.*?)\nWhat to know:", txt, re.S)
    quoted = m.group(0).replace("\n", " ") if m else None
    body = ("### As quoted by RNZ (\"Explainer: What you need to know about the smaller political parties in this year's "
            "election\", 12 October 2026)\n\n" + (quoted.split("What to know:")[0].strip() if quoted else "(quote not found)"))
    items = [{"url": "https://nzloyal.com/", "title": "nzloyal.com (blocked)",
              "doc": L.write_doc(P, "nzloyal-com-not-retrievable", "New Zealand Loyal website (nzloyal.com) — policies",
                                 "https://nzloyal.com/", None, method="curl and headless Chromium both blocked", note=note)},
             {"url": rnz, "title": "RNZ quotation of NZ Loyal's stated policies",
              "doc": L.write_doc(P, "rnz-quote-of-party-website", "NZ Loyal's policies as quoted from its website by RNZ",
                                 rnz, body, method="curl (rnz.co.nz)", note="Secondary source: RNZ's verbatim quotation of the "
                                 "party's website. This is not the party's full policy text, which could not be retrieved.")}]
    save_index(P, items)


def progressive():
    P = "progressive-aotearoa-new-zealand"
    b = "https://www.progressiveparty.co.nz"
    items = [page_doc(P, "policies", b + "/policies-3/", "Policies"), page_doc(P, "manifesto", b + "/ppanz-manifesto/", "PPANZ Manifesto")]
    save_index(P, items)


def nap():
    P = "nap"
    items = [page_doc(P, "media-release-2026-10-07-exit-politics", "https://nap.org.nz/", "Not A Party has a radical proposal — leave politics behind (media release, 7 Oct 2026)"),
             page_doc(P, "principles", "https://nap.org.nz/principles/", "Principles", cut_after="## One reply"),
             page_doc(P, "beyond-democracy", "https://nap.org.nz/beyond-democracy/", "Beyond Democracy", cut_after="## One reply")]
    save_index(P, items)


def seg():
    P = "socialist-equality-group"
    u = "https://www.wsws.org/en/articles/2026/10/14/cjbj-o14.html"
    items = [page_doc(P, "election-statement-2026-10-13", u, "Fight against war and for international socialism! (SEG election statement, 13 Oct 2026)",
                      selectors=("article", "main"), cut_after="Read more")]
    save_index(P, items)


ALL = {"animal-justice": animal_justice, "alliance": alliance, "legalise-cannabis": legalise_cannabis,
       "vision-nz": vision_nz, "te-tai-tokerau-party": te_tai_tokerau, "conservative": conservative,
       "womens-rights": womens_rights, "nz-outdoors-freedom": outdoors_freedom, "free-palestine": free_palestine,
       "nz-loyal": nz_loyal, "progressive-aotearoa-new-zealand": progressive, "nap": nap, "socialist-equality-group": seg}

if __name__ == "__main__":
    for k in (sys.argv[1:] or ALL):
        ALL[k]()

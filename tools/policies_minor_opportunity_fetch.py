"""Opportunity (TOP): build parties/opportunity/policies/documents/ from
 - policy PDFs on cdn.opportunity.org.nz (reachable; www.opportunity.org.nz is Cloudflare-blocked),
 - TOP press releases mirrored on scoop.co.nz,
 - www.opportunity.org.nz pages recovered from Common Crawl WARC captures (tools/policies_minor_cc.py; the live
   site is Cloudflare-blocked), and explicit "not retrievable" stubs for cited pages with no Common Crawl capture.
Run: python3 -I tools/policies_minor_opportunity_fetch.py
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policies_minor_lib as L

P = "opportunity"
CDN = "https://cdn.opportunity.org.nz/documents/policy/"
PDFS = [  # (doc slug, title, file name on CDN)
    ("pdf-tax-reset", "Tax Reset (policy document)", "Opportunity Policy - Tax Reset.pdf"),
    ("pdf-abundant-energy", "Abundant Energy (policy document)", "Opportunity Policy - Abundant Energy.pdf"),
    ("pdf-climate-action", "Climate Action (policy document)", "Opportunity Policy - Climate Action.pdf"),
    ("pdf-affordable-housing", "Affordable Housing (policy document)", "Opportunity Policy - Affordable Housing.pdf"),
    ("pdf-smart-on-crime", "Smart on Crime (policy document)", "Opportunity Policy - Smart on Crime.pdf"),
    ("pdf-clean-up-politics", "Clean Up Politics (policy document)", "Opportunity Policy - Clean Up Politics.pdf"),
    ("pdf-intergenerational-infrastructure", "Intergenerational Infrastructure (policy document)", "Opportunity Policy - Intergenerational Infrastructure.pdf"),
    ("pdf-breakthrough-economy", "Breakthrough Economy (policy overview)", "breakthrough-economy-policy-overview.pdf"),
    ("pdf-citizens-voice", "Citizens' Voice (policy document)", "citizens-voice-policy.pdf"),
    ("pdf-healthy-oceans", "Healthy Oceans (policy document)", "oceans-policy.pdf"),
    ("pdf-abundant-energy-paper", "Abundant Energy - Opportunity Party Policy (policy paper)", "Abundant Energy - Opportunity Party Policy.pdf"),
    ("pdf-future-fit-education", "Future-Fit Education Policy Paper", "Future-Fit Education Policy Paper.pdf"),
    ("pdf-honouring-te-tiriti", "Honouring Te Tiriti Policy Paper", "Honouring Te Tiriti Policy Paper.pdf"),
    ("pdf-digital-future", "Digital Future (policy document)", "Opportunity Policy - Digital Future.pdf"),
    ("pdf-tax-reset-transition-plan", "Tax Reset Transition Plan (policy document)", "Opportunity Policy - Tax Reset Transition Plan.pdf"),
]
CC_SKIP = {"statements"}  # index page only
SCOOP = [  # (doc slug, url)
    ("release-2026-02-state-of-the-nation", "https://www.scoop.co.nz/stories/PO2602/S00118/we-are-the-next-generation-of-leaders-says-qiulae-wong.htm"),
    ("release-2026-04-healthy-oceans-dunedin", "https://www.scoop.co.nz/stories/PO2604/S00041/opportunity-party-candidate-david-bainbridge-zafar-champions-healthy-oceans-policy-for-dunedin.htm"),
    ("release-2026-04-free-public-transport", "https://www.scoop.co.nz/stories/PO2604/S00050/its-time-for-permanent-free-public-transport.htm"),
    ("release-2026-05-tax-reset", "https://www.scoop.co.nz/stories/PO2605/S00043/opportunitys-tax-reset-the-largest-tax-cut-for-low-income-working-kiwis-in-history.htm"),
    ("release-2026-06-mp-allowances", "https://www.scoop.co.nz/stories/PO2606/S00107/opportunity-mps-will-not-use-taxpayer-funded-allowances-to-build-private-property-wealth.htm"),
    ("release-2026-07-breakthrough-economy", "https://www.scoop.co.nz/stories/PO2607/S00015/innovation-fairness-and-small-business-opportunitys-breakthrough-economy-policy.htm"),
    ("release-2026-08-intergenerational-infrastructure", "https://www.scoop.co.nz/stories/PO2608/S00027/opportunity-launches-intergenerational-infrastructure-policy.htm"),
]

BLOCK_NOTE = ("www.opportunity.org.nz returns HTTP 403 (Cloudflare 'Just a moment...' bot challenge) to curl and to "
              "headless Chromium (tools/fetch_page.js) as of 2026-10-23, and web.archive.org (where policy.nz archived "
              "this page) is not reachable from this environment (connection reset). The page's text is therefore NOT "
              "reproduced here. Where the same policy is published as a PDF on cdn.opportunity.org.nz or as a press "
              "release on scoop.co.nz, see the linked documents. policy.nz's own summary of what this page says is "
              "recorded in ../policies.json (summary_source: policy.nz).")


def site_stub_slug(url):
    path = url.split("opportunity.org.nz/")[-1].strip("/")
    return "web-" + re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")


def main():
    index = {}
    for slug, title, fn in PDFS:
        url = CDN + fn.replace(" ", "%20")
        path, code = L.fetch(url, P, ext=".pdf")
        if not path:
            L.write_doc(P, slug, title, url, None, fmt="pdf", note=f"Download failed (HTTP {code}).")
            continue
        body = L.pdf_md(path)
        L.write_doc(P, slug, title, url, body, fmt="pdf", method="curl + pdftotext -layout (poppler)",
                    note="Text extracted from the party's PDF with pdftotext; page furniture (headers/footers, page "
                         "numbers) is kept as extracted; bullets normalised to Markdown and page breaks shown as horizontal rules. Layout, images, charts and tables-as-graphics are not reproduced.")
        index[url] = "documents/" + slug + ".md"
    for slug, url in SCOOP:
        path, code = L.fetch(url, P)
        if not path:
            L.write_doc(P, slug, slug, url, None, note=f"Download failed (HTTP {code}).")
            continue
        title, byline, md = L.scoop_md(path)
        L.write_doc(P, slug, title, url, md, method="curl (scoop.co.nz mirror of party press release)",
                    note=f"Press release as published on Scoop. Byline: {byline}. Advertising and Scoop page furniture removed.")
        index[url] = "documents/" + slug + ".md"
    # stubs for every party web page cited by policy.nz
    d = json.load(open(os.path.join(L.ROOT, "raw/policy.nz/parties/opportunity-party.json")))
    pages = set()
    for pol in d["policies"]:
        for c in pol.get("citations", []):
            u = c["url"]
            orig = re.sub(r"^https?://web\.archive\.org/web/\d+/", "", u)
            orig = re.sub(r"^/web/\d+/", "", orig)
            if "www.opportunity.org.nz" in orig or orig.startswith("https://opportunity.org.nz"):
                pages.add(orig.rstrip("/"))
    ccdir = os.path.join(L.raw_dir(P), "cc-html")
    ccidx = json.load(open(os.path.join(ccdir, "index.json"))) if os.path.exists(os.path.join(ccdir, "index.json")) else {}
    for path, meta in ccidx.items():
        if path in CC_SKIP or meta["file"].endswith(".pdf"):
            continue
        orig = "https://www.opportunity.org.nz/" + path
        pages.add(orig)
    for orig in sorted(pages):
        slug = site_stub_slug(orig)
        path = orig.split("opportunity.org.nz/")[-1].strip("/")
        meta = ccidx.get(path)
        if meta:
            t, md = L.main_md(os.path.join(ccdir, meta["file"]), selectors=("main", "#content", "body"))
            ts = meta["timestamp"]
            cap = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}"
            L.write_doc(P, slug, t.replace(" - The Opportunity Party", "").strip() or path, orig, md,
                        method="Common Crawl WARC capture (tools/policies_minor_cc.py); live site Cloudflare-blocked",
                        note=f"Text of www.opportunity.org.nz/{path} as captured by Common Crawl on {cap} "
                             f"({meta['timestamp']}, {meta['warc'].split('/')[1]}). The live page may have changed since.",
                        extra={"captured": cap, "cc_timestamp": meta["timestamp"], "cc_warc": meta["warc"]})
        else:
            L.write_doc(P, slug, "opportunity.org.nz: /" + path, orig, None,
                        method="curl, headless Chromium and Common Crawl all failed", note=BLOCK_NOTE +
                        " No Common Crawl capture (CC-MAIN-2026-30/34/39/43) with HTTP 200 exists for this URL.")
        index[orig] = "documents/" + slug + ".md"
    json.dump(index, open(os.path.join(L.raw_dir(P), "doc-index.json"), "w"), indent=1)
    print(len(index), "documents")


if __name__ == "__main__":
    main()

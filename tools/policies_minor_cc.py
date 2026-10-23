"""Common Crawl access for Cloudflare-blocked minor-party sites (opportunity.org.nz, nzloyal.com).
Adapted from tools/policies_green_cc_index.py / policies_green_cc_fetch.py (static cluster.idx + cdx shards; WARC
byte ranges from data.commoncrawl.org).

  python3 -I tools/policies_minor_cc.py index <party> <surt-key> CC-MAIN-2026-43 [...]
      e.g. index opportunity 'nz,org,opportunity)/' CC-MAIN-2026-30 CC-MAIN-2026-34 CC-MAIN-2026-39 CC-MAIN-2026-43
  python3 -I tools/policies_minor_cc.py fetch <party> <regex-on-path> [...]
      saves raw/party-docs/<party>/cc-html/<path>.html, metadata in raw/party-docs/<party>/cc-html/index.json
"""
import glob, gzip, json, os, re, sys, time, urllib.request, zlib

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw", "party-docs")


def get(url, rng=None, tries=10):
    for i in range(tries):
        try:
            h = {"User-Agent": "PoliticsNZResearch/1.0"}
            if rng:
                h["Range"] = "bytes=%d-%d" % rng
            return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=180).read()
        except Exception as e:
            print("  retry", i, e, file=sys.stderr)
            time.sleep(2 + i * 2)
    raise SystemExit("failed " + url)


def index(party, key, crawls):
    out_dir = os.path.join(ROOT, party, "cc")
    os.makedirs(out_dir, exist_ok=True)
    for c in crawls:
        base = f"https://data.commoncrawl.org/cc-index/collections/{c}/indexes/"
        lines = get(base + "cluster.idx").decode().splitlines()
        sel = [i for i, l in enumerate(lines) if l.startswith(key)]
        if not sel:
            sel = [max(i for i, l in enumerate(lines) if l.split("\t")[0] < key)]
        else:
            sel = [sel[0] - 1] + sel
        out = []
        for i in sel:
            k, shard, off, ln, _ = lines[i].split("\t")
            raw = get(base + shard, (int(off), int(off) + int(ln) - 1))
            for row in zlib.decompress(raw, 16 + zlib.MAX_WBITS).decode().splitlines():
                if not row.startswith(key):
                    continue
                surt, ts, js = row.split(" ", 2)
                d = json.loads(js)
                out.append({"url": d["url"], "status": d.get("status"), "timestamp": ts, "filename": d["filename"],
                            "offset": d["offset"], "length": d["length"], "mime": d.get("mime", ""), "redirect": d.get("redirect")})
        open(os.path.join(out_dir, c + ".jsonl"), "w").write("\n".join(json.dumps(x) for x in out) + "\n")
        print(c, len(sel), "blocks", len(out), "captures", flush=True)


def fetch(party, pats):
    d = os.path.join(ROOT, party)
    html = os.path.join(d, "cc-html")
    os.makedirs(html, exist_ok=True)
    idxf = os.path.join(html, "index.json")
    idx = json.load(open(idxf)) if os.path.exists(idxf) else {}
    caps = {}
    for f in glob.glob(os.path.join(d, "cc", "*.jsonl")):
        for l in open(f):
            if not l.startswith("{"):
                continue
            x = json.loads(l)
            if x.get("status") != "200":
                continue
            m = re.match(r"https?://[^/]+/?(.*)$", x["url"])
            path = m.group(1).split("?")[0].split("#")[0].rstrip("/")
            if "?" in x["url"] and path in caps:
                continue
            if path in caps and caps[path]["timestamp"] >= x["timestamp"]:
                continue
            caps[path] = x
    pats = [re.compile(p) for p in pats]
    for path, x in sorted(caps.items()):
        if not any(p.search(path) for p in pats):
            continue
        if path in idx and idx[path]["timestamp"] >= x["timestamp"]:
            continue
        off, ln = int(x["offset"]), int(x["length"])
        data = None
        for i in range(10):
            try:
                req = urllib.request.Request("https://data.commoncrawl.org/" + x["filename"],
                                             headers={"Range": f"bytes={off}-{off+ln-1}", "User-Agent": "PoliticsNZResearch/1.0"})
                data = gzip.decompress(urllib.request.urlopen(req, timeout=120).read())
                break
            except Exception as e:
                print("retry", path, e, file=sys.stderr)
                time.sleep(2 + i)
        if data is None:
            print("FAIL", path)
            continue
        body = data.split(b"\r\n\r\n", 2)[2]
        ext = ".pdf" if "pdf" in x.get("mime", "") or path.lower().endswith(".pdf") else ".html"
        fn = (re.sub(r"[^A-Za-z0-9_.-]", "_", path) or "index")[:150] + ("" if fn_has(path, ext) else ext)
        open(os.path.join(html, fn), "wb").write(body)
        idx[path] = {"file": fn, "url": x["url"], "timestamp": x["timestamp"], "warc": x["filename"], "mime": x.get("mime")}
        print("ok", path, x["timestamp"], len(body))
        json.dump(idx, open(idxf, "w"), indent=1)


def fn_has(path, ext):
    return path.lower().endswith(ext)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "index":
        index(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif cmd == "fetch":
        fetch(sys.argv[2], sys.argv[3:])

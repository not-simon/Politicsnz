#!/usr/bin/env python3
"""Fetch raw wikitext of English Wikipedia articles used as finding aids / date checks for
data/onthisday.json. Saves to raw/onthisday/wikipedia/<title>.wikitext (untrusted data).

Usage: python3 tools/onthisday_wiki_fetch.py "Title 1" "Title 2" ...
       python3 tools/onthisday_wiki_fetch.py --from-file titles.txt
Retries politely on HTTP 429 (Wikipedia's rate limiter) and skips titles already fetched.
"""
import json, os, sys, time, urllib.parse, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "raw", "onthisday", "wikipedia")
UA = "PoliticsNZResearch/1.0 (personal research; simongeorgebrown@gmail.com)"


def safe_name(title):
    return urllib.parse.quote(title.replace(" ", "_"), safe="") + ".wikitext"


def fetch(title, tries=8):
    url = ("https://en.wikipedia.org/w/index.php?title=" + urllib.parse.quote(title.replace(" ", "_"))
           + "&action=raw")
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "replace"), r.geturl()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(1.5 + attempt * 1.5)
                continue
            if e.code == 404:
                return None, url
            raise
        except Exception:
            time.sleep(2 + attempt)
    return None, url


def main(argv):
    os.makedirs(OUT, exist_ok=True)
    titles = []
    if argv and argv[0] == "--from-file":
        titles = [l.strip() for l in open(argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
    else:
        titles = argv
    index_path = os.path.join(OUT, "_index.json")
    index = json.load(open(index_path)) if os.path.exists(index_path) else {}
    for t in titles:
        fn = safe_name(t)
        path = os.path.join(OUT, fn)
        if os.path.exists(path):
            continue
        text, url = fetch(t)
        if text is None:
            print("MISSING", t, file=sys.stderr)
            index[t] = {"file": None, "status": "missing"}
            continue
        # follow redirects in wikitext
        if text.lstrip().lower().startswith("#redirect"):
            import re
            m = re.search(r"\[\[([^\]|#]+)", text)
            if m:
                target = m.group(1).strip()
                text2, _ = fetch(target)
                if text2:
                    text = text2
                    index[t] = {"file": fn, "redirect_to": target}
        open(path, "w", encoding="utf-8").write(text)
        index.setdefault(t, {})
        index[t].update({"file": fn, "status": "ok", "retrieved": time.strftime("%Y-%m-%d"),
                         "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(t.replace(" ", "_"))})
        print("ok", t, len(text), file=sys.stderr)
        time.sleep(0.7)
    json.dump(index, open(index_path, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1:])

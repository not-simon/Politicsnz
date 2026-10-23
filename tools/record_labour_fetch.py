#!/usr/bin/env python3
"""Fetch Wikipedia plaintext extracts used for the Labour track-record research into raw/record/labour/."""
import json, sys, time, urllib.request, urllib.error, urllib.parse, pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "raw/record/labour"
UA = "PoliticsNZResearch/1.0 (personal research)"
def fetch(title):
    q = urllib.parse.urlencode({"action":"query","prop":"extracts","explaintext":1,"titles":title,"format":"json","redirects":1})
    req = urllib.request.Request("https://en.wikipedia.org/w/api.php?"+q, headers={"User-Agent":UA})
    for i in range(5):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=60)); break
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(10*(i+1))
    time.sleep(3)
    page = next(iter(d["query"]["pages"].values()))
    txt = page.get("extract","")
    fn = OUT / (title.replace(" ","_").replace("/","-")+".txt")
    fn.write_text(txt)
    print(title, len(txt))
if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for t in sys.argv[1:]: fetch(t)

import json, os, sys
base = os.path.dirname(os.path.abspath(__file__))
g = {}
for f in ("part1.py", "part2.py", "part3.py"):
    exec(open(os.path.join(base, f)).read(), g)

PARTIES = ["national","labour","green","act","nz-first","te-pati-maori","opportunity","nz-loyal","nz-outdoors-freedom","legalise-cannabis","animal-justice","alliance","conservative","womens-rights","vision-nz","free-palestine","te-tai-tokerau-party"]
data = {"national": g["national"], "labour": g["labour"], "green": g["green"], "act": g["act"], "nz-first": g["nzf"],
        "te-pati-maori": g["tpm"], "opportunity": g["top"], "nz-loyal": g["nz_loyal"], "nz-outdoors-freedom": g["ofp"],
        "legalise-cannabis": g["alcp"], "animal-justice": g["ajp"], "alliance": g["alliance"], "conservative": g["conservative"],
        "womens-rights": g["wrp"], "vision-nz": g["vision"], "free-palestine": g["free_palestine"], "te-tai-tokerau-party": g["ttp"]}

ids = [s[0] for s in g["STATEMENTS"]]
for p, d in data.items():
    for k in d:
        assert k in ids, (p, k)
    for k, v in d.items():
        if v is not None:
            assert v["position"] in (-2,-1,0,1,2), (p,k)
            assert v["tier"] in (1,2,3,4,5), (p,k)
            assert v["confidence"] in ("high","medium","low"), (p,k)
            assert v["source_url"].startswith("http"), (p,k)

out = {"coder": "B", "date": "2026-10-23",
       "scale": "-2 strongly disagree, -1 disagree, 0 argued neutral (three EUvox cases or vote/statement contradiction), +1 agree, +2 strongly agree, null = no public position found. Positions are the party's relative to the statement text as written.",
       "evidence_tiers": {"1": "2026 manifesto/policy text", "2": "recorded parliamentary vote 2023-26", "3": "party's own questionnaire answer (Greenpeace, NZCTU, Grey Power, KPMG tracker)", "4": "dated leader/spokesperson statement", "5": "coalition agreement or government action attributable to the party (flagged)"},
       "notes": "raw/quiz2/coder-b/NOTES.md",
       "statements": []}
counts = {p: 0 for p in PARTIES}
for sid, text, pol in g["STATEMENTS"]:
    pos = {}
    for p in PARTIES:
        cell = data[p].get(sid)
        pos[p] = cell
        if cell is not None:
            counts[p] += 1
    out["statements"].append({"id": sid, "text": text, "polarity": pol, "positions": pos})
out["coverage"] = counts
path = "/home/user/Politicsnz/data/guide/quiz2-coder-b.json"
os.makedirs(os.path.dirname(path), exist_ok=True)
json.dump(out, open(path, "w"), ensure_ascii=False, indent=1)
print(json.dumps(counts, indent=0))
# distribution check
from collections import Counter
cnt = Counter()
for s in out["statements"]:
    for p, cell in s["positions"].items():
        cnt[None if cell is None else cell["position"]] += 1
print(cnt)

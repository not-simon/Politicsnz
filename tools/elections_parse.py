"""Parsers for Wikipedia election pages (raw/elections/*)."""
import io, re, os, warnings
import pandas as pd
import mwparserfromhell as mw
from elections_common import RAW, clean, party_slug, to_int
warnings.filterwarnings("ignore")

def electorates_from_wikitext(path):
    txt = open(path).read()
    # strip refs first so templates parse cleanly
    txt = re.sub(r"<ref[^>/]*/>", "", txt)
    txt = re.sub(r"<ref[^>]*>.*?</ref>", "", txt, flags=re.S)
    code = mw.parse(txt)
    out = []
    maori_mode = False
    for t in code.filter_templates(recursive=False):
        nm = str(t.name).strip().lower()
        if not nm.startswith("nz electorate result ") or nm.endswith("start") or nm.endswith("end"):
            continue
        kind = nm.replace("nz electorate result ", "")
        g = lambda k: clean(t.get(k).value) if t.has(k) else ""
        winner = g("winner") or g("incumbent")
        wparty = g("winner-party") or g("incumbent-party")
        if kind == "hold":
            winner, wparty = g("incumbent"), g("incumbent-party")
            if g("winner"): winner, wparty = g("winner"), g("winner-party") or wparty
        e = {"name": g("electorate"), "winner": winner, "party": party_slug(wparty),
             "majority": to_int(g("majority")), "runner_up": g("second"),
             "runner_up_party": party_slug(g("second-party")) if g("second-party") else None,
             "third": g("third") or None, "third_party": party_slug(g("third-party")) if g("third-party") else None,
             "result": kind, "incumbent": g("incumbent") or None,
             "incumbent_party": party_slug(g("incumbent-party")) if g("incumbent-party") else None}
        out.append(e)
    return out

def summary_table(path):
    t = pd.read_html(io.StringIO(open(path).read()), match="Valid votes")[0]
    h1 = [str(x) for x in t.iloc[1]]; h2 = [str(x) for x in t.iloc[2]]
    cols = {}
    for i, (a, b) in enumerate(zip(h1, h2)):
        key = (a.split()[0].lower() if a != "nan" else "", b)
        cols[key] = i
    def col(group, sub):
        for (g, s), i in cols.items():
            if g == group and s.lower().startswith(sub.lower()): return i
        return None
    pv, pp = col("party", "Votes"), col("party", "%") or col("party", "Of total")
    ev, ep = col("electorate", "Votes"), col("electorate", "%") or col("electorate", "Of total")
    # seats
    seats_list = col("seats", "List"); seats_el = col("seats", "Electorate"); seats_tot = col("seats", "Total")
    if seats_list is None:   # 2020/2023 layout
        seats_list = col("party", "Seats"); seats_el = col("electorate", "Seats"); seats_tot = col("total", "Total")
    rows, meta = [], {}
    def num(x, f=int):
        x = str(x).replace(",", "").strip()
        x = re.sub(r"\[.*?\]", "", x)
        try:
            v = float(x)
            if v != v: return None
            return int(v) if f is int else v
        except ValueError: return None
    for _, r in t.iloc[3:].iterrows():
        name = re.sub(r"\[.*?\]", "", str(r.iloc[1])).strip()
        low = name.lower()
        if low.startswith("valid"): meta["valid_party_votes"] = num(r.iloc[pv]); meta["valid_electorate_votes"] = num(r.iloc[ev]); continue
        if low.startswith("informal"): meta["informal_party_votes"] = num(r.iloc[pv]); continue
        if low.startswith("disallowed"): meta["disallowed_party_votes"] = num(r.iloc[pv]); continue
        if low.startswith("below"): meta["below_threshold_votes"] = num(r.iloc[pv]); meta["below_threshold_pct"] = num(r.iloc[pp], float); continue
        if low == "total": meta["votes_cast"] = num(r.iloc[pv]); meta["total_seats"] = num(r.iloc[seats_tot]); continue
        if low.startswith("eligible"): meta["enrolled"] = num(r.iloc[pv]); meta["turnout_pct"] = num(r.iloc[pp], float); continue
        if low.startswith("unregistered"):
            meta["unregistered_electorate_votes"] = num(r.iloc[ev]); continue
        rows.append({"display": name, "party": party_slug(name),
                     "party_votes": num(r.iloc[pv]), "party_vote_pct": num(r.iloc[pp], float),
                     "electorate_votes": num(r.iloc[ev]), "electorate_votes_pct": num(r.iloc[ep], float),
                     "electorate_seats": num(r.iloc[seats_el]) or 0, "list_seats": num(r.iloc[seats_list]) or 0,
                     "total_seats": num(r.iloc[seats_tot]) or 0})
    return rows, meta

def list_mps_from_wikitext(path):
    """Return {party_slug: [(name, rank)]} from the 'List results' section table."""
    txt = open(path).read()
    i = txt.find("Successful list MPs")
    if i < 0: i = txt.find("List results")
    sec = txt[i:]
    j = sec.find("{|"); k = sec.find("\n|}", j)
    tab = sec[j:k]
    tab = re.sub(r"<ref[^>]*/>", "", tab); tab = re.sub(r"<ref[^>]*>.*?</ref>", "", tab, flags=re.S)
    rows = re.split(r"\n\|-[^\n]*", tab)
    hdr_row = rows[0] if "[[" in rows[0] else rows[1]
    parties = []
    for line in hdr_row.split("\n"):
        line = line.strip()
        if not line.startswith(("|", "!")) or line.startswith("{|"): continue
        for cell in re.split(r"\|\||!!", line.lstrip("|!")):
            m = re.search(r"\[\[([^\]|]+)(?:\|([^\]]+))?", cell)
            if m:
                try: parties.append(party_slug(m.group(1)))
                except KeyError: parties.append(party_slug(m.group(2)))
    body = rows[-1]
    cells = re.split(r"\n\|(?:\s*valign\s*=\s*\"?top\"?\s*\|)?", "\n" + body.strip())
    cells = [c for c in cells if "[[" in c]
    out = {}
    for p, c in zip(parties, cells):
        names = []
        for m in re.finditer(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]\s*(?:\((\d+)\))?", c):
            names.append((clean(m.group(2) or m.group(1)), int(m.group(3)) if m.group(3) else None))
        out[p] = names
    return out

def _party_from_cell(c):
    m = re.search(r"\{\{\s*party name with colou?r\s*\|([^}|]+)", c, re.I)
    return party_slug(m.group(1)) if m else None

def _date(s):
    import datetime
    s = clean(s).strip(" '")
    m = re.search(r"(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})", s)
    if not m: return s or None
    return datetime.datetime.strptime(" ".join(m.groups()), "%d %B %Y").date().isoformat()

def changes_table(path, heading_patterns=("=== Changes ===", "===Changes===", "==Summary of changes during term==")):
    txt = open(path).read()
    i = -1
    for h in heading_patterns:
        i = txt.find(h)
        if i >= 0: break
    if i < 0: return []
    sec = txt[i:]; j = sec.find("{|"); k = sec.find("\n|}", j)
    tab = sec[j:k]
    tab = re.sub(r"<ref[^>]*/>", "", tab); tab = re.sub(r"<ref[^>]*>.*?</ref>", "", tab, flags=re.S)
    tab = re.sub(r"\{\{\s*efn[^{}]*(\{\{[^{}]*\}\}[^{}]*)*\}\}", "", tab, flags=re.I)
    out = []
    for row in re.split(r"\n\|-[^\n]*", tab)[1:]:
        lines = [l for l in row.strip().split("\n")]
        # join continuation lines
        cells = []
        for l in lines:
            if l.startswith("!") and not cells: break
            if l.startswith("|") or l.startswith("!"):
                cells.extend([x for x in re.split(r"\|\||!!", l[1:])])
            elif cells:
                cells[-1] += "\n" + l
        if len(cells) < 6: continue
        cells = [c.strip() for c in cells]
        def nm(c):
            m = re.search(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", c)
            return clean(m.group(2) or m.group(1)) if m else clean(c)
        rec = {"seat": clean(cells[1]).strip("'"), "incumbent_party": _party_from_cell(cells[2]), "incumbent": nm(cells[3]),
               "date_vacated": _date(cells[4]), "reason": clean(cells[5]).strip("'")}
        rest = cells[6:]
        if rest and re.search(r"colspan\s*=\s*\"?5", rest[0]) or (len(rest) >= 1 and "None" in rest[0] and len(rest) < 3) or (rest and "N/A" in rest[0]):
            rec.update({"replacement": None, "replacement_party": None, "date_entered": None,
                        "change": clean(re.sub(r"^.*?\|", "", rest[0])) if rest else None})
        else:
            rec.update({"replacement_party": _party_from_cell(rest[0]), "replacement": nm(rest[1]),
                        "date_entered": _date(rest[2]), "change": clean(rest[3]) if len(rest) > 3 else None})
        rec["italic_note"] = cells[3].startswith("''")
        out.append(rec)
    return out

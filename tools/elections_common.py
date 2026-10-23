"""Shared helpers for the elections area (party slug maps, wikitext cleaning, person slugs)."""
import re, unicodedata, os, glob
import mwparserfromhell as mw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(ROOT, "raw", "elections")

# Wikipedia party article names / display names -> repo party slug
PARTY = {
 "new zealand national party": "national", "national": "national",
 "new zealand labour party": "labour", "labour": "labour",
 "green party of aotearoa new zealand": "green", "green": "green", "greens": "green",
 "act new zealand": "act", "act": "act",
 "new zealand first": "nz-first", "nz first": "nz-first",
 "māori party": "te-pati-maori", "te pāti māori": "te-pati-maori", "te pati maori": "te-pati-maori", "maori party": "te-pati-maori", "māori": "te-pati-maori",
 "mana party (new zealand)": "mana", "mana party": "mana", "mana movement": "mana", "mana": "mana",
 "internet party (new zealand)": "internet-party", "internet party": "internet-party", "internet": "internet-party",
 "internet party and mana movement": "internet-mana", "internet mana": "internet-mana",
 "united future new zealand": "united-future", "united future": "united-future",
 "conservative party (new zealand)": "conservative", "conservative party of new zealand": "conservative",
 "new conservative party (new zealand)": "conservative", "conservative party nz": "conservative",
 "conservative": "conservative", "new conservative": "conservative", "new conservatives": "conservative",
 "the opportunities party": "opportunity", "opportunity party (new zealand)": "opportunity",
 "opportunities": "opportunity", "opportunities (top)": "opportunity", "opportunity": "opportunity", "top": "opportunity",
 "jim anderton's progressive party": "progressive", "new zealand progressive party": "progressive", "progressive": "progressive",
 "aotearoa legalise cannabis party": "legalise-cannabis", "legalise cannabis": "legalise-cannabis",
 "bill and ben party": "bill-and-ben", "bill and ben": "bill-and-ben",
 "the kiwi party": "kiwi-party", "kiwi": "kiwi-party",
 "new zealand pacific party": "pacific-party", "pacific": "pacific-party",
 "the family party": "family-party", "family party": "family-party",
 "alliance (new zealand political party)": "alliance", "alliance": "alliance",
 "new zealand democratic party": "social-credit", "new zealand democratic party for social credit": "social-credit",
 "democrats": "social-credit", "social credit": "social-credit",
 "libertarianz": "libertarianz",
 "workers party of new zealand": "workers-party", "workers party": "workers-party",
 "residents action movement": "residents-action-movement", "ram": "residents-action-movement",
 "the republic of new zealand party": "republic-of-nz", "ronz": "republic-of-nz",
 "ban 1080 party": "ban-1080", "ban 1080": "ban-1080",
 "the civilian party": "civilian-party", "civilian": "civilian-party",
 "nz independent coalition": "nz-independent-coalition", "independent coalition": "nz-independent-coalition",
 "focus nz": "focus-nz", "focus": "focus-nz",
 "people's party": "nz-peoples-party", "new zealand people's party": "nz-peoples-party",
 "outdoors": "nz-outdoors-freedom", "new zealand outdoors party": "nz-outdoors-freedom", "nz outdoors party": "nz-outdoors-freedom",
 "nz outdoors & freedom party": "nz-outdoors-freedom", "outdoors & freedom": "nz-outdoors-freedom",
 "advance new zealand": "advance-nz", "advance nz": "advance-nz",
 "one": "one-party", "one party": "one-party", "one party (new zealand)": "one-party",
 "vision nz": "vision-nz", "vision new zealand": "vision-nz",
 "tea": "tea-party", "the tea party": "tea-party", "tea party (new zealand)": "tea-party",
 "sustainable nz": "sustainable-nz", "sustainable new zealand party": "sustainable-nz",
 "heartland new zealand party": "heartland", "heartland": "heartland",
 "new zealand loyal": "nz-loyal", "nz loyal": "nz-loyal",
 "newzeal": "newzeal", "freedoms new zealand": "freedoms-nz", "freedoms nz": "freedoms-nz",
 "democracynz": "democracynz",
 "animal justice party aotearoa new zealand": "animal-justice", "animal justice": "animal-justice",
 "women's rights party": "womens-rights", "women's rights": "womens-rights",
 "leighton baker party": "leighton-baker", "new nation party": "new-nation", "new nation": "new-nation",
 "independent politician": "independent", "independent (politician)": "independent", "independent": "independent",
 "free palestine party (new zealand)": "free-palestine", "te tai tokerau party": "te-tai-tokerau-party",
}
NAMES = {  # display names for slugs (current/most recent name)
 "national": "National", "labour": "Labour", "green": "Green", "act": "ACT", "nz-first": "NZ First",
 "te-pati-maori": "Te Pāti Māori (Māori Party)", "mana": "Mana", "internet-party": "Internet Party",
 "internet-mana": "Internet MANA", "united-future": "United Future", "conservative": "Conservative",
 "opportunity": "The Opportunity Party (TOP)", "progressive": "Progressive", "legalise-cannabis": "Aotearoa Legalise Cannabis",
 "independent": "Independent",
}

def party_slug(name):
    if name is None: return None
    n = clean(name).strip().lower()
    n = re.sub(r"\[\w\]$", "", n).strip()
    n = re.sub(r"\[\d+\]$", "", n).strip()
    if n in PARTY: return PARTY[n]
    raise KeyError("unknown party: %r" % name)

def clean(s):
    """wikitext -> plain text"""
    if s is None: return ""
    s = str(s)
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    code = mw.parse(s)
    for t in code.filter_templates(recursive=False):
        nm = str(t.name).strip().lower()
        try:
            if nm in ("sortname",):
                code.replace(t, f"{t.get(1).value} {t.get(2).value}")
            elif nm in ("nz electorate link",):
                code.replace(t, str(t.get(1).value))
            else:
                code.replace(t, "")
        except Exception:
            code.replace(t, "")
    s = code.strip_code()
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()

def person_slug(name):
    n = unicodedata.normalize("NFKD", name)
    n = "".join(c for c in n if not unicodedata.combining(c))
    n = n.lower().replace("'", "").replace("’", "")
    n = re.sub(r"[^a-z0-9]+", "-", n).strip("-")
    return n

def existing_person_slugs():
    out = {}
    for p in glob.glob(os.path.join(ROOT, "parties", "*", "people", "*")):
        out[os.path.basename(p)] = os.path.basename(os.path.dirname(os.path.dirname(p)))
    return out

def to_int(s):
    s = clean(s).replace(",", "").strip()
    m = re.match(r"^-?\d+", s)
    return int(m.group()) if m else None

#!/usr/bin/env python3
"""Validate data/geo against the election data.

Checks, for every election year in data/elections/{2011,2014,2017,2020,2023}.json and
data/electorates/2026.json, that each electorate matches exactly one feature (by slug) in the
boundary-set files that index.json says apply to that year, and that no feature is left
unmatched.  Also checks file sizes, GeoJSON sanity (closed rings, >= 4 points, lon/lat ranges)
and that feature names equal the election-data names.

Exit status 1 if any mismatch.  Usage: python3 tools/geo_validate.py
"""
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = os.path.join(ROOT, "data", "geo")
MAX_BYTES = 600_000
YEARS = [2011, 2014, 2017, 2020, 2023, 2026]


def slugify(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("'", "").replace("’", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"^mount-", "mt-", s)  # repo convention: mt-albert, mt-roskill, mt-maunganui (as Stats NZ spells them)


def load_electorates(year):
    if year == 2026:
        el = json.load(open(os.path.join(ROOT, "data", "electorates", "2026.json"), encoding="utf-8"))
    else:
        el = json.load(open(os.path.join(ROOT, "data", "elections", f"{year}.json"), encoding="utf-8"))["electorates"]
    return [(e["type"], e.get("slug") or slugify(e["name"]), e["name"]) for e in el]


def check_geometry(f, problems, label):
    g = f["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    if not polys:
        problems.append(f"{label}: empty geometry")
    for poly in polys:
        for ring in poly:
            if len(ring) < 4:
                problems.append(f"{label}: ring with {len(ring)} points")
            if ring[0] != ring[-1]:
                problems.append(f"{label}: unclosed ring")
            for x, y in ring:
                if not (165 <= x <= 185 and -48.5 <= y <= -33):
                    problems.append(f"{label}: coordinate out of NZ range {x},{y}")
                    break


def main():
    index = json.load(open(os.path.join(GEO, "index.json"), encoding="utf-8"))
    problems = []
    layers = {}
    for bs, entry in index["boundary_sets"].items():
        for etype, info in entry["layers"].items():
            path = os.path.join(ROOT, "data", info["file"])
            size = os.path.getsize(path)
            if size > MAX_BYTES:
                problems.append(f"{info['file']}: {size} bytes > {MAX_BYTES}")
            fc = json.load(open(path, encoding="utf-8"))
            by_slug = {}
            for f in fc["features"]:
                p = f["properties"]
                for k in ("name", "slug", "type", "boundary_set"):
                    if k not in p:
                        problems.append(f"{info['file']}: feature missing {k}")
                if p.get("type") != etype or str(p.get("boundary_set")) != bs:
                    problems.append(f"{info['file']}: {p.get('name')} has type/boundary_set {p.get('type')}/{p.get('boundary_set')}")
                if p["slug"] in by_slug:
                    problems.append(f"{info['file']}: duplicate slug {p['slug']}")
                by_slug[p["slug"]] = p
                check_geometry(f, problems, f"{info['file']} {p['name']}")
            layers[(etype, bs)] = (info["file"], by_slug, size)
    print("files:")
    for (etype, bs), (file, by_slug, size) in sorted(layers.items()):
        print(f"  {file:28s} {size/1024:6.0f} KB  {len(by_slug):3d} features")
    for year in YEARS:
        bs = str(index["election_to_boundary_set"][str(year)])
        els = load_electorates(year)
        used = {"general": set(), "maori": set()}
        for etype, slug, name in els:
            file, by_slug, _ = layers[(etype, bs)]
            if slug not in by_slug:
                problems.append(f"{year}: {etype} '{name}' (slug {slug}) has no feature in {file}")
                continue
            used[etype].add(slug)
            canon = by_slug[slug]["name"]
            if canon != name and name not in index["boundary_sets"][bs]["aliases"].get(slug, []):
                problems.append(f"{year}: {etype} '{name}' matched feature named '{canon}' (not listed as alias)")
        for etype in ("general", "maori"):
            file, by_slug, _ = layers[(etype, bs)]
            extra = set(by_slug) - used[etype]
            if extra:
                problems.append(f"{year}: features in {file} with no electorate: {sorted(extra)}")
        n_g = sum(1 for t, _, _ in els if t == "general")
        n_m = sum(1 for t, _, _ in els if t == "maori")
        print(f"{year}: boundary set {bs}; {n_g} general + {n_m} Māori electorates matched")
    if problems:
        print(f"\n{len(problems)} PROBLEM(S):")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("\nOK: every electorate matches exactly one feature; no unmatched features.")


if __name__ == "__main__":
    main()

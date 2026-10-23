#!/usr/bin/env python3
"""Build simplified electorate GeoJSON for the interactive map.

Input : raw/geo/<type>-<set>.geojson (from tools/geo_fetch.py; WGS84, full resolution)
Output: data/geo/<type>-<set>.json  (WGS84 GeoJSON, topology-preserving simplification, < ~600 KB)
        data/geo/index.json         (boundary set -> election years, bboxes, insets, name map, licence)

Simplification is pure Python and topology-aware: all rings are cut into shared arcs at
junctions (TopoJSON-style), each unique arc is simplified once with Visvalingam–Whyatt
(effective-area), and rings are re-assembled from the same simplified arcs so neighbouring
electorates still share exactly the same boundary (no slivers/gaps).  The per-arc tolerance
is scaled down for arcs that belong to small (urban) electorates so no polygon collapses, and
arc end points (junctions) are never removed.  A global tolerance is searched so each output
file lands under the size budget.

Coordinates are rounded to 5 dp (~1 m).  Longitudes west of the antimeridian (Chatham
Islands) are shifted by +360 so the map does not wrap (noted in index.json).

Usage: python3 tools/geo_build.py [--budget 600000]
"""
import heapq
import json
import math
import os
import re
import sys
import unicodedata
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw", "geo")
OUT = os.path.join(ROOT, "data", "geo")

# Which boundary set each election used.
SET_ELECTIONS = {"2007": [2008, 2011], "2014": [2014, 2017], "2020": [2020, 2023], "2025": [2026]}
DATAFINDER = {
    ("general", "2007"): (104065, "General Electoral District 2007"),
    ("general", "2014"): (104062, "General Electoral District 2014"),
    ("general", "2020"): (104580, "General Electorates 2020"),
    ("general", "2025"): (122741, "General Electorates 2025"),
    ("maori", "2007"): (104066, "Māori Electoral District 2007"),
    ("maori", "2014"): (104063, "Māori Electoral District 2014"),
    ("maori", "2020"): (104579, "Māori Electorates 2020"),
    ("maori", "2025"): (122742, "Māori Electorates 2025"),
}
ARCGIS = "https://services2.arcgis.com/vKb0s8tBIA3bdocZ/ArcGIS/rest/services"

# Suggested insets (WGS84 bbox: [west, south, east, north]); Chatham lons are +360-shifted.
INSETS = {
    "auckland": {"label": "Auckland", "bbox": [174.45, -37.10, 175.15, -36.60]},
    "wellington": {"label": "Wellington", "bbox": [174.60, -41.45, 175.15, -40.95]},
    "christchurch": {"label": "Christchurch", "bbox": [172.35, -43.70, 172.85, -43.35]},
    "chatham": {"label": "Chatham Islands", "bbox": [183.20, -44.50, 184.60, -43.50]},
}
MAINLAND_BBOX = [166.0, -47.5, 179.0, -34.0]


def slugify(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("'", "").replace("’", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"^mount-", "mt-", s)  # repo convention: mt-albert, mt-roskill, mt-maunganui (as Stats NZ spells them)


def clean_source_name(n):
    n = "".join(c for c in n if unicodedata.category(c) != "Cc")  # stray U+0081 in Māori 2014
    return n.strip()


def canonical_names():
    """slug -> canonical name (latest election spelling), per (type, set)."""
    out = defaultdict(dict)
    aliases = defaultdict(lambda: defaultdict(set))
    for bs, years in SET_ELECTIONS.items():
        for y in years:
            if y == 2026:
                p = os.path.join(ROOT, "data", "electorates", "2026.json")
                if not os.path.exists(p):
                    continue
                el = json.load(open(p, encoding="utf-8"))
            else:
                p = os.path.join(ROOT, "data", "elections", f"{y}.json")
                if not os.path.exists(p):
                    continue
                el = json.load(open(p, encoding="utf-8"))["electorates"]
            for e in el:
                sl = e.get("slug") or slugify(e["name"])
                out[(e["type"], bs)][sl] = e["name"]  # later years overwrite -> latest spelling
                aliases[(e["type"], bs)][sl].add(e["name"])
    # prefer the spelling used by data/electorates/2026.json (the site's canonical electorate list)
    names2026 = out.get(("general", "2025"), {}) | out.get(("maori", "2025"), {})
    for key, m in out.items():
        for sl in m:
            if sl in names2026:
                m[sl] = names2026[sl]
            aliases[key][sl].add(m[sl])  # every spelling used by any election year + the canonical one
    return out, aliases


# ---------------------------------------------------------------- geometry helpers
def ring_area(r):
    a = 0.0
    for i in range(len(r) - 1):
        a += r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1]
    return a / 2.0


def polys_of(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    return geom["coordinates"]


def visvalingam(pts, thresh, min_keep):
    """Return kept indices of an open polyline; endpoints kept. min_keep = min number of points."""
    n = len(pts)
    if n <= 2:
        return list(range(n))
    prev = list(range(-1, n - 1))
    nxt = list(range(1, n + 1))
    alive = [True] * n

    def area(i):
        a, b, c = pts[prev[i]], pts[i], pts[nxt[i]]
        return abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / 2.0

    eff = [0.0] * n
    heap = []
    for i in range(1, n - 1):
        eff[i] = area(i)
        heap.append((eff[i], i))
    heapq.heapify(heap)
    count = n
    maxseen = 0.0
    while heap and count > min_keep:
        a, i = heapq.heappop(heap)
        if not alive[i] or a != eff[i]:
            continue
        if a >= thresh:
            break
        # remove i; enforce monotone effective areas
        maxseen = max(maxseen, a)
        alive[i] = False
        count -= 1
        p, q = prev[i], nxt[i]
        nxt[p] = q
        prev[q] = p
        for j in (p, q):
            if 0 < j < n - 1 and alive[j]:
                eff[j] = max(area(j), maxseen)
                heapq.heappush(heap, (eff[j], j))
    return [i for i in range(n) if alive[i]]


# ---------------------------------------------------------------- topology
class Topology:
    def __init__(self, features):
        self.features = features
        # rings: (feature idx, poly idx, ring idx) -> list of points (closed)
        self.rings = []
        for fi, f in enumerate(features):
            for pi, poly in enumerate(polys_of(f["geometry"])):
                for ri, ring in enumerate(poly):
                    pts = [tuple(p) for p in ring]
                    if pts[0] != pts[-1]:
                        pts.append(pts[0])
                    # drop consecutive dups
                    cl = [pts[0]]
                    for p in pts[1:]:
                        if p != cl[-1]:
                            cl.append(p)
                    self.rings.append(((fi, pi, ri), cl))
        self._find_junctions()
        self._cut()

    def _find_junctions(self):
        neigh = {}
        junction = set()
        for _, r in self.rings:
            m = len(r) - 1
            for i in range(m):
                p = r[i]
                nb = frozenset((r[i - 1] if i > 0 else r[m - 1], r[i + 1]))
                prev = neigh.get(p)
                if prev is None:
                    neigh[p] = nb
                elif prev != nb:
                    junction.add(p)
        self.junctions = junction

    def _cut(self):
        self.arcs = []  # list of point lists (open; or closed ring arcs)
        self.arc_index = {}
        self.ring_arcs = []  # per ring: list of (arc id, reversed?)
        self.arc_features = defaultdict(set)
        for (fi, _, _), r in self.rings:
            m = len(r) - 1
            js = [i for i in range(m) if r[i] in self.junctions]
            parts = []
            if not js:
                parts.append(r)  # whole closed ring is one arc
            else:
                rot = r[js[0]:m] + r[: js[0] + 1]  # rotate so starts at a junction, closed
                cuts = [i for i in range(len(rot)) if rot[i] in self.junctions]
                for a, b in zip(cuts, cuts[1:]):
                    parts.append(rot[a : b + 1])
            ids = []
            for part in parts:
                key = tuple(part)
                rkey = tuple(reversed(part))
                if key in self.arc_index:
                    ids.append((self.arc_index[key], False))
                elif rkey in self.arc_index:
                    ids.append((self.arc_index[rkey], True))
                else:
                    aid = len(self.arcs)
                    self.arcs.append(part)
                    self.arc_index[key] = aid
                    ids.append((aid, False))
                self.arc_features[ids[-1][0]].add(fi)
            self.ring_arcs.append(ids)

    def simplify(self, base_thresh, feature_scale, min_island_area):
        simp = []
        for aid, arc in enumerate(self.arcs):
            scale = min(feature_scale[fi] for fi in self.arc_features[aid])
            th = base_thresh * scale
            closed = arc[0] == arc[-1] and len(arc) > 3
            if closed:
                keep = visvalingam(arc[:-1] + [arc[0]], th, 4)
                # ensure a closed arc keeps >= 4 points (3 distinct)
                pts = [arc[i] for i in keep]
                if len(pts) < 4:
                    pts = []
            else:
                keep = visvalingam(arc, th, 2)
                pts = [arc[i] for i in keep]
            simp.append(pts)
        # reassemble
        out_rings = []
        for ids in self.ring_arcs:
            ring = []
            for aid, rev in ids:
                pts = simp[aid]
                if rev:
                    pts = pts[::-1]
                if ring and pts and ring[-1] == pts[0]:
                    pts = pts[1:]
                ring.extend(pts)
            if ring and ring[0] != ring[-1]:
                ring.append(ring[0])
            out_rings.append(ring)
        # rebuild features
        geoms = defaultdict(lambda: defaultdict(dict))
        for ((fi, pi, ri), orig), ring in zip(self.rings, out_rings):
            geoms[fi][pi][ri] = (ring, ring_area(orig))
        results = []
        for fi in range(len(self.features)):
            polys = []
            parts = geoms[fi]
            # largest original outer ring is always kept
            largest = max(parts, key=lambda pi: abs(parts[pi][0][1]))
            for pi in sorted(parts):
                outer, oarea = parts[pi][0]
                if len(outer) < 4:
                    continue
                if pi != largest and abs(oarea) < min_island_area:
                    continue
                poly = [outer]
                for ri in sorted(parts[pi]):
                    if ri == 0:
                        continue
                    hole, harea = parts[pi][ri]
                    if len(hole) >= 4 and abs(harea) >= min_island_area:
                        poly.append(hole)
                polys.append(poly)
            results.append(polys)
        return results


def round_ring(r, nd=5):
    out = []
    for p in r:
        q = (round(p[0], nd), round(p[1], nd))
        if not out or q != out[-1]:
            out.append(q)
    if out[0] != out[-1]:
        out.append(out[0])
    return out


def feature_area_deg2(polys):
    a = 0.0
    for poly in polys:
        a += abs(ring_area(poly[0]))
        for h in poly[1:]:
            a -= abs(ring_area(h))
    return a


def to_geojson(polys):
    polys = [[list(map(list, round_ring(r))) for r in poly] for poly in polys]
    polys = [p for p in polys if len(p[0]) >= 4]
    if len(polys) == 1:
        return {"type": "Polygon", "coordinates": polys[0]}
    return {"type": "MultiPolygon", "coordinates": polys}


def bbox_of(coords_iter):
    xs, ys = [], []
    for x, y in coords_iter:
        xs.append(x)
        ys.append(y)
    return [round(min(xs), 4), round(min(ys), 4), round(max(xs), 4), round(max(ys), 4)]


def build_layer(etype, bs, canon, aliases, budget):
    raw_path = os.path.join(RAW, f"{etype}-{bs}.geojson")
    fc = json.load(open(raw_path, encoding="utf-8"))
    feats = fc["features"]
    name_map = {}
    for f in feats:
        p = f["properties"]
        nf = [k for k in p if k.endswith("_NAME")][0]
        src = p[nf]
        cleaned = clean_source_name(src)
        sl = slugify(cleaned)
        name = canon.get((etype, bs), {}).get(sl, cleaned)
        f["_slug"], f["_name"], f["_source_name"] = sl, name, src
        f["_code"] = p[[k for k in p if re.match(r"[GM]ED\d{4}_V1_00$", k)][0]]
        if src != name:
            name_map[src] = name
        # shift Chatham Islands east of the antimeridian
        for poly in polys_of(f["geometry"]):
            for ring in poly:
                for pt in ring:
                    if pt[0] < 0:
                        pt[0] += 360.0
    topo = Topology(feats)
    areas = [feature_area_deg2(polys_of(f["geometry"])) for f in feats]
    ref = sorted(areas)[len(areas) // 2]  # median electorate area
    # scale tolerance by relative area for small electorates (floor 2 %)
    scale = [max(0.02, min(1.0, a / ref)) for a in areas]
    min_island = 2.5e-5  # deg^2 ~ 0.2 km^2 : drop tiny islets (never the main part)
    print(f"{etype}-{bs}: {len(feats)} features, {len(topo.arcs)} arcs, {len(topo.junctions)} junctions")

    def render(th):
        polys = topo.simplify(th, scale, min_island)
        out_feats = []
        for f, pl in zip(feats, polys):
            out_feats.append({
                "type": "Feature",
                "properties": {
                    "name": f["_name"], "slug": f["_slug"], "type": etype, "boundary_set": int(bs),
                    "code": f["_code"], "source_name": f["_source_name"],
                },
                "geometry": to_geojson(pl),
            })
        lid, ltitle = DATAFINDER[(etype, bs)]
        doc = {
            "type": "FeatureCollection",
            "name": f"{etype}-{bs}",
            "boundary_set": int(bs),
            "elections": SET_ELECTIONS[bs],
            "crs": "EPSG:4326 (longitudes > 180 for Chatham Islands)",
            "source": {
                "title": ltitle,
                "publisher": "Stats NZ (Tatauranga Aotearoa), Stats NZ Geographic Data Service",
                "url": f"https://datafinder.stats.govt.nz/layer/{lid}/",
                "service": f"{ARCGIS}/{fc['source']['arcgis_service'].split('/services/')[1]}",
                "licence": "CC BY 4.0",
                "licence_url": "https://creativecommons.org/licenses/by/4.0/",
                "attribution": "Representation Commission, Stats NZ",
                "fetched": fc["source"].get("fetched"),
                "simplified": "topology-preserving Visvalingam–Whyatt, tools/geo_build.py",
            },
            "features": out_feats,
        }
        s = json.dumps(doc, ensure_ascii=False, separators=(",", ":"))
        return doc, s, polys

    # search tolerance (deg^2) so that size <= budget
    lo, hi = 1e-6, 1e-3  # floor 1e-6 deg^2 (~0.01 km^2): finer than that is wasted bytes
    best = None
    for _ in range(22):
        mid = math.sqrt(lo * hi)
        doc, s, polys = render(mid)
        size = len(s.encode("utf-8"))
        if size <= budget:
            best = (mid, doc, s, polys, size)
            hi = mid
        else:
            lo = mid
        if hi / lo < 1.08:
            break
    if best is None:
        doc, s, polys = render(hi)
        best = (hi, doc, s, polys, len(s.encode("utf-8")))
    # if the floor tolerance already fits the budget, use it (stops the search over-fitting)
    doc0, s0, polys0 = render(1e-6)
    if len(s0.encode("utf-8")) <= budget:
        best = (1e-6, doc0, s0, polys0, len(s0.encode("utf-8")))
    th, doc, s, polys, size = best
    # QA: area retention + vertex count
    worst = (1.0, "")
    nverts = 0
    for f, pl, a0 in zip(feats, polys, areas):
        a1 = feature_area_deg2(pl)
        nverts += sum(len(r) for poly in pl for r in poly)
        ratio = a1 / a0 if a0 else 1
        if abs(1 - ratio) > abs(1 - worst[0]):
            worst = (ratio, f["_name"])
        if not pl:
            raise RuntimeError(f"{f['_name']} collapsed")
    print(f"   tolerance {th:.3g} deg^2 -> {size/1024:.0f} KB, {nverts} vertices; worst area retention {worst[0]:.5f} ({worst[1]})")
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{etype}-{bs}.json"), "w", encoding="utf-8") as fh:
        fh.write(s)
    all_pts = [pt for f in doc["features"] for poly in polys_of(f["geometry"]) for r in poly for pt in r]
    main_pts = [pt for pt in all_pts if pt[0] <= 180]
    return {
        "file": f"geo/{etype}-{bs}.json",
        "features": len(doc["features"]),
        "bytes": size,
        "vertices": nverts,
        "tolerance_deg2": th,
        "bbox": bbox_of(all_pts),
        "bbox_mainland": bbox_of(main_pts),
        "has_chatham": len(main_pts) != len(all_pts),
        "name_map": name_map,
        "aliases": {sl: sorted(v) for sl, v in aliases.get((etype, bs), {}).items() if len(v) > 1},
        "names": {f["properties"]["slug"]: f["properties"]["name"] for f in doc["features"]},
    }


def main():
    budget = 600_000
    if "--budget" in sys.argv:
        budget = int(sys.argv[sys.argv.index("--budget") + 1])
    budget = int(budget * 0.97)
    canon, aliases = canonical_names()
    index = {
        "description": "NZ electorate boundaries for the interactive map. All files are GeoJSON in WGS84 (EPSG:4326).",
        "licence": {
            "name": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
            "url": "https://creativecommons.org/licenses/by/4.0/",
            "attribution": "Electorate boundaries: Representation Commission / Stats NZ (Tatauranga Aotearoa), via the Stats NZ Geographic Data Service, licensed CC BY 4.0. Simplified for web display.",
            "source_portal": "https://datafinder.stats.govt.nz/",
            "arcgis_mirror": ARCGIS,
        },
        "notes": [
            "Boundary polygons extend offshore to the limit of the territorial sea (as published); they are not clipped to the coastline.",
            "Longitudes for the Chatham Islands (part of the Rongotai / Wellington Bays and Te Tai Tonga electorates) are stored as 183–184 (i.e. +360) so polygons do not wrap across the antimeridian; use bbox_mainland for the main map and the 'chatham' inset for the islands. The 2007 layers as published do not include the Chatham Islands.",
            "Geometry simplified with a topology-preserving Visvalingam–Whyatt (shared arcs), tolerance adapted per electorate so small urban seats keep detail; coordinates rounded to 5 dp.",
            "Feature properties: name (canonical, as in data/elections and data/electorates), slug, type, boundary_set, code (Stats NZ electorate code), source_name (name string as published in the layer).",
        ],
        "election_to_boundary_set": {str(y): int(bs) for bs, ys in SET_ELECTIONS.items() for y in ys},
        "boundary_sets": {},
        "insets": INSETS,
        "bbox_mainland": MAINLAND_BBOX,
    }
    for bs in SET_ELECTIONS:
        entry = {"elections": SET_ELECTIONS[bs], "layers": {}, "name_map": {}, "aliases": {}}
        for etype in ("general", "maori"):
            lid, ltitle = DATAFINDER[(etype, bs)]
            info = build_layer(etype, bs, canon, aliases, budget)
            entry["name_map"].update(info.pop("name_map"))
            entry["aliases"].update(info.pop("aliases"))
            info["source"] = {"title": ltitle, "url": f"https://datafinder.stats.govt.nz/layer/{lid}/"}
            entry["layers"][etype] = info
        index["boundary_sets"][bs] = entry
    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=1)
    print("wrote", os.path.join(OUT, "index.json"))


if __name__ == "__main__":
    main()

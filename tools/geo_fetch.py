#!/usr/bin/env python3
"""Download NZ electorate boundary layers from Stats NZ's ArcGIS Online feature services.

Source: Stats NZ Geographic Data Service (datafinder.stats.govt.nz) layers, mirrored by
Stats NZ on ArcGIS Online (org vKb0s8tBIA3bdocZ).  Licence: Creative Commons Attribution 4.0
International (CC BY 4.0); copyright text on each layer: "Representation Commission, Stats NZ".

Boundary sets:
  2007  General Electoral District 2007 / Māori Electoral District 2007  (2008 and 2011 elections)
  2014  General Electoral District 2014 / Māori Electoral District 2014  (2014 and 2017 elections)
  2020  General Electorates 2020 / Māori Electorates 2020               (2020 and 2023 elections)
  2025  General Electorates 2025 / Māori Electorates 2025               (2026 election)

Writes raw/geo/<type>-<set>.geojson (WGS84, full-resolution geometry as served) plus
raw/geo/<type>-<set>.meta.json (layer metadata from the service).

Usage: python3 tools/geo_fetch.py [--only general-2025,...]
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw", "geo")
BASE = "https://services2.arcgis.com/vKb0s8tBIA3bdocZ/ArcGIS/rest/services"

LAYERS = {
    "general-2007": ("General_Electorates_2007", 104065),
    "general-2014": ("General_Electorates_2014", 104062),
    "general-2020": ("General_Electorates_2020", 104580),
    "general-2025": ("General_Electorates_2025", 122741),
    "maori-2007": ("Māori_Electorates_2007", 104066),
    "maori-2014": ("Māori_Electorates_2014", 104063),
    "maori-2020": ("Māori_Electorates_2020", 104579),
    "maori-2025": ("Māori_Electorates_2025", 122742),
}
UA = "PoliticsNZResearch/1.0 (personal research; electorate map)"


def get(url, tries=5):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 + 3 * i)
    raise RuntimeError(f"failed {url}: {last}")


def fetch_layer(key, service, datafinder_id):
    svc = f"{BASE}/{urllib.parse.quote(service)}/FeatureServer/0"
    meta = json.loads(get(f"{svc}?f=pjson"))
    ids = json.loads(get(f"{svc}/query?where=1%3D1&returnIdsOnly=true&f=json"))
    oid_field = ids.get("objectIdFieldName", "OBJECTID")
    oids = sorted(ids["objectIds"])
    print(f"{key}: {meta.get('name')} — {len(oids)} features", flush=True)
    feats = []
    for oid in oids:
        q = urllib.parse.urlencode({
            "where": f"{oid_field}={oid}", "outFields": "*", "returnGeometry": "true",
            "outSR": "4326", "f": "geojson",
        })
        fc = json.loads(get(f"{svc}/query?{q}"))
        if fc.get("exceededTransferLimit"):
            raise RuntimeError(f"{key} oid {oid}: transfer limit exceeded")
        assert len(fc["features"]) == 1, (key, oid, len(fc["features"]))
        f = fc["features"][0]
        name_field = [k for k in f["properties"] if k.endswith("_NAME")][0]
        print(f"   {oid:3d} {f['properties'][name_field]}", flush=True)
        feats.append(f)
    out = {
        "type": "FeatureCollection",
        "name": meta.get("name"),
        "source": {
            "arcgis_service": svc,
            "datafinder_layer": f"https://datafinder.stats.govt.nz/layer/{datafinder_id}/",
            "licence": "CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/",
            "attribution": meta.get("copyrightText"),
            "fetched": time.strftime("%Y-%m-%d"),
        },
        "features": feats,
    }
    os.makedirs(RAW, exist_ok=True)
    with open(os.path.join(RAW, f"{key}.geojson"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False)
    with open(os.path.join(RAW, f"{key}.meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)


def main():
    only = None
    if len(sys.argv) > 2 and sys.argv[1] == "--only":
        only = set(sys.argv[2].split(","))
    for key, (service, lid) in LAYERS.items():
        if only and key not in only:
            continue
        fetch_layer(key, service, lid)


if __name__ == "__main__":
    main()

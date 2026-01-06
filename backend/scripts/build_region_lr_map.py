"""
Fetch official Yandex Market geo regions and build lr_code -> region_name map.

This script does NOT guess or hardcode anything. It must be run to generate
backend/data/region_lr_map.csv, which is the only allowed mapping source.
"""

import csv
import sys
from pathlib import Path

import httpx

API_URL = "https://market.yandex.ru/api/geo/regions"
OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "region_lr_map.csv"


def fetch_regions() -> list[dict]:
    with httpx.Client(timeout=15.0) as client:
        resp = client.get(API_URL)
        resp.raise_for_status()
        data = resp.json()
        # Expecting a list of regions with id/lr and name
        return data


def build_map():
    regions = fetch_regions()
    seen = set()
    rows = []
    for item in regions:
        code = item.get("id") or item.get("lr")
        name = item.get("name")
        if code is None or name is None:
            continue
        try:
            code_int = int(code)
        except ValueError:
            continue
        key = (code_int, name)
        if key in seen:
            continue
        seen.add(key)
        rows.append({"lr_code": code_int, "region_name": str(name).strip()})

    rows = sorted(rows, key=lambda x: x["lr_code"])
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["lr_code", "region_name"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Regions fetched: {len(rows)}")
    print("First 10 rows:")
    for r in rows[:10]:
        print(r)


if __name__ == "__main__":
    try:
        build_map()
    except Exception as exc:
        sys.stderr.write(f"Failed to build region_lr_map.csv: {exc}\n")
        sys.exit(1)

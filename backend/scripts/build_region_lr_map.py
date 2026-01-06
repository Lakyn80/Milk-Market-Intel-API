"""
Builds lr_code -> region_name map from official Yandex GEO suggest API.
This CSV is the ONLY allowed source for region code normalization.
No hardcoded mappings. No guessing.
"""

import csv
import sys
import time
import logging
from pathlib import Path

import requests

OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "region_lr_map.csv"
API_URL = "https://suggest-maps.yandex.ru/suggest-geo"

# Queries to maximize coverage (single Cyrillic letters + common bigrams)
QUERIES = (
    [chr(c) for c in range(ord("а"), ord("я") + 1)]
    + ["мо", "но", "са", "ка", "ба", "во", "св", "се", "ко", "та", "кра", "обл", "респ"]
)


def fetch_suggest(session: requests.Session, query: str) -> list[dict]:
    params = {
        "text": query,
        "lang": "ru",
        "v": "5",
        "types": "geo",
        "attrs": "geos",
        "n": 20,
        "national": "ru",
        "origin": "market",
    }
    resp = session.get(API_URL, params=params, timeout=10)
    if resp.status_code == 429:
        time.sleep(0.5)
        resp = session.get(API_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("results") or data.get("items") or []
    return items


def extract_regions(items: list[dict]) -> list[tuple[int, str]]:
    regions = []
    for item in items:
        entity = item.get("entity") or item.get("type") or ""
        if str(entity).lower() != "region":
            continue
        code = item.get("id") or item.get("lr") or item.get("geoid")
        name = item.get("name") or item.get("title")
        if code is None or name is None:
            continue
        try:
            code_int = int(code)
        except (ValueError, TypeError):
            continue
        regions.append((code_int, str(name).strip()))
    return regions


def build_map():
    session = requests.Session()
    seen = set()
    rows = []
    total_queries = len(QUERIES)
    for q in QUERIES:
        try:
            items = fetch_suggest(session, q)
        except Exception as exc:
            logging.warning("Query %s failed: %s", q, exc)
            continue
        for code_int, name in extract_regions(items):
            if code_int in seen:
                continue
            seen.add(code_int)
            rows.append({"lr_code": code_int, "region_name": name})
        time.sleep(0.35)
    rows = sorted(rows, key=lambda x: x["lr_code"])
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["lr_code", "region_name"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Queries: {total_queries}, regions collected: {len(rows)}")
    print("First 10 rows:")
    for r in rows[:10]:
        print(r)


if __name__ == "__main__":
    try:
        build_map()
    except Exception as exc:
        sys.stderr.write(f"Failed to build region_lr_map.csv: {exc}\n")
        sys.exit(1)

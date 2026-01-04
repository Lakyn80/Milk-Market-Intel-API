import json
from datetime import datetime
import argparse
from pathlib import Path
import random
import time
from typing import List, Dict

from app.modules.retail.providers.yandex_catalog import YandexMarketCatalogProvider

# Default dairy-focused categories (mix of catalog and search URLs).
DEFAULT_CATEGORIES = [
    # Umbrella dairy category
    "https://market.yandex.ru/catalog--molochnye-produkty/54650/list?hid=91308",
    # Key dairy product searches (fallback when precise hid is unknown)
    "https://market.yandex.ru/search?text=%D0%BC%D0%BE%D0%BB%D0%BE%D0%BA%D0%BE",
    "https://market.yandex.ru/search?text=%D1%81%D0%BB%D0%B8%D0%B2%D0%BA%D0%B8",
    "https://market.yandex.ru/search?text=%D0%BA%D0%B5%D1%84%D0%B8%D1%80",
    "https://market.yandex.ru/search?text=%D1%80%D1%8F%D0%B6%D0%B5%D0%BD%D0%BA%D0%B0",
    "https://market.yandex.ru/search?text=%D0%BF%D1%80%D0%BE%D1%81%D1%82%D0%BE%D0%BA%D0%B2%D0%B0%D1%88%D0%B0",
    "https://market.yandex.ru/search?text=%D0%B9%D0%BE%D0%B3%D1%83%D1%80%D1%82",
    "https://market.yandex.ru/search?text=%D1%82%D0%B2%D0%BE%D1%80%D0%BE%D0%B3",
    "https://market.yandex.ru/search?text=%D1%81%D1%8B%D1%80",
    "https://market.yandex.ru/search?text=%D1%81%D0%BC%D0%B5%D1%82%D0%B0%D0%BD%D0%B0",
    "https://market.yandex.ru/search?text=%D0%BC%D0%B0%D1%81%D0%BB%D0%BE%20%D1%81%D0%BB%D0%B8%D0%B2%D0%BE%D1%87%D0%BD%D0%BE%D0%B5",
    "https://market.yandex.ru/search?text=%D0%BC%D0%BE%D0%BB%D0%BE%D1%87%D0%BD%D1%8B%D0%B5%20%D0%B4%D0%B5%D1%81%D0%B5%D1%80%D1%82%D1%8B",
    "https://market.yandex.ru/search?text=%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D0%B5%20%D0%BC%D0%BE%D0%BB%D0%BE%D1%87%D0%BD%D1%8B%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D1%8B",
    "https://market.yandex.ru/search?text=%D1%81%D1%83%D1%85%D0%BE%D0%B5%20%D0%BC%D0%BE%D0%BB%D0%BE%D0%BA%D0%BE",
    "https://market.yandex.ru/search?text=%D1%81%D0%B3%D1%83%D1%89%D0%B5%D0%BD%D0%BA%D0%B0",
]

OUTPUT_DIR = Path(__file__).resolve().parents[3] / "data"


def load_existing(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data.get("items") or []
        if isinstance(data, list):
            return data
    except Exception:
        return []
    return []


def save_items(path: Path, items: List[Dict]) -> None:
    payload = {
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "count": len(items),
        "items": items,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_for_region(lr: str, categories: List[str], pages: int | None) -> tuple[List[Dict], Path]:
    provider = YandexMarketCatalogProvider(region=lr)
    region_path = OUTPUT_DIR / f"yandex_catalog_lr_{lr}.json"
    all_items = load_existing(region_path)

    def on_page(items_page: List[Dict]) -> None:
        for it in items_page:
            it["region"] = lr
        all_items.extend(items_page)
        save_items(region_path, all_items)

    for url in categories:
        try:
            provider.fetch_category(
                url,
                page_limit=pages if pages and pages > 0 else None,
                region_lr=lr,
                throttle_seconds=random.uniform(1.5, 3.0),
                per_page_callback=on_page,
            )
            print(f"Saved {len(all_items)} items so far | lr={lr} | {url}")
            time.sleep(random.uniform(4.0, 7.0))  # between categories
        except Exception as exc:  # pragma: no cover - runtime safety
            print(f"Warning: failed lr={lr} category={url}: {exc}")
            continue

    # Final write to stamp collected_at
    save_items(region_path, all_items)
    return all_items, region_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Yandex Market catalog (POC).")
    parser.add_argument(
        "--pages",
        type=int,
        default=0,
        help="Number of pages per category (0 or negative = all pages until empty).",
    )
    parser.add_argument(
        "--category",
        action="append",
        dest="categories",
        help="Category URL to scrape (can be passed multiple times). Defaults to built-in list.",
    )
    parser.add_argument(
        "--lr",
        required=True,
        help="Yandex lr region code (single region per run, required).",
    )
    args = parser.parse_args()

    lr = str(args.lr)
    categories = args.categories or DEFAULT_CATEGORIES
    pages = args.pages if args.pages else None

    items, region_path = fetch_for_region(lr, categories, pages=pages)
    print(f"Saved {len(items)} items -> {region_path}")


if __name__ == "__main__":
    main()

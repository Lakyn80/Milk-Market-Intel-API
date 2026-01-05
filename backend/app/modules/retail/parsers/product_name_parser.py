import re
from typing import Dict, Optional


PRODUCT_TYPES = [
    ("йогурт", "йогурт"),
    ("кефир", "кефир"),
    ("ряженка", "ряженка"),
    ("простокваш", "простокваша"),
    ("сметан", "сметана"),
    ("творог", "творог"),
    ("сыр", "сыр"),
    ("масло", "масло"),
    ("сливк", "сливки"),
    ("молоко", "молоко"),
    ("десерт", "десерт"),
    ("напиток", "напиток"),
    ("питьев", "питьевое"),
    ("детск", "детское"),
]

PACKAGE_TYPES = [
    ("бутыл", "бутылка"),
    ("пакет", "пакет"),
    ("пачк", "пачка"),
    ("стакан", "стакан"),
    ("короб", "коробка"),
    ("ведро", "ведро"),
    ("банка", "банка"),
    ("пленк", "пленка"),
    ("тетра", "тетрапак"),
]

FLAVORS = [
    "персик",
    "клубник",
    "ванил",
    "шоколад",
    "банан",
    "вишн",
    "манго",
    "малина",
    "черник",
    "яблок",
    "карамел",
    "груш",
    "мед",
    "орех",
    "черносмород",
]


def _extract_brand(raw: str) -> Optional[str]:
    match = re.search(r"[«\"]([^»\"]+)[»\"]", raw)
    if match:
        return match.group(1).strip()
    return None


def _extract_brand_prefix(raw: str, raw_l: str) -> Optional[str]:
    # Heuristic: take text before the first known product_type word.
    for key, _ in PRODUCT_TYPES:
        idx = raw_l.find(key)
        if idx > 0:
            candidate = raw[:idx].strip()
            candidate = re.sub(r"[-,:]+$", "", candidate).strip()
            if 1 < len(candidate) <= 40:
                return candidate
    return None


def _extract_fat_percent(raw_l: str) -> Optional[float]:
    m = re.search(r"(\d{1,2}(?:[.,]\d)?)\s*%", raw_l)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", "."))
    except Exception:
        return None


def _extract_type(raw_l: str) -> Optional[str]:
    for key, val in PRODUCT_TYPES:
        if key in raw_l:
            return val
    return None


def _extract_package(raw_l: str) -> Optional[str]:
    for key, val in PACKAGE_TYPES:
        if key in raw_l:
            return val
    return None


def _extract_flavor(raw_l: str) -> Optional[str]:
    for fl in FLAVORS:
        if fl in raw_l:
            return fl
    return None


def _extract_weight_volume(raw_l: str) -> Dict[str, Optional[int]]:
    weight_g = None
    volume_ml = None

    m = re.search(r"(\d+(?:[.,]\d+)?)\s*кг", raw_l)
    if m:
        try:
            weight_g = int(float(m.group(1).replace(",", ".")) * 1000)
        except Exception:
            pass

    m = re.search(r"(\d+(?:[.,]\d+)?)\s*г(?![а-я])", raw_l)
    if m:
        try:
            weight_g = int(float(m.group(1).replace(",", ".")))
        except Exception:
            pass

    m = re.search(r"(\d+(?:[.,]\d+)?)\s*л(?![а-я])", raw_l)
    if m:
        try:
            volume_ml = int(float(m.group(1).replace(",", ".")) * 1000)
        except Exception:
            pass

    m = re.search(r"(\d+(?:[.,]\d+)?)\s*мл", raw_l)
    if m:
        try:
            volume_ml = int(float(m.group(1).replace(",", ".")))
        except Exception:
            pass

    return {"weight_g": weight_g, "volume_ml": volume_ml}


def parse_product_name(name: str) -> Dict[str, Optional[object]]:
    raw = name or ""
    raw_l = raw.lower()

    fat_percent = _extract_fat_percent(raw_l)
    product_type = _extract_type(raw_l)
    package_type = _extract_package(raw_l)
    flavor = _extract_flavor(raw_l)
    brand = _extract_brand(raw) or _extract_brand_prefix(raw, raw_l)
    weight_volume = _extract_weight_volume(raw_l)

    return {
        "raw_name": raw,
        "brand": brand,
        "product_type": product_type,
        "flavor": flavor,
        "fat_percent": fat_percent,
        "package_type": package_type,
        "weight_g": weight_volume.get("weight_g"),
        "volume_ml": weight_volume.get("volume_ml"),
    }

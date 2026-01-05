import re
from typing import Optional, Dict


def normalize_brand(value: str) -> Optional[str]:
    if not value:
        return None
    s = value.strip()
    s = s.strip('"\''"«»")
    s = re.sub(r"\s+", " ", s)
    return s.lower() if s else None


def from_quoted(raw_name: str) -> Optional[str]:
    match = re.search(r"[«\"]([^»\"]+)[»\"]", raw_name)
    if match:
        return normalize_brand(match.group(1))
    return None


def from_prefix(raw_name: str, product_type: Optional[str]) -> Optional[str]:
    if not product_type:
        return None
    raw_l = raw_name.lower()
    idx = raw_l.find(product_type)
    if idx <= 0:
        return None
    prefix = raw_name[:idx].strip()
    prefix = re.sub(r"[-,:]+$", "", prefix).strip()
    if prefix and len(prefix) > 1:
        return normalize_brand(prefix)
    return None


def choose_brand(parsed_brand: Optional[str], raw_name: str, product_type: Optional[str]) -> Dict[str, Optional[str]]:
    # Try explicit brand from parsed layer
    if parsed_brand:
        normalized = normalize_brand(parsed_brand)
        if normalized:
            return {
                "brand_name": normalized,
                "extraction_method": "existing_brand",
                "confidence": "medium",
            }

    # Try quoted brand
    quoted = from_quoted(raw_name)
    if quoted:
        return {
            "brand_name": quoted,
            "extraction_method": "quoted_name",
            "confidence": "medium",
        }

    # Try prefix before product type
    prefix = from_prefix(raw_name, product_type)
    if prefix:
        return {
            "brand_name": prefix,
            "extraction_method": "name_prefix",
            "confidence": "low",
        }

    return {
        "brand_name": None,
        "extraction_method": None,
        "confidence": None,
    }

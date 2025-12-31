import re

CLEAN_PATTERNS = [
    r",\s*офис.*$",
    r",\s*магазин.*$",
    r"представительство.*$",
    r"№\s*\d+",
]

def canonical_company_name(name: str) -> str:
    s = name.lower()

    for p in CLEAN_PATTERNS:
        s = re.sub(p, "", s)

    s = re.sub(r"\s+", " ", s).strip()
    return s

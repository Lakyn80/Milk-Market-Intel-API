import re
from typing import Dict, Tuple

POSITIVE_KEYWORDS = {
    r"молок": 3,
    r"молоч": 3,
    r"сыр": 2,
    r"творог": 2,
    r"йогурт": 2,
    r"слив": 2,
    r"комбинат": 2,
    r"завод": 2,
    r"фабрика": 2,
}

NEGATIVE_KEYWORDS = {
    r"магазин": -3,
    r"маркет": -3,
    r"лавка": -3,
    r"рынок": -3,
    r"ярмарка": -3,
    r"мясо": -2,
    r"рыба": -2,
    r"кондитер": -2,
    r"№": -2,
}

KNOWN_PRODUCERS = {
    "wimm-bill-dann",
    "danone",
    "pepsico",
    "савушкин",
    "экомилк",
}


def score_company(name: str) -> Tuple[int, Dict[str, int]]:
    name_l = name.lower()
    score = 0
    reasons: Dict[str, int] = {}

    for pattern, value in POSITIVE_KEYWORDS.items():
        if re.search(pattern, name_l):
            score += value
            reasons[pattern] = value

    for pattern, value in NEGATIVE_KEYWORDS.items():
        if re.search(pattern, name_l):
            score += value
            reasons[pattern] = value

    for producer in KNOWN_PRODUCERS:
        if producer in name_l:
            score += 3
            reasons[f"known:{producer}"] = 3

    return score, reasons


def is_dairy_b2b(name: str, threshold: int = 2) -> Tuple[bool, int, Dict[str, int]]:
    score, reasons = score_company(name)
    return score >= threshold, score, reasons

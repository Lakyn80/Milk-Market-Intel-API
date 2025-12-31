def normalize_weight(value: float | None, unit: str | None) -> tuple[float | None, str | None]:
    if value is None or unit is None:
        return value, unit

    unit = unit.lower().strip()

    if unit in ("g", "gram", "grams"):
        return value / 1000, "kg"

    if unit in ("kg", "kilogram", "kilograms"):
        return value, "kg"

    if unit in ("ml",):
        return value / 1000, "l"

    if unit in ("l", "liter", "litre"):
        return value, "l"

    return value, unit

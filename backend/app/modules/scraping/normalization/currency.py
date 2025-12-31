def normalize_currency(value: float | None, currency: str | None) -> tuple[float | None, str | None]:
    if value is None or currency is None:
        return value, currency

    currency = currency.upper().strip()

    if currency in ("RUB", "₽"):
        return value, "RUB"

    if currency in ("USD", "$"):
        return value, "USD"

    if currency in ("EUR", "€"):
        return value, "EUR"

    return value, currency

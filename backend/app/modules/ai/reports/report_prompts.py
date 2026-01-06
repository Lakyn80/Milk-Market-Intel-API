PROMPTS = {
    "market_overview": {
        "cs": "Report type: Market Overview. Data je již spočítaná (overview, regiony, kategorie). Neprováděj výpočty ani převody měn, jen interpretuj v češtině. Pokud není uvedena měna, ber vždy RUB, nikdy nepřeváděj na jiné měny.",
        "en": "Report type: Market Overview. Data is precomputed (overview, regions, categories). Do NOT calculate or convert currency; only interpret in English. If currency is not shown, assume RUB and never convert to other currencies.",
        "ru": "Report type: Market Overview. Данные уже посчитаны (overview, регионы, категории). Не рассчитывай и не конвертируй валюту, только интерпретируй по-русски. Если валюта не указана, всегда предполагается RUB, без конвертации.",
    },
    "region_comparison": {
        "cs": "Report type: Region Comparison. Data je již spočítaná. Neprováděj výpočty, jen popiš rozdíly regionů v češtině. Měnu nikdy nepřeváděj, pracuj s RUB.",
        "en": "Report type: Region Comparison. Data is precomputed. Do NOT calculate; just describe differences in English. Never convert currency; use RUB.",
        "ru": "Report type: Region Comparison. Данные уже посчитаны. Не считай, просто опиши различия по-русски. Валюту не конвертируй, используй RUB.",
    },
    "category_deep_dive": {
        "cs": "Report type: Category Deep Dive. Data je již spočítaná. Neprováděj výpočty, jen interpretuj kontext kategorie v češtině. Měnu vždy ponech v RUB, bez převodu.",
        "en": "Report type: Category Deep Dive. Data is precomputed. Do NOT calculate; only interpret the category context in English. Always keep currency in RUB, no conversion.",
        "ru": "Report type: Category Deep Dive. Данные уже посчитаны. Не считай, просто интерпретируй контекст категории по-русски. Валюта только RUB, без конвертации.",
    },
}

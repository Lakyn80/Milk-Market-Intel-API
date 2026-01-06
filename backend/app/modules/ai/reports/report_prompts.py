PROMPTS = {
    "market_overview": {
        "cs": "Report type: Market Overview. Data je již spočítaná (overview, regiony, kategorie). Neprováděj výpočty ani převody měn, jen interpretuj v češtině. Měnu ponech tak, jak je v datech, nic nepřeváděj.",
        "en": "Report type: Market Overview. Data is precomputed (overview, regions, categories). Do NOT calculate or convert currency; only interpret in English. Keep currency exactly as provided in the data.",
        "ru": "Report type: Market Overview. Данные уже посчитаны (overview, регионы, категории). Не рассчитывай и не конвертируй валюту, только интерпретируй по-русски. Оставляй валюту как в данных, без преобразований.",
    },
    "region_comparison": {
        "cs": "Report type: Region Comparison. Data je již spočítaná. Neprováděj výpočty, jen popiš rozdíly regionů v češtině. Měnu nech přesně tak, jak je v datech.",
        "en": "Report type: Region Comparison. Data is precomputed. Do NOT calculate; just describe differences in English. Keep currency as-is from the data.",
        "ru": "Report type: Region Comparison. Данные уже посчитаны. Не считай, просто опиши различия по-русски. Валюту оставляй как в данных.",
    },
    "category_deep_dive": {
        "cs": "Report type: Category Deep Dive. Data je již spočítaná. Neprováděj výpočty, jen interpretuj kontext kategorie v češtině. Měnu nijak neměň, používej přesně, co je v datech.",
        "en": "Report type: Category Deep Dive. Data is precomputed. Do NOT calculate; only interpret the category context in English. Do not alter currency; use exactly what the data provides.",
        "ru": "Report type: Category Deep Dive. Данные уже посчитаны. Не считай, просто интерпретируй контекст категории по-русски. Валюту не меняй, используй как в данных.",
    },
}

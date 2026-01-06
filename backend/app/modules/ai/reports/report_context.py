from typing import Any, Dict, List, Optional

from app.modules.ai.loaders.analytics_loader import load_analytics
from app.modules.ai.reports.report_types import ReportRequest, ReportType


def _normalize_region(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, int):
        return str(value)
    return ""


def _match_region_name(name: Any, target: str) -> bool:
    if not isinstance(name, (str, int)):
        return False
    return _normalize_region(name).lower() == target.lower()


def build_context(req: ReportRequest) -> Dict[str, Any]:
    data = load_analytics()
    ctx: Dict[str, Any] = {"type": req.type.value, "lang": req.lang, "currency": "RUB"}

    if req.type == ReportType.MARKET_OVERVIEW:
        ctx["overview"] = data.get("overview")
        ctx["regions"] = data.get("regions")
        ctx["categories"] = data.get("categories")
        return ctx

    if req.type == ReportType.REGION_COMPARISON:
        if not req.regions or len(req.regions) < 2:
            raise ValueError("region_comparison requires at least two regions")
        requested = [_normalize_region(r) for r in req.regions]
        regions = data.get("regions") or []
        matched: List[Dict[str, Any]] = []
        for region in regions:
            name = region.get("region") if isinstance(region, dict) else None
            if any(_match_region_name(name, target) for target in requested):
                matched.append(region)
        missing = [r for r in requested if not any(_match_region_name(m.get("region"), r) for m in matched if isinstance(m, dict))]
        if missing:
            raise ValueError(f"Regions not found: {', '.join(missing)}")
        ctx["regions"] = matched
        return ctx

    if req.type == ReportType.CATEGORY_DEEP_DIVE:
        if not req.category:
            raise ValueError("category_deep_dive requires category")
        category_key = req.category.strip().lower()
        categories = data.get("categories") or []
        matched_cats = [
            c for c in categories
            if isinstance(c, dict) and isinstance(c.get("category"), str) and c["category"].strip().lower() == category_key
        ]
        if not matched_cats:
            raise ValueError(f"Category not found: {req.category}")
        prices = data.get("prices") or []
        prices_sample = [
            p for p in prices
            if isinstance(p, dict) and isinstance(p.get("category"), str) and p["category"].strip().lower() == category_key
        ][:50]
        ctx["category"] = req.category
        ctx["category_summary"] = matched_cats
        ctx["prices_sample"] = prices_sample
        ctx["regions"] = data.get("regions")
        return ctx

    raise ValueError(f"Unsupported report type: {req.type}")

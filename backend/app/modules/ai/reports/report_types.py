from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class ReportType(str, Enum):
    MARKET_OVERVIEW = "market_overview"
    REGION_COMPARISON = "region_comparison"
    CATEGORY_DEEP_DIVE = "category_deep_dive"


class ReportRequest(BaseModel):
    type: ReportType
    lang: str = Field("cs", pattern="^(cs|en|ru)$")
    regions: Optional[List[str | int]] = None
    category: Optional[str] = None

    @validator("regions", pre=True)
    def normalize_regions(cls, v):
        if v is None:
            return v
        if isinstance(v, (str, int)):
            return [v]
        if isinstance(v, list):
            return v
        raise ValueError("regions must be list, string, int, or null")

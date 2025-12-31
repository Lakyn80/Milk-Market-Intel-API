from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    country: str = "RU"
    region: str | None = None
    website: str | None = None


class CompanyRead(BaseModel):
    id: int
    name: str
    country: str
    region: str | None
    website: str | None

    class Config:
        from_attributes = True

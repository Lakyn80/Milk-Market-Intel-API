from sqlalchemy.orm import Session
from app.modules.companies.models import Company


class CompanyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, *, name: str, country: str = 'RU', region: str | None = None, website: str | None = None) -> Company:
        company = Company(
            name=name,
            country=country,
            region=region,
            website=website,
        )
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def get_by_name(self, name: str) -> Company | None:
        return self.db.query(Company).filter(Company.name == name).first()

    def list_all(self) -> list[Company]:
        return self.db.query(Company).order_by(Company.name).all()

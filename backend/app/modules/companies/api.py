from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.modules.companies.repository import CompanyRepository
from app.modules.companies.schemas import CompanyCreate, CompanyRead

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=CompanyRead)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    repo = CompanyRepository(db)
    return repo.create(**payload.dict())


@router.get("/", response_model=list[CompanyRead])
def list_companies(db: Session = Depends(get_db)):
    repo = CompanyRepository(db)
    return repo.list_all()

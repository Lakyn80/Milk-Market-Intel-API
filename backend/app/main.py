from fastapi import FastAPI

from .router import api_router
from .db.base import Base
from .db.session import engine

# IMPORT MODELS (nutné pro create_all)
from .modules.companies.models import Company  # noqa: F401


app = FastAPI(
    title="Milk Market Intel API",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(api_router)

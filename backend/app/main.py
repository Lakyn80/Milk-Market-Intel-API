from fastapi import FastAPI
from app.router import api_router

app = FastAPI(
    title="Milk Market Intel API",
    version="0.1.0"
)

app.include_router(api_router)

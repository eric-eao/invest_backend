from fastapi import FastAPI

from app.routes import categories

app = FastAPI(
    title="Invest Control",
    description="API de controle de investimentos",
    version="0.1.0",
)

app.include_router(categories.router, prefix="/categories")

from fastapi import FastAPI

from app.routes import categories
from app.routes.admin import benchmarks

app = FastAPI(
    title="Invest Control",
    description="API de controle de investimentos",
    version="0.1.0",
)

app.include_router(categories.router, prefix="/categories")
app.include_router(benchmarks.router, prefix="/admin/benchmarks")

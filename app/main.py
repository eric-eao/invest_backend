from fastapi import FastAPI

from app.routes.private_credit import categories
from app.routes.private_credit import assets
from app.routes.admin import benchmarks
from app.routes.admin import modules

from app.routes import movements

app = FastAPI(
    title="Invest Control",
    description="API de controle de investimentos",
    version="0.1.0",
)

app.include_router(categories.router, prefix="/private-credit/categories")
app.include_router(assets.router, prefix="/private-credit/assets")
app.include_router(benchmarks.router, prefix="/admin/benchmarks")
app.include_router(modules.router, prefix="/admin/modules")
app.include_router(movements.router, prefix="/movements")

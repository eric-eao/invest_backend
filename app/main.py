from fastapi import FastAPI

from app.routes.private_credit.categories import router as categories_router
from app.routes.private_credit.assets import router as assets_router
from app.routes.admin.modules import  router as modules_router
from app.routes.admin.benchmarks import router as admin_benchmarks_router
from app.routes.snapshot.benchmarks import router as snapshot_benchmarks_router
from app.routes.movements import router as movements_router
from app.routes.export import router as export_router

app = FastAPI(
    title="Invest Control",
    description="API de controle de investimentos",
    version="0.1.0",
)

app.include_router(categories_router, prefix="/private-credit/categories")
app.include_router(assets_router, prefix="/private-credit/assets")
app.include_router(admin_benchmarks_router, prefix="/admin/benchmarks")
app.include_router(modules_router, prefix="/admin/modules")
app.include_router(movements_router, prefix="/movements")
app.include_router(snapshot_benchmarks_router, prefix="/snapshot-benchmarks")
app.include_router(export_router, prefix="/exports")

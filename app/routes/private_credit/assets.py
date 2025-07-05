from fastapi import APIRouter, Body, Depends, Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.db.session import get_db
from app.core.modules.private_credit.assets.handlers import asset_handler
from app.schemas.private_credit_asset import PrivateCreditAssetOut, PrivateCreditAssetCreate, PrivateCreditAssetUpdate


router = APIRouter(tags=["private_credit_assets"])


@router.get("/", response_model=List[PrivateCreditAssetOut])
def list_assets(db: Session = Depends(get_db)):
    return asset_handler.list_assets(db)


@router.get("/{asset_id}", response_model=PrivateCreditAssetOut)
def get_asset(asset_id: UUID, db: Session = Depends(get_db)):
    return asset_handler.get_asset(db, asset_id)


@router.post("/", response_model=PrivateCreditAssetOut, status_code=201)
def create_asset(asset_in: PrivateCreditAssetCreate, db: Session = Depends(get_db)):
    return asset_handler.create_asset(db, asset_in)


@router.patch("/{asset_id}", response_model=PrivateCreditAssetOut)
def update_asset(
    asset_id: UUID,
    updates: PrivateCreditAssetUpdate = Body(..., embed=False),
    db: Session = Depends(get_db)
):
    print(">>>> DEBUG ENTROU NA ROTA")
    return asset_handler.update_asset(db, asset_id, updates)


@router.delete("/{asset_id}", status_code=204)
def delete_asset(asset_id: UUID, db: Session = Depends(get_db)):
    asset_handler.delete_asset(db, asset_id)
    return Response(status_code=204)

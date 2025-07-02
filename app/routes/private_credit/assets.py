from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.db.session import get_db
from app.core.modules.private_credit.assets.handlers import asset_handler
from app.schemas.private_credit_asset import PrivateCreditAssetOut, PrivateCreditAssetCreate, PrivateCreditAssetUpdate

router = APIRouter(tags=["Private-credit-assets"])


@router.get("/", response_model=List[PrivateCreditAssetOut])
def list_assets(db: Session = Depends(get_db)):
    return asset_handler.list_assets(db)


@router.get("/{asset_id}", response_model=PrivateCreditAssetOut)
def get_asset(asset_id: UUID, db: Session = Depends(get_db)):
    return asset_handler.get_asset(db, asset_id)


@router.post("/", response_model=PrivateCreditAssetOut)
def create_asset(asset_in: PrivateCreditAssetCreate, db: Session = Depends(get_db)):
    return asset_handler.create_asset(db, asset_in)


@router.put("/{asset_id}", response_model=PrivateCreditAssetOut)
def update_asset(asset_id: UUID, updates: PrivateCreditAssetUpdate, db: Session = Depends(get_db)):
    return asset_handler.update_asset(db, asset_id, updates)


@router.delete("/{asset_id}")
def delete_asset(asset_id: UUID, db: Session = Depends(get_db)):
    asset_handler.delete_asset(db, asset_id)
    return {"detail": "Ativo removido com sucesso"}

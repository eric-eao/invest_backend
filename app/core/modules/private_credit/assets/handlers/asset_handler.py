from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException
from app.core.modules.private_credit.assets.validators.asset_validator import asset_validator
from app.models.private_credit_asset import PrivateCreditAsset
from app.schemas.private_credit_asset import PrivateCreditAssetCreate, PrivateCreditAssetUpdate

def list_assets(db: Session):
    return db.query(PrivateCreditAsset).all()

def get_asset(db: Session, asset_id: UUID):
    item = db.query(PrivateCreditAsset).filter(PrivateCreditAsset.id == asset_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")
    return item

def create_asset(db: Session, asset_in: PrivateCreditAssetCreate):
    asset_validator(
        asset_in.rate_type,
        asset_in.indexer,
        asset_in.fixed_rate,
        asset_in.spread,
        asset_in.index_percent
    )
    db_item = PrivateCreditAsset(**asset_in.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_asset(db: Session, asset_id: UUID, updates: PrivateCreditAssetUpdate):
    item = db.query(PrivateCreditAsset).filter(PrivateCreditAsset.id == asset_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")

    # mescla os valores antigos com os novos
    data = {
        "rate_type": item.rate_type,
        "indexer": item.indexer,
        "fixed_rate": item.fixed_rate,
        "spread": item.spread,
        "index_percent": item.index_percent,
    }
    data.update(updates.model_dump(exclude_unset=True))

    # chama o validador, agora com os dados completos
    asset_validator(
        data["rate_type"],
        data["indexer"],
        data["fixed_rate"],
        data["spread"],
        data["index_percent"],
    )

    # aplica os updates no item
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


def delete_asset(db: Session, asset_id: UUID):
    item = db.query(PrivateCreditAsset).filter(PrivateCreditAsset.id == asset_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")
    db.delete(item)
    db.commit()

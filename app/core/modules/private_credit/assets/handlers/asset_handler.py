from decimal import Decimal
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.core.modules.movements.services import create_initial_movement_asset_service
from app.core.modules.private_credit.assets.validators.asset_validator import asset_validator
from app.models.private_credit.private_credit_asset import PrivateCreditAsset
from app.schemas.private_credit_asset import PrivateCreditAssetCreate, PrivateCreditAssetOut, PrivateCreditAssetUpdate

def list_assets(db: Session):
    assets = db.query(PrivateCreditAsset).all()
    result = []

    for item in assets:
        data = PrivateCreditAssetOut.from_orm(item).dict()

        if item.current_unit_price and item.total_quantity:
            data["current_amount"] = (Decimal(item.current_unit_price) * Decimal(item.total_quantity)).quantize(Decimal("0.01"))
        else:
            data["current_amount"] = None

        result.append(data)

    return result


def get_asset(db: Session, asset_id: UUID):
    item = db.query(PrivateCreditAsset).filter(PrivateCreditAsset.id == asset_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")

    data = PrivateCreditAssetOut.from_orm(item).dict()

    if item.current_unit_price and item.total_quantity:
        data["current_amount"] = (Decimal(item.current_unit_price) * Decimal(item.total_quantity)).quantize(Decimal("0.01"))
    else:
        data["current_amount"] = None

    return data


def create_asset(db: Session, asset_in: PrivateCreditAssetCreate):
    # prevenir duplicidade
    existing = db.query(PrivateCreditAsset).filter(PrivateCreditAsset.code == asset_in.code).first()
    if existing:
        raise HTTPException(status_code=409, detail="Ativo com este código já existe")

    # validando as regras
    asset_validator(
        asset_in.rate_type,
        asset_in.indexer,
        asset_in.fixed_rate,
        asset_in.spread,
        asset_in.index_percent
    )

    try:
        db_asset = PrivateCreditAsset(
            description=asset_in.description,
            code=asset_in.code,
            institution=asset_in.institution,
            category_id=asset_in.category_id,
            maturity_date=asset_in.maturity_date,
            rate_type=asset_in.rate_type,
            indexer=asset_in.indexer,
            fixed_rate=asset_in.fixed_rate,
            spread=asset_in.spread,
            index_percent=asset_in.index_percent,
            active=asset_in.active,
        )
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro de integridade ao criar ativo")

    # movimento inicial
    if asset_in.initial_movement:
        result = create_initial_movement_asset_service.create_initial_movement_asset(
            db=db,
            movement_in=asset_in.initial_movement,
            asset_id=db_asset.id
        )
        db_asset.average_unit_price = result["average_unit_price"]
        db_asset.total_quantity = result["total_quantity"]
        db_asset.total_cost = result["total_cost"]
        db.commit()
        db.refresh(db_asset)

    return db_asset


def update_asset(db: Session, asset_id: UUID, updates: PrivateCreditAssetUpdate):
    print(">>>> DEBUG HANDLER UPDATE INICIOU")
    item = db.query(PrivateCreditAsset).filter(PrivateCreditAsset.id == asset_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")

    # mescla dados completos
    data = {
        "rate_type": item.rate_type,
        "indexer": item.indexer,
        "fixed_rate": item.fixed_rate,
        "spread": item.spread,
        "index_percent": item.index_percent,
    }
    data.update(updates.model_dump(exclude_unset=True))

    print("\n>>>> DEBUG UPDATES model_dump:", updates.model_dump(exclude_unset=True))
    print(">>>> DEBUG MERGED data dict:", data)

    asset_validator(
        data["rate_type"],
        data["indexer"],
        data["fixed_rate"],
        data["spread"],
        data["index_percent"]
    )

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



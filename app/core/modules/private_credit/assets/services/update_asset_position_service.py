from decimal import Decimal
from sqlalchemy import func
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.movements import Movement
from app.models.private_credit.private_credit_asset import PrivateCreditAsset

def update_asset_position(db: Session, asset_id: UUID):

    # agregados dos movimentos (considerando todos, PENDING + CONFIRMED)
    result = (
        db.query(
            func.sum(Movement.quantity).label("total_quantity"),
            func.sum(Movement.amount).label("total_cost"),
        )
        .filter(Movement.asset_id == asset_id)
        .one()
    )

    total_quantity = result.total_quantity or Decimal(0)
    total_cost = result.total_cost or Decimal(0)

    average_unit_price = (
        total_cost / total_quantity if total_quantity > 0 else Decimal(0)
    )

    asset = db.query(PrivateCreditAsset).filter(PrivateCreditAsset.id == asset_id).first()
    if asset:
        asset.total_quantity = total_quantity
        asset.total_cost = total_cost
        asset.average_unit_price = average_unit_price

        db.commit()
        db.refresh(asset)

        print(
            f"""
            asset atualizado => 
            id={asset.id}, 
            total_quantity={asset.total_quantity}, 
            total_cost={asset.total_cost}, 
            average_unit_price={asset.average_unit_price}
            """
        )

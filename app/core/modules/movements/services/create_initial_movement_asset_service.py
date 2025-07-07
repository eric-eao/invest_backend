from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.modules.control.handlers.portfolio_date_handler import sync_portfolio_dates
from app.core.modules.private_credit.assets.services.update_asset_position_service import update_asset_position
from app.models.movements import Movement, MovementStatus
from app.schemas.movement import MovementCreate
from uuid import UUID


def create_initial_movement_asset(
    db: Session,
    movement_in: MovementCreate,
    asset_id: UUID
):
    if movement_in.movement_type != "DEPOSIT":
        raise HTTPException(
            status_code=400,
            detail="O movimento inicial obrigatoriamente deve ser DEPOSIT."
        )

    amount = movement_in.quantity * movement_in.unit_price

    db_movement = Movement(
        asset_id=asset_id,
        module_id=movement_in.module_id,
        movement_type=movement_in.movement_type,
        quantity=movement_in.quantity,
        unit_price=movement_in.unit_price,
        amount=amount,
        movement_date=movement_in.movement_date,
        settlement_date=movement_in.settlement_date,
        broker=movement_in.broker,
        transaction_reference=movement_in.transaction_reference,
        status=MovementStatus.CONFIRMED,
        notes=movement_in.notes,
        source=movement_in.source,
    )
    db.add(db_movement)

    sync_portfolio_dates(db, movement_in.module_id)
    update_asset_position(db, movement_in.asset_id)

    # retorna valores para atualizar o asset
    return {
        "average_unit_price": movement_in.unit_price,
        "total_quantity": movement_in.quantity,
        "total_cost": amount
    }

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.modules.control.handlers.portfolio_date_handler import sync_portfolio_dates
from app.core.modules.movements.services.process_positions_service import process_positions_service
from app.core.modules.private_credit.assets.services.update_asset_position_service import update_asset_position
from app.models.movements import Movement, MovementStatus
from app.models.positions import Position
from app.schemas.enums import MovementType
from app.schemas.movement import MovementCreate
from uuid import UUID


def create_initial_movement_asset(
    db: Session,
    movement_in: MovementCreate,
    asset_id: UUID
):
    # validação do tipo
    if movement_in.movement_type != MovementType.DEPOSIT:
        raise HTTPException(
            status_code=400,
            detail="O movimento inicial obrigatoriamente deve ser DEPOSIT."
        )

    # validação mínima de valores
    if movement_in.quantity <= 0 or movement_in.unit_price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantidade e preço unitário devem ser maiores que zero."
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
        status=MovementStatus.PENDING,
        notes=movement_in.notes,
        source=movement_in.source,
    )
    db.add(db_movement)

    # atualiza datas de controle e posição
    sync_portfolio_dates(db, movement_in.module_id)
    update_asset_position(db, asset_id)
    process_positions_service(
        db=db,
        module_id=movement_in.module_id,
        position_model=Position
    )

    # retorna dados agregados para atualizar o asset
    return {
        "average_unit_price": movement_in.unit_price,
        "total_quantity": movement_in.quantity,
        "total_cost": amount
    }

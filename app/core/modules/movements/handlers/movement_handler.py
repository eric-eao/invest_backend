from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.modules.control.handlers.portfolio_date_handler import sync_portfolio_dates
from app.models.movements import Movement, MovementStatus
from app.schemas.movement import MovementCreate, MovementUpdate
from uuid import UUID

def create_movement(db: Session, movement_in: MovementCreate) -> Movement:
    amount = movement_in.quantity * movement_in.unit_price

    new_movement = Movement(
        asset_id=movement_in.asset_id,
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

    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    sync_portfolio_dates(db, movement_in.module_id)

    return new_movement


def get_movement(db: Session, movement_id: UUID) -> Movement:
    movement = db.query(Movement).filter(Movement.id == movement_id).first()
    if not movement:
        raise HTTPException(status_code=404, detail="Movimento não encontrado")
    return movement


def update_movement(db: Session, movement_id: UUID, movement_in: MovementUpdate) -> Movement:
    movement = get_movement(db, movement_id)

    for field, value in movement_in.model_dump(exclude_unset=True).items():
        setattr(movement, field, value)

    # recalcula amount se quantidade ou preço mudarem
    if movement_in.quantity or movement_in.unit_price:
        q = Decimal(str(movement_in.quantity)) if movement_in.quantity else movement.quantity
        p = movement_in.unit_price if movement_in.unit_price else movement.unit_price
        movement.amount = q * p

    db.commit()
    db.refresh(movement)

    movement = get_movement(db, movement_id)
    sync_portfolio_dates(db, movement.module_id)

    return movement


def delete_movement(db: Session, movement_id: UUID):
    movement = get_movement(db, movement_id)
    module_id = movement.module_id
    db.delete(movement)
    db.commit()

    # sincroniza depois de remover
    sync_portfolio_dates(db, module_id)
    


def create_initial_movement_for_asset(
    db: Session,
    movement_in: MovementCreate,
    asset_id: UUID
):
    if movement_in.movement_type != "APORTE":
        raise HTTPException(
            status_code=400,
            detail="O movimento inicial obrigatoriamente deve ser APORTE."
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

    # retorna valores para atualizar o asset
    return {
        "average_unit_price": movement_in.unit_price,
        "total_quantity": movement_in.quantity,
        "total_cost": amount
    }

from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.modules.control.handlers.portfolio_date_handler import sync_portfolio_dates
from app.core.modules.movements.services.process_positions_service import process_positions_service
from app.core.modules.private_credit.assets.services.update_asset_position_service import update_asset_position
from app.models.movements import Movement, MovementStatus
from app.models.positions import Position
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
    update_asset_position(db, movement_in.asset_id)
    process_positions_service(
        db=db,
        module_id=movement_in.module_id,
        position_model=Position
    )

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
        movement.status = MovementStatus.PENDING
        
    # recalcula amount se quantidade ou preço mudarem
    if movement_in.quantity or movement_in.unit_price:
        q = Decimal(str(movement_in.quantity)) if movement_in.quantity else movement.quantity
        p = movement_in.unit_price if movement_in.unit_price else movement.unit_price
        movement.amount = q * p

    db.commit()
    db.refresh(movement)

    asset_id = movement.asset_id

    sync_portfolio_dates(db, movement.module_id)
    update_asset_position(db, asset_id)
    process_positions_service(
        db=db,
        module_id=movement.module_id,
        position_model=Position
    )

    return movement


def delete_movement(db: Session, movement_id: UUID):
    movement = get_movement(db, movement_id)
    module_id = movement.module_id
    asset_id = movement.asset_id

    # remove o movimento
    db.delete(movement)
    db.commit()

    # após deletar, marca como PENDING apenas os movimentos do mesmo asset
    db.query(Movement).filter(
        Movement.asset_id == asset_id,
        Movement.status == MovementStatus.CONFIRMED
    ).update({"status": MovementStatus.PENDING})
    db.commit()

    # sincroniza datas do portfólio
    sync_portfolio_dates(db, module_id)

    # atualiza o custo médio do asset
    update_asset_position(db, asset_id)

    # processa posições apenas para movimentos pendentes
    process_positions_service(
        db=db,
        module_id=module_id,
        position_model=Position
    )

    return {"message": f"Movimento {movement_id} excluído e posições reprocessadas para o asset {asset_id}."}



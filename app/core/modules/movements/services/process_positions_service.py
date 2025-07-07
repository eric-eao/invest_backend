from sqlalchemy.orm import Session
from sqlalchemy import asc
from decimal import Decimal
from app.models.movements import Movement, MovementType, MovementStatus

def process_positions_generic_service(
    db: Session,
    module_id: str,
    position_model,
) -> dict:

    try:
        # 1️⃣ apaga posições anteriores do módulo
        db.query(position_model).filter(
            position_model.module_id == module_id
        ).delete()
        db.commit()

        # 2️⃣ busca movimentos confirmados do módulo
        movements = (
            db.query(Movement)
            .filter(
                Movement.module_id == module_id,
                Movement.status == MovementStatus.CONFIRMED,
            )
            .order_by(asc(Movement.movement_date), asc(Movement.created_at))
            .all()
        )

        if not movements:
            return {"message": "Nenhum movimento confirmado para processar."}

        for mv in movements:
            if mv.movement_type == MovementType.DEPOSIT:
                # cria novo lote
                new_lot = position_model(
                    asset_id=mv.asset_id,
                    module_id=mv.module_id,
                    quantity_initial=mv.quantity,
                    quantity_current=mv.quantity,
                    unit_price_initial=mv.unit_price,
                    total_invested=mv.amount,
                    lot_start_date=mv.movement_date,
                    last_valuation_date=None,
                    current_unit_price=None,
                    profitability_percent=None,
                    profitability_amount=None,
                )
                db.add(new_lot)

            elif mv.movement_type in [
                MovementType.PARTIAL_REDEMPTION,
                MovementType.FULL_REDEMPTION
            ]:
                quantity_to_redeem = mv.quantity

                open_lots = (
                    db.query(position_model)
                    .filter(
                        position_model.asset_id == mv.asset_id,
                        position_model.module_id == mv.module_id,
                        position_model.quantity_current > 0,
                    )
                    .order_by(asc(position_model.lot_start_date))
                    .all()
                )

                for lot in open_lots:
                    if quantity_to_redeem <= 0:
                        break

                    if lot.quantity_current >= quantity_to_redeem:
                        lot.quantity_current -= quantity_to_redeem
                        quantity_to_redeem = Decimal(0)
                        if lot.quantity_current == 0:
                            lot.lot_end_date = mv.movement_date
                        break
                    else:
                        quantity_to_redeem -= lot.quantity_current
                        lot.quantity_current = Decimal(0)
                        lot.lot_end_date = mv.movement_date

        db.commit()
        return {"message": f"Posições recalculadas com sucesso para módulo {module_id}"}

    except Exception as e:
        db.rollback()
        raise Exception(f"Erro ao processar posições genéricas: {str(e)}")

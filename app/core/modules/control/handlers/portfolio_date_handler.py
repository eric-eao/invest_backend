from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from app.models.control.control_portfolio_date import ControlPortfolioDate
from app.models.movements import Movement
from app.schemas.control_portfolio_date import ControlPortfolioDateCreate, ControlPortfolioDateUpdate


def list_portfolio_dates(db: Session):
    return db.query(ControlPortfolioDate).options(joinedload(ControlPortfolioDate.module)).all()


def get_portfolio_date(db: Session, portfolio_date_id: UUID):
    item = (
        db.query(ControlPortfolioDate)
        .options(joinedload(ControlPortfolioDate.module))
        .filter(ControlPortfolioDate.id == portfolio_date_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Controle de data não encontrado")
    return item


def create_portfolio_date(db: Session, data_in: ControlPortfolioDateCreate):
    item = ControlPortfolioDate(**data_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def sync_portfolio_dates(db: Session, module_id: UUID):
    control = db.query(ControlPortfolioDate).filter(
        ControlPortfolioDate.module_id == module_id
    ).first()

    if not control:
        raise HTTPException(
            status_code=404,
            detail=f"Controle de portfólio (control_portfolio_dates) não encontrado para module_id={module_id}"
        )

    first_date = db.query(func.min(Movement.movement_date)).filter(
        Movement.module_id == module_id
    ).scalar()

    last_date = db.query(func.max(Movement.movement_date)).filter(
        Movement.module_id == module_id
    ).scalar()

    control.first_investiment = first_date
    control.last_investiment = last_date
    control.updated_at = func.now()

    db.commit()
    db.refresh(control)
    return control
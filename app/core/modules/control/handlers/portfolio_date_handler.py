from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from app.models.control_portfolio_date import ControlPortfolioDate
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

def update_portfolio_date(db: Session, portfolio_date_id: UUID, updates: ControlPortfolioDateUpdate):
    item = db.query(ControlPortfolioDate).filter(ControlPortfolioDate.id == portfolio_date_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Controle de data não encontrado")
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item

def delete_portfolio_date(db: Session, portfolio_date_id: UUID):
    item = db.query(ControlPortfolioDate).filter(ControlPortfolioDate.id == portfolio_date_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Controle de data não encontrado")
    db.delete(item)
    db.commit()

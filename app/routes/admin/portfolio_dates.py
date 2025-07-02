from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.db.session import get_db
from app.core.modules.control.handlers import portfolio_date_handler
from app.schemas.control_portfolio_date import ControlPortfolioDateOut, ControlPortfolioDateCreate, ControlPortfolioDateUpdate


router = APIRouter(tags=["portfolio-dates"])

@router.get("/", response_model=List[ControlPortfolioDateOut])
def list_portfolio_dates(db: Session = Depends(get_db)):
    return portfolio_date_handler.list_portfolio_dates(db)

@router.get("/{portfolio_date_id}", response_model=ControlPortfolioDateOut)
def get_portfolio_date(portfolio_date_id: UUID, db: Session = Depends(get_db)):
    return portfolio_date_handler.get_portfolio_date(db, portfolio_date_id)

@router.post("/", response_model=ControlPortfolioDateOut)
def create_portfolio_date(data_in: ControlPortfolioDateCreate, db: Session = Depends(get_db)):
    return portfolio_date_handler.create_portfolio_date(db, data_in)

@router.put("/{portfolio_date_id}", response_model=ControlPortfolioDateOut)
def update_portfolio_date(portfolio_date_id: UUID, updates: ControlPortfolioDateUpdate, db: Session = Depends(get_db)):
    return portfolio_date_handler.update_portfolio_date(db, portfolio_date_id, updates)

@router.delete("/{portfolio_date_id}")
def delete_portfolio_date(portfolio_date_id: UUID, db: Session = Depends(get_db)):
    portfolio_date_handler.delete_portfolio_date(db, portfolio_date_id)
    return {"detail": "Controle de data removido com sucesso"}

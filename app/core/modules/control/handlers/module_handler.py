from sqlalchemy import func
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException
from app.models.control.control_module import ControlModule
from app.models.control.control_portfolio_date import ControlPortfolioDate
from app.schemas.control_module import ControlModuleCreate, ControlModuleUpdate


def list_modules(db: Session):
    return db.query(ControlModule).all()


def get_module(db: Session, module_id: UUID):
    module = db.query(ControlModule).filter(ControlModule.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    return module


def create_module(db: Session, module_in: ControlModuleCreate):
    db_module = ControlModule(**module_in.model_dump())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)

    # cria automaticamente o controle de portfolio_dates
    db_portfolio = ControlPortfolioDate(
        module_id=db_module.id,
        first_investiment=None,
        last_investiment=None,
        active=True,
        updated_at=func.now()
    )
    db.add(db_portfolio)
    db.commit()

    return db_module


def update_module(db: Session, module_id: UUID, updates: ControlModuleUpdate):
    module = db.query(ControlModule).filter(ControlModule.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")

    control_portfolio = db.query(ControlPortfolioDate).filter(
        ControlPortfolioDate.module_id == module_id
    ).first()

    if not control_portfolio:
        raise HTTPException(
            status_code=404,
            detail="Controle de portfólio (control_portfolio_dates) não encontrado para o módulo."
        )

    # aplica updates no módulo
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(module, field, value)

    # se o campo active for atualizado, sincroniza no portfolio_date
    if updates.active is not None:
        control_portfolio.active = updates.active
        control_portfolio.updated_at = func.now()

    db.commit()
    db.refresh(module)
    return module


def delete_module(db: Session, module_id: UUID):
    module = db.query(ControlModule).filter(ControlModule.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")

    # busca e remove o portfolio_date vinculado
    control_portfolio = db.query(ControlPortfolioDate).filter(
        ControlPortfolioDate.module_id == module_id
    ).first()

    if control_portfolio:
        db.delete(control_portfolio)

    db.delete(module)
    db.commit()

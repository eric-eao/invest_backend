from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException
from app.models.control_module import ControlModule
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
    return db_module

def update_module(db: Session, module_id: UUID, updates: ControlModuleUpdate):
    module = db.query(ControlModule).filter(ControlModule.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(module, field, value)
    db.commit()
    db.refresh(module)
    return module

def delete_module(db: Session, module_id: UUID):
    module = db.query(ControlModule).filter(ControlModule.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    db.delete(module)
    db.commit()

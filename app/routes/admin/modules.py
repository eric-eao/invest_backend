from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.db.session import get_db
from app.schemas.control_module import ControlModuleOut, ControlModuleCreate, ControlModuleUpdate
from app.core.modules.control.handlers import module_handler

router = APIRouter(tags=["modules"])

@router.get("/", response_model=List[ControlModuleOut])
def list_modules(db: Session = Depends(get_db)):
    return module_handler.list_modules(db)

@router.get("/{module_id}", response_model=ControlModuleOut)
def get_module(module_id: str, db: Session = Depends(get_db)):
    return module_handler.get_module(db, module_id)

@router.post("/", response_model=ControlModuleOut)
def create_module(module_in: ControlModuleCreate, db: Session = Depends(get_db)):
    return module_handler.create_module(db, module_in)

@router.put("/{module_id}", response_model=ControlModuleOut)
def update_module(module_id: str, updates: ControlModuleUpdate, db: Session = Depends(get_db)):
    return module_handler.update_module(db, module_id, updates)

@router.delete("/{module_id}")
def delete_module(module_id: str, db: Session = Depends(get_db)):
    module_handler.delete_module(db, module_id)
    return {"detail": "Módulo removido com sucesso"}

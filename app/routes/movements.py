from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.schemas.movement import MovementOut, MovementCreate, MovementUpdate
from app.core.modules.movements.handlers import movement_handler
from app.core.db.session import get_db

router = APIRouter(tags=["movements"])


@router.post("/", response_model=MovementOut, status_code=201)
def create_movement(movement_in: MovementCreate, db: Session = Depends(get_db)):
    return movement_handler.create_movement(db, movement_in)


@router.get("/{movement_id}", response_model=MovementOut)
def read_movement(movement_id: UUID, db: Session = Depends(get_db)):
    return movement_handler.get_movement(db, movement_id)


@router.put("/{movement_id}", response_model=MovementOut)
def update_movement(movement_id: UUID, movement_in: MovementUpdate, db: Session = Depends(get_db)):
    return movement_handler.update_movement(db, movement_id, movement_in)


@router.delete("/{movement_id}", status_code=204)
def delete_movement(movement_id: UUID, db: Session = Depends(get_db)):
    movement_handler.delete_movement(db, movement_id)
    return {"ok": True}

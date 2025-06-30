from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.core.db.session import get_db
from app.core.categories.handlers import category_handler


router = APIRouter(tags=["categories"])


@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return category_handler.list_categories(db)


@router.post("/", response_model=CategoryOut, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return category_handler.create_category(db, category)


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    return category_handler.get_category(db, category_id)


@router.patch("/{category_id}", response_model=CategoryOut)
def update_category(category_id: UUID, updates: CategoryUpdate, db: Session = Depends(get_db)):
    return category_handler.update_category(db, category_id, updates)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    return category_handler.delete_category(db, category_id)

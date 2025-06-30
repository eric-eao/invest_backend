from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category
from fastapi import HTTPException
from uuid import UUID


def list_categories(db: Session):
    return db.query(Category).all()


def create_category(db: Session, category_in: CategoryCreate):
    db_category = Category(**category_in.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: UUID):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def update_category(db: Session, category_id: UUID, updates: CategoryUpdate):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: UUID):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()

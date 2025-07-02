from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.private_credit_category import CategoryCreate, CategoryUpdate
from app.models.private_credit_category import Category
from fastapi import HTTPException
from uuid import UUID


def list_categories(db: Session):
    return db.query(Category).all()


def create_category(db: Session, category_in: CategoryCreate):
    db_category = Category(
        **category_in.dict(), 
        module="private_credit"
    )
    db.add(db_category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Categoria já existe")
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: UUID):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category


def update_category(db: Session, category_id: UUID, updates: CategoryUpdate):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: UUID):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(category)
    db.commit()

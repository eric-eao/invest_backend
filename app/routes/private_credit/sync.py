from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.core.modules.private_credit.assets.handlers.calculate_private_credit_handler import calculate_private_credit_handler

router = APIRouter(tags=["private_credit_sync"])

@router.post("/")
def sync_private_credit(db: Session = Depends(get_db)):
    try:
        return calculate_private_credit_handler(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from sqlalchemy.orm import Session
from app.core.modules.private_credit.assets.services.calculate_private_credit_service import calculate_private_credit_service
from app.core.modules.private_credit.assets.services.update_asset_summary_service import update_private_credit_asset_summaries

def calculate_private_credit_handler(db: Session) -> dict:
    result = calculate_private_credit_service(db)
    update_private_credit_asset_summaries(db)
    return result

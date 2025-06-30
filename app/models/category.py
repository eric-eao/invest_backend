import uuid
from sqlalchemy import Column, String, Float, Boolean, Enum, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import CurrencyEnum

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    allocation_planned = Column(Float, nullable=False)
    currency = Column(Enum(CurrencyEnum, name="currency_enum"), nullable=False, default=CurrencyEnum.BRL)
    active = Column(Boolean, default=True, nullable=False)
    module = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)

    __table_args__ = (
        # nome único dentro do módulo
        # evita duas categorias chamadas "Tesouro" no mesmo módulo
        # mas permite "Tesouro" no bonds e no private_credit por exemplo
        # UNIQUE(name, module)
        UniqueConstraint("name", "module", name="uix_category_name_module"),
        {"sqlite_autoincrement": True},
    )


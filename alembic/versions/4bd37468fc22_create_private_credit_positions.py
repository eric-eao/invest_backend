"""create private_credit_positions

Revision ID: 4bd37468fc22
Revises: 55bcff81ebc7
Create Date: 2025-07-06 20:57:13.229843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = '4bd37468fc22'
down_revision: Union[str, Sequence[str], None] = '55bcff81ebc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'private_credit_positions',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('asset_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('module_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('quantity_initial', sa.DECIMAL(20, 6), nullable=False),
        sa.Column('quantity_current', sa.DECIMAL(20, 6), nullable=False),
        sa.Column('unit_price_initial', sa.DECIMAL(20, 6), nullable=False),
        sa.Column('total_invested', sa.DECIMAL(20, 6), nullable=False),
        sa.Column('lot_start_date', sa.Date, nullable=False),
        sa.Column('lot_end_date', sa.Date, nullable=True),
        sa.Column('current_unit_price', sa.DECIMAL(20, 6), nullable=True),
        sa.Column('profitability_percent', sa.DECIMAL(20, 6), nullable=True),
        sa.Column('profitability_amount', sa.DECIMAL(20, 6), nullable=True),
        sa.Column('last_valuation_date', sa.Date, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )


def downgrade():
    op.drop_table('private_credit_positions')

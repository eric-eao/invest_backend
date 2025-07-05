"""add fields to private_credit_assets for tracking

Revision ID: 771d17d6965d
Revises: 2ab8511a7185
Create Date: 2025-07-05 12:27:56.000149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '771d17d6965d'
down_revision: Union[str, Sequence[str], None] = '2ab8511a7185'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('private_credit_assets', sa.Column('average_unit_price', sa.DECIMAL(20, 6)))
    op.add_column('private_credit_assets', sa.Column('total_quantity', sa.DECIMAL(20, 6)))
    op.add_column('private_credit_assets', sa.Column('total_cost', sa.DECIMAL(20, 6)))
    op.add_column('private_credit_assets', sa.Column('current_unit_price', sa.DECIMAL(20, 6)))
    op.add_column('private_credit_assets', sa.Column('last_valuation_date', sa.Date))
    op.add_column('private_credit_assets', sa.Column('profitability_percent', sa.DECIMAL(10, 4)))
    op.add_column('private_credit_assets', sa.Column('profitability_amount', sa.DECIMAL(20, 6)))


def downgrade():
    op.drop_column('private_credit_assets', 'average_unit_price')
    op.drop_column('private_credit_assets', 'total_quantity')
    op.drop_column('private_credit_assets', 'total_cost')
    op.drop_column('private_credit_assets', 'current_unit_price')
    op.drop_column('private_credit_assets', 'last_valuation_date')
    op.drop_column('private_credit_assets', 'profitability_percent')
    op.drop_column('private_credit_assets', 'profitability_amount')

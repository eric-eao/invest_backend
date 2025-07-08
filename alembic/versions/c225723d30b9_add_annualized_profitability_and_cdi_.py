"""add annualized profitability and cdi_ref to private_credit_assets

Revision ID: c225723d30b9
Revises: 38e8d5ec733c
Create Date: 2025-07-07 21:02:01.846876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c225723d30b9'
down_revision: Union[str, Sequence[str], None] = '38e8d5ec733c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('private_credit_assets', sa.Column('profitability_percent_annualized', sa.Numeric(20, 6), nullable=True))
    op.add_column('private_credit_assets', sa.Column('cdi_ref', sa.Numeric(20, 6), nullable=True))


def downgrade():
    op.drop_column('private_credit_assets', 'cdi_ref')
    op.drop_column('private_credit_assets', 'profitability_percent_annualized')
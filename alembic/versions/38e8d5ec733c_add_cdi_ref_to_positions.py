"""add cdi_ref to positions

Revision ID: 38e8d5ec733c
Revises: 6e8f180339b0
Create Date: 2025-07-07 20:44:29.610836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38e8d5ec733c'
down_revision: Union[str, Sequence[str], None] = '6e8f180339b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("positions", sa.Column("cdi_ref", sa.Numeric(20, 6), nullable=True))


def downgrade():
    op.drop_column("positions", "cdi_ref")

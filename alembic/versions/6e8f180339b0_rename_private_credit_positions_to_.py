"""rename private_credit_positions to positions

Revision ID: 6e8f180339b0
Revises: 4bd37468fc22
Create Date: 2025-07-06 21:08:38.491960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e8f180339b0'
down_revision: Union[str, Sequence[str], None] = '4bd37468fc22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.rename_table('private_credit_positions', 'positions')


def downgrade():
    op.rename_table('positions', 'private_credit_positions')

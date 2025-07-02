"""rename categories to private_credit_categories

Revision ID: 7159431ae56f
Revises: 80e47424908f
Create Date: 2025-07-01 20:24:14.752412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7159431ae56f'
down_revision: Union[str, Sequence[str], None] = '80e47424908f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.rename_table('categories', 'private_credit_categories')


def downgrade():
    op.rename_table('private_credit_categories', 'categories')

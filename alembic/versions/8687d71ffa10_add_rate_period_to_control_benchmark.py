"""add rate_period to control_benchmark

Revision ID: 8687d71ffa10
Revises: 7bf9db417aa6
Create Date: 2025-07-06 12:27:05.584001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8687d71ffa10'
down_revision: Union[str, Sequence[str], None] = '7bf9db417aa6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'control_benchmarks',
        sa.Column(
            'rate_period',
            sa.String(length=20),
            nullable=False,
            server_default='daily'  # define um default se quiser evitar nulls
        )
    )


def downgrade():
    op.drop_column('control_benchmarks', 'rate_period')

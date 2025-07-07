"""add summary_calc_status to snapshot_benchmark

Revision ID: 55bcff81ebc7
Revises: 8687d71ffa10
Create Date: 2025-07-06 12:52:27.763693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55bcff81ebc7'
down_revision: Union[str, Sequence[str], None] = '8687d71ffa10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "snapshot_benchmarks",
        sa.Column("summary_calc_status", sa.String(length=20), nullable=False, server_default="PENDING")
    )


def downgrade():
    op.drop_column("snapshot_benchmarks", "summary_calc_status")

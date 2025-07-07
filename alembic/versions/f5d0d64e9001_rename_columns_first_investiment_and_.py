"""rename columns first_investiment and last_investiment

Revision ID: f5d0d64e9001
Revises: 624e07476f97
Create Date: 2025-07-05 21:07:22.793573

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5d0d64e9001'
down_revision: Union[str, Sequence[str], None] = '624e07476f97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "control_portfolio_dates",
        "first_investiment",
        new_column_name="first_investment"
    )
    op.alter_column(
        "control_portfolio_dates",
        "last_investiment",
        new_column_name="last_investment"
    )


def downgrade() -> None:
    op.alter_column(
        "control_portfolio_dates",
        "first_investment",
        new_column_name="first_investiment"
    )
    op.alter_column(
        "control_portfolio_dates",
        "last_investment",
        new_column_name="last_investiment"
    )

"""create control_portfolio_dates table

Revision ID: c96a6de3822f
Revises: 2544b0164b49
Create Date: 2025-07-01 21:09:24.657067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c96a6de3822f'
down_revision: Union[str, Sequence[str], None] = '2544b0164b49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'control_portfolio_dates',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('module_id', sa.UUID(as_uuid=True), sa.ForeignKey('control_modules.id'), nullable=False),
        sa.Column('first_investiment', sa.Date(), nullable=True),
        sa.Column('last_investiment', sa.Date(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('control_portfolio_dates')

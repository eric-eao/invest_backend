"""create private_credit_assets table

Revision ID: 5651f72b2c30
Revises: c96a6de3822f
Create Date: 2025-07-01 21:50:25.357879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5651f72b2c30'
down_revision: Union[str, Sequence[str], None] = 'c96a6de3822f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'private_credit_assets',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False, unique=True),
        sa.Column('institution', sa.String(100), nullable=False),
        sa.Column('category_id', sa.UUID(as_uuid=True), sa.ForeignKey('private_credit_categories.id'), nullable=False),
        sa.Column('maturity_date', sa.Date(), nullable=True),
        sa.Column('rate_type', sa.String(20), nullable=False),
        sa.Column('indexer', sa.String(20), nullable=True),
        sa.Column('fixed_rate', sa.Float(), nullable=True),
        sa.Column('spread', sa.Float(), nullable=True),
        sa.Column('index_percent', sa.Float(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    )


def downgrade():
    op.drop_table('private_credit_assets')

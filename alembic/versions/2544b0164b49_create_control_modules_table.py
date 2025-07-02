"""create control_modules table

Revision ID: 2544b0164b49
Revises: 7159431ae56f
Create Date: 2025-07-01 20:49:55.254605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2544b0164b49'
down_revision: Union[str, Sequence[str], None] = '7159431ae56f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'control_modules',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column('sync_status', sa.String(20), nullable=False, server_default=sa.text("'pending'")),
        sa.Column('last_sync_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    )

def downgrade():
    op.drop_table('control_modules')

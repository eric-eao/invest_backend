"""create movements table

Revision ID: 2ab8511a7185
Revises: 5651f72b2c30
Create Date: 2025-07-05 11:50:27.452022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = '2ab8511a7185'
down_revision: Union[str, Sequence[str], None] = '5651f72b2c30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'movements',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('asset_id', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('module_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('control_modules.id'), nullable=False),
        sa.Column('movement_type', sa.Enum('APORTE', 'RESGATE_TOTAL', 'RESGATE_PARCIAL', name='movement_type_enum'), nullable=False),
        sa.Column('quantity', sa.DECIMAL(20, 6), nullable=False),
        sa.Column('unit_price', sa.DECIMAL(20, 6), nullable=False),
        sa.Column('amount', sa.DECIMAL(20, 6), nullable=False),
        sa.Column('movement_date', sa.Date, nullable=False),
        sa.Column('settlement_date', sa.Date, nullable=True),
        sa.Column('broker', sa.String(255), nullable=True),
        sa.Column('transaction_reference', sa.String(255), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'CONFIRMED', 'CANCELLED', name='movement_status_enum'), nullable=False, server_default='PENDING'),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('source', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('movements')
    op.execute('DROP TYPE movement_type_enum')
    op.execute('DROP TYPE movement_status_enum')

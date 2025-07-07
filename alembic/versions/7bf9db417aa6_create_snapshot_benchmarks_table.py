"""create snapshot_benchmarks table

Revision ID: 7bf9db417aa6
Revises: f5d0d64e9001
Create Date: 2025-07-05 21:20:58.614282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7bf9db417aa6'
down_revision: Union[str, Sequence[str], None] = 'f5d0d64e9001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Corrige a mudança de tipo para ENUM explicitamente
    op.execute("""
        ALTER TABLE private_credit_categories
        ALTER COLUMN currency
        TYPE currency_enum
        USING currency::currency_enum
    """)

    # Cria a tabela de snapshots
    op.create_table(
        'snapshot_benchmarks',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('benchmark_id', sa.UUID(as_uuid=True), sa.ForeignKey('control_benchmarks.id'), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('rate_daily', sa.Numeric(20, 6), nullable=True),
        sa.Column('rate_monthly', sa.Numeric(20, 6), nullable=True),
        sa.Column('rate_semester', sa.Numeric(20, 6), nullable=True),
        sa.Column('rate_yearly', sa.Numeric(20, 6), nullable=True),
        sa.Column('rate_ytd', sa.Numeric(20, 6), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('snapshot_benchmarks')

    op.execute("""
        ALTER TABLE private_credit_categories
        ALTER COLUMN currency
        TYPE VARCHAR(3)
    """)

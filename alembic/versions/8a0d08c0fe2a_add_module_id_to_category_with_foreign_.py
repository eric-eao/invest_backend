"""add module_id to category with foreign key

Revision ID: 8a0d08c0fe2a
Revises: c288c3ec2137
Create Date: 2025-07-05 16:49:08.854436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a0d08c0fe2a'
down_revision: Union[str, Sequence[str], None] = 'c288c3ec2137'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # adiciona a coluna
    op.add_column(
        'private_credit_categories',
        sa.Column('module_id', sa.UUID(as_uuid=True), nullable=True)
    )
    # cria a FK
    op.create_foreign_key(
        'fk_category_module_id',
        'private_credit_categories',
        'control_modules',
        ['module_id'],
        ['id'],
        ondelete='RESTRICT'
    )
    # depois ajusta a coluna para NOT NULL se quiser
    # mas primeiro convém preencher dados existentes
    # com UPDATE no banco se já houver linhas
    # e depois alterar para nullable=False

    # drop da coluna antiga
    op.drop_column('private_credit_categories', 'module')


def downgrade():
    op.add_column(
        'private_credit_categories',
        sa.Column('module', sa.String(length=50), nullable=False)
    )
    op.drop_constraint('fk_category_module_id', 'private_credit_categories', type_='foreignkey')
    op.drop_column('private_credit_categories', 'module_id')

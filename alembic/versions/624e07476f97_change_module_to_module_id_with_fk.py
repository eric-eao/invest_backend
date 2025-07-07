"""change module to module_id with FK

Revision ID: 624e07476f97
Revises: 8a0d08c0fe2a
Create Date: 2025-07-05 16:54:04.639153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '624e07476f97'
down_revision: Union[str, Sequence[str], None] = '8a0d08c0fe2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # adiciona nova coluna module_id (nullable temporariamente)
    op.add_column(
        "private_credit_categories",
        sa.Column("module_id", sa.UUID(as_uuid=True), nullable=True)
    )

    # se quiser migrar dados antigos manualmente:
    # op.execute("UPDATE private_credit_categories SET module_id = 'meu-uuid-fixo' WHERE module = 'private_credit'")
    # ou simplesmente deixe nulo e ajuste depois manualmente

    # cria FK
    op.create_foreign_key(
        "fk_category_module_id",
        "private_credit_categories",
        "control_modules",
        ["module_id"],
        ["id"],
        ondelete="RESTRICT"
    )

    # remove a antiga coluna module
    op.drop_column("private_credit_categories", "module")


def downgrade() -> None:
    # recria a coluna antiga
    op.add_column(
        "private_credit_categories",
        sa.Column("module", sa.String(length=50), nullable=False)
    )
    op.drop_constraint("fk_category_module_id", "private_credit_categories", type_="foreignkey")
    op.drop_column("private_credit_categories", "module_id")

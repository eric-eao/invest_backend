"""change movement_type_enum to english

Revision ID: c288c3ec2137
Revises: 771d17d6965d
Create Date: 2025-07-05 16:37:08.466442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c288c3ec2137'
down_revision: Union[str, Sequence[str], None] = '771d17d6965d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # renomeia o enum antigo
    op.execute("ALTER TYPE movement_type_enum RENAME TO movement_type_enum_old")
    # cria o novo enum em inglês
    op.execute("""
        CREATE TYPE movement_type_enum AS ENUM ('DEPOSIT', 'FULL_REDEMPTION', 'PARTIAL_REDEMPTION')
    """)
    # aplica na tabela
    op.execute("""
        ALTER TABLE movements
        ALTER COLUMN movement_type
        TYPE movement_type_enum
        USING movement_type::text::movement_type_enum
    """)
    # dropa o tipo antigo
    op.execute("DROP TYPE movement_type_enum_old")


def downgrade() -> None:
    # cria novamente o tipo antigo
    op.execute("""
        CREATE TYPE movement_type_enum_old AS ENUM ('DEPOSIT', 'RESGATE_TOTAL', 'RESGATE_PARCIAL')
    """)
    # aplica na tabela
    op.execute("""
        ALTER TABLE movements
        ALTER COLUMN movement_type
        TYPE movement_type_enum_old
        USING movement_type::text::movement_type_enum_old
    """)
    # remove o tipo em inglês
    op.execute("DROP TYPE movement_type_enum")
    # renomeia de volta
    op.execute("ALTER TYPE movement_type_enum_old RENAME TO movement_type_enum")

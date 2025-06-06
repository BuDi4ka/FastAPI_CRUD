"""add roles to users

Revision ID: 7ba3bd7703bb
Revises: afca8b522411
Create Date: 2025-06-06 18:04:17.230918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7ba3bd7703bb'
down_revision: Union[str, None] = 'afca8b522411'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.VARCHAR(), server_default='user', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###

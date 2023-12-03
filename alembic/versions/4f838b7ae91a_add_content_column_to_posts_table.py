"""add content column to posts table

Revision ID: 4f838b7ae91a
Revises: a22d65c24ad5
Create Date: 2023-12-02 19:40:01.721163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f838b7ae91a'
down_revision: Union[str, None] = 'a22d65c24ad5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')

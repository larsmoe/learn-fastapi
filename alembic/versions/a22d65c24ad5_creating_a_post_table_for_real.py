"""creating a post table for real

Revision ID: a22d65c24ad5
Revises: c967ca4e01bd
Create Date: 2023-12-02 19:36:59.899520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a22d65c24ad5'
down_revision: Union[str, None] = 'c967ca4e01bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')

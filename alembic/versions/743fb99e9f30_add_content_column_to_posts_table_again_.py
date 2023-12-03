"""add content column to posts table again for real

Revision ID: 743fb99e9f30
Revises: 4f838b7ae91a
Create Date: 2023-12-02 19:46:22.791381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '743fb99e9f30'
down_revision: Union[str, None] = '4f838b7ae91a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    print('test')


def downgrade() -> None:
    print('test')

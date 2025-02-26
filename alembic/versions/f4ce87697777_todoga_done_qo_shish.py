"""Todoga done qo'shish

Revision ID: f4ce87697777
Revises: 
Create Date: 2025-02-06 10:16:59.104571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4ce87697777'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("todo", sa.Column("done", sa.Boolean(), default=False)) #Done degan ustun qo'shdim todo jadvaliga
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("todo", "done") # todo jadvalidan done degan ustunni olib tashladim
    # ### end Alembic commands ###
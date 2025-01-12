"""First migration

Revision ID: 14275c65da8b
Revises: 
Create Date: 2025-01-13 01:50:08.099563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '14275c65da8b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('deposits')


def downgrade() -> None:
    op.create_table('deposits',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('date', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('periods', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('amount', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rate', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='deposits_pkey')
    )

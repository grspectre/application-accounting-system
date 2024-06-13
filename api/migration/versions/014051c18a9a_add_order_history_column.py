"""add order_history column

Revision ID: 014051c18a9a
Revises: 748dbf1a7ee2
Create Date: 2024-06-12 22:00:49.555390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '014051c18a9a'
down_revision: Union[str, None] = '748dbf1a7ee2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('order_history', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'order_history')
    # ### end Alembic commands ###
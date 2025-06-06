"""Initial revision

Revision ID: 43ab56b50737
Revises: a572f819a6a4
Create Date: 2024-10-11 18:23:08.487502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '43ab56b50737'
down_revision: Union[str, None] = 'a572f819a6a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('start_date', sa.DateTime(), nullable=False))
    op.add_column('events', sa.Column('end_date', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'events', 'locations', ['location_id'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.drop_column('events', 'date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'end_date')
    op.drop_column('events', 'start_date')
    # ### end Alembic commands ###

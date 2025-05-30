"""Initial revision

Revision ID: af0666b5fa25
Revises: 5ff54022611d
Create Date: 2024-10-04 17:28:08.256027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af0666b5fa25'
down_revision: Union[str, None] = '5ff54022611d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('date_of_birth', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'date_of_birth')
    # ### end Alembic commands ###

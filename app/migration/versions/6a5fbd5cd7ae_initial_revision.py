"""Initial revision

Revision ID: 6a5fbd5cd7ae
Revises: ff2ce9d41ab4
Create Date: 2024-10-07 14:57:53.184408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a5fbd5cd7ae'
down_revision: Union[str, None] = 'ff2ce9d41ab4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

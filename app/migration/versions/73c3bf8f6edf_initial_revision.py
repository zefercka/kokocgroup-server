"""Initial revision

Revision ID: 73c3bf8f6edf
Revises: 8af0bd3554ba
Create Date: 2024-10-13 20:38:51.097378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73c3bf8f6edf'
down_revision: Union[str, None] = '8af0bd3554ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('stream_url', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'stream_url')
    # ### end Alembic commands ###

"""Initial revision

Revision ID: 7713e040b8da
Revises: a8786dac2d2b
Create Date: 2024-10-08 12:36:48.231586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7713e040b8da'
down_revision: Union[str, None] = 'a8786dac2d2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news_categories',
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_foreign_key(None, 'news', 'news_categories', ['category_name'], ['name'])
    op.drop_constraint('news_actions_news_id_fkey', 'news_actions', type_='foreignkey')
    op.create_foreign_key(None, 'news_actions', 'news', ['news_id'], ['id'], onupdate='CASCADE', ondelete='NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'news_actions', type_='foreignkey')
    op.create_foreign_key('news_actions_news_id_fkey', 'news_actions', 'news', ['news_id'], ['id'])
    op.drop_constraint(None, 'news', type_='foreignkey')
    op.drop_table('news_categories')
    # ### end Alembic commands ###

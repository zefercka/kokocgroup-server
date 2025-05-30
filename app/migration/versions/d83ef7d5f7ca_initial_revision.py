"""Initial revision

Revision ID: d83ef7d5f7ca
Revises: 1bf23833b460
Create Date: 2024-10-08 21:11:36.358652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd83ef7d5f7ca'
down_revision: Union[str, None] = '1bf23833b460'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image_uploads',
    sa.Column('file_name', sa.String(length=32), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='NO ACTIONS'),
    sa.PrimaryKeyConstraint('file_name')
    )
    op.create_foreign_key(None, 'roles_permissions', 'permissions', ['permission'], ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'roles_permissions', type_='foreignkey')
    op.drop_table('image_uploads')
    # ### end Alembic commands ###

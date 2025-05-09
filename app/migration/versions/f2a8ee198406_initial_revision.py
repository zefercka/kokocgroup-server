"""Initial revision

Revision ID: f2a8ee198406
Revises: a54a50604ea6
Create Date: 2024-10-10 17:50:49.720963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f2a8ee198406'
down_revision: Union[str, None] = 'a54a50604ea6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('base_settings',
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('value', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('news_categories',
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('file_uploads',
    sa.Column('file_name', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('file_name')
    )
    op.create_table('team_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('position', sa.String(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_roles',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    op.drop_table('user_roles')
    op.add_column('news', sa.Column('category_name', sa.String(length=32), nullable=False))
    op.add_column('news', sa.Column('status', sa.String(), nullable=False))
    op.alter_column('news', 'title',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=256),
               existing_nullable=False)
    op.create_index('ix_title_content', 'news', [sa.text("(coalesce(title, '') || coalesce(content, ''))")], unique=False, postgresql_using='gin', postgresql_ops={'news_search': 'gin_trgm_ops'})
    op.create_foreign_key(None, 'news', 'news_categories', ['category_name'], ['name'], onupdate='CASCADE', ondelete='SET NULL')
    op.drop_column('news', 'category')
    op.drop_constraint('news_actions_user_id_fkey', 'news_actions', type_='foreignkey')
    op.drop_constraint('news_actions_news_id_fkey', 'news_actions', type_='foreignkey')
    op.create_foreign_key(None, 'news_actions', 'users', ['user_id'], ['id'], onupdate='CASCADE', ondelete='SET NULL')
    op.create_foreign_key(None, 'news_actions', 'news', ['news_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('roles', 'created_at')
    op.drop_column('roles', 'updated_at')
    op.drop_constraint('roles_permissions_permission_fkey', 'roles_permissions', type_='foreignkey')
    op.drop_constraint('roles_permissions_role_id_fkey', 'roles_permissions', type_='foreignkey')
    op.create_foreign_key(None, 'roles_permissions', 'permissions', ['permission'], ['name'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'roles_permissions', 'roles', ['role_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'roles_permissions', type_='foreignkey')
    op.drop_constraint(None, 'roles_permissions', type_='foreignkey')
    op.create_foreign_key('roles_permissions_role_id_fkey', 'roles_permissions', 'roles', ['role_id'], ['id'])
    op.create_foreign_key('roles_permissions_permission_fkey', 'roles_permissions', 'permissions', ['permission'], ['name'])
    op.add_column('roles', sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.add_column('roles', sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'news_actions', type_='foreignkey')
    op.drop_constraint(None, 'news_actions', type_='foreignkey')
    op.create_foreign_key('news_actions_news_id_fkey', 'news_actions', 'news', ['news_id'], ['id'])
    op.create_foreign_key('news_actions_user_id_fkey', 'news_actions', 'users', ['user_id'], ['id'])
    op.add_column('news', sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'news', type_='foreignkey')
    op.drop_index('ix_title_content', table_name='news', postgresql_using='gin', postgresql_ops={'news_search': 'gin_trgm_ops'})
    op.alter_column('news', 'title',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=128),
               existing_nullable=False)
    op.drop_column('news', 'status')
    op.drop_column('news', 'category_name')
    op.create_table('user_roles',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='user_roles_role_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_roles_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'role_id', name='user_roles_pkey')
    )
    op.drop_table('users_roles')
    op.drop_table('team_members')
    op.drop_table('file_uploads')
    op.drop_table('news_categories')
    op.drop_table('base_settings')
    # ### end Alembic commands ###

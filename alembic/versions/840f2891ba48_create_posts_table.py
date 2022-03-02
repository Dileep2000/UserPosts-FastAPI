"""Create Posts table

Revision ID: 840f2891ba48
Revises: e4e1b1716ab3
Create Date: 2022-03-02 10:06:15.965011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '840f2891ba48'
down_revision = 'e4e1b1716ab3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer,nullable=False,primary_key=True),sa.Column('title',sa.String,nullable=False), sa.Column('content',sa.String,nullable=False), sa.Column('published',sa.Boolean,server_default='True',nullable=False), sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')), sa.Column('user_id',sa.Integer,nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users', local_cols=['user_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_table('posts')
    pass

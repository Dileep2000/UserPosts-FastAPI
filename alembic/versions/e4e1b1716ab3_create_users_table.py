"""Create Users Table

Revision ID: e4e1b1716ab3
Revises: 
Create Date: 2022-03-02 09:56:52.486661

"""
from telnetlib import Telnet
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4e1b1716ab3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',sa.Column('id',sa.Integer, nullable=False, primary_key=True),sa.Column('email',sa.String,nullable=False,unique=True),sa.Column('password',sa.String,nullable=False),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_table('users')
    pass

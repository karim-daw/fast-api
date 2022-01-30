"""create posts table

Revision ID: 033269c59fba
Revises: 
Create Date: 2022-01-30 17:57:42.831407

"""
from pickle import TRUE
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '033269c59fba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_table('posts')
    pass

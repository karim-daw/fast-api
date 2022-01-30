"""add content column to post table

Revision ID: da7be89b536d
Revises: 033269c59fba
Create Date: 2022-01-30 18:08:03.514569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da7be89b536d'
down_revision = '033269c59fba'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

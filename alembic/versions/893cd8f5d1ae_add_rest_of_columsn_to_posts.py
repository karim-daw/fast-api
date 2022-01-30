"""add rest of columsn to posts

Revision ID: 893cd8f5d1ae
Revises: 1fcfd9e8e218
Create Date: 2022-01-30 18:29:22.516926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '893cd8f5d1ae'
down_revision = '1fcfd9e8e218'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"),
    op.add_column(
        'posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("Now()")))
        )
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass

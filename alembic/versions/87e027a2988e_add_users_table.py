"""add users table

Revision ID: 87e027a2988e
Revises: da7be89b536d
Create Date: 2022-01-30 18:12:18.527233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87e027a2988e'
down_revision = 'da7be89b536d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('password', sa.String(), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email') # insure you cant have duplicate emails
    )
    pass


def downgrade():
    op.drop_table('users')
    pass

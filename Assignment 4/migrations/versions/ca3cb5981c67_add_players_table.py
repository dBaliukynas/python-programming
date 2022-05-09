"""Add players table

Revision ID: ca3cb5981c67
Revises: 
Create Date: 2022-05-09 21:47:59.418869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca3cb5981c67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('surname', sa.String(length=64), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('nationality', sa.String(length=64), nullable=False),
    sa.Column('position', sa.String(length=64), nullable=False),
    sa.Column('points', sa.Float(), nullable=False),
    sa.Column('rebounds', sa.Float(), nullable=False),
    sa.Column('assists', sa.Float(), nullable=False),
    sa.Column('steals', sa.Float(), nullable=False),
    sa.Column('blocks', sa.Float(), nullable=False),
    sa.Column('performance_index_rating', sa.Float(), nullable=False),
    sa.Column('image_source', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('players')
    # ### end Alembic commands ###
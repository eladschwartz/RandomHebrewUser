"""initial

Revision ID: 8bcdc600897f
Revises: 
Create Date: 2025-01-08 12:51:57.352408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bcdc600897f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dob',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('street_name', sa.String(length=100), nullable=True),
    sa.Column('street_number', sa.Integer(), nullable=True),
    sa.Column('postal_code', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.String(length=100), nullable=True),
    sa.Column('longitude', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=10), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('gender', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('seeds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('seed', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('phone_id', sa.Integer(), nullable=False),
    sa.Column('dob_id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dob_id'], ['dob.id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.ForeignKeyConstraint(['phone_id'], ['phones.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('seed')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('seeds')
    op.drop_table('users')
    op.drop_table('phones')
    op.drop_table('locations')
    op.drop_table('dob')
    # ### end Alembic commands ###

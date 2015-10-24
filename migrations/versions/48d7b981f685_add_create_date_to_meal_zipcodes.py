"""add create_date to meal_zipcodes

Revision ID: 48d7b981f685
Revises: 54a5edc457d2
Create Date: 2015-10-24 14:54:45.658000

"""

# revision identifiers, used by Alembic.
revision = '48d7b981f685'
down_revision = '54a5edc457d2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meal_zipcode', sa.Column('create_date', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meal_zipcode', 'create_date')
    ### end Alembic commands ###

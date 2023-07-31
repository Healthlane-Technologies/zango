"""
added_address

Revision ID: 89b08b35fcbd
Revises: 9b2c1eb188f3
Create Date: 2023-07-28 10:16:22.486279
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89b08b35fcbd'
down_revision = '9b2c1eb188f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'Addresses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('address', sa.String(200), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('apps2.MyUsers.id'), nullable=False),
        schema='apps2'
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Addresses', schema='apps2')
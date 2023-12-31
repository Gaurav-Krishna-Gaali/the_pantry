"""empty message

Revision ID: 2747492a479e
Revises: d7631682dbe9
Create Date: 2023-08-15 17:06:49.859104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2747492a479e'
down_revision = 'd7631682dbe9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    # ### end Alembic commands ###

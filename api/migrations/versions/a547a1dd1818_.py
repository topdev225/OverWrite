"""empty message

Revision ID: a547a1dd1818
Revises: 2663146645e3
Create Date: 2019-11-18 14:34:42.462464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a547a1dd1818"
down_revision = "2663146645e3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("product_variants", sa.Column("bin", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("product_variants", "bin")
    # ### end Alembic commands ###

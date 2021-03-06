"""empty message

Revision ID: e15781f13e75
Revises: 412dd8dcf954
Create Date: 2019-01-14 16:25:18.775494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e15781f13e75"
down_revision = "412dd8dcf954"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("product_variants", "sku")
    op.add_column("products", sa.Column("item_number", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("products", "item_number")
    op.add_column(
        "product_variants", sa.Column("sku", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###

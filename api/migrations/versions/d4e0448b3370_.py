"""empty message

Revision ID: d4e0448b3370
Revises: 79b160988817
Create Date: 2019-03-29 12:29:24.804408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d4e0448b3370"
down_revision = "79b160988817"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("product_variants", sa.Column("custom_vendor_cost", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("product_variants", "custom_vendor_cost")
    # ### end Alembic commands ###

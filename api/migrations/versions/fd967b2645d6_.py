"""empty message

Revision ID: fd967b2645d6
Revises: ee6f54349227
Create Date: 2020-01-28 13:05:38.123246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fd967b2645d6"
down_revision = "ee6f54349227"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("product_variants", sa.Column("decorator_id", sa.Integer(), nullable=True))
    op.add_column("product_variants", sa.Column("vendor_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "product_variants", "vendors", ["decorator_id"], ["id"])
    op.create_foreign_key(None, "product_variants", "vendors", ["vendor_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "product_variants", type_="foreignkey")
    op.drop_constraint(None, "product_variants", type_="foreignkey")
    op.drop_column("product_variants", "vendor_id")
    op.drop_column("product_variants", "decorator_id")
    # ### end Alembic commands ###
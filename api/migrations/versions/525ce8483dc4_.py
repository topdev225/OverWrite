"""empty message

Revision ID: 525ce8483dc4
Revises: 2b0fac1c8703
Create Date: 2018-12-27 10:20:16.759492

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "525ce8483dc4"
down_revision = "2b0fac1c8703"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("product_variants", sa.Column("bag_fold_label_cost", sa.Float(), nullable=True))
    op.add_column("product_variants", sa.Column("margin", sa.Float(), nullable=True))
    op.add_column("product_variants", sa.Column("margin_oversize", sa.Float(), nullable=True))
    op.add_column(
        "product_variants", sa.Column("vendor_cost_oversize_cost", sa.Float(), nullable=True)
    )
    op.drop_column("product_variants", "vendor_cost_oversize_price")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "product_variants",
        sa.Column(
            "vendor_cost_oversize_price",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("product_variants", "vendor_cost_oversize_cost")
    op.drop_column("product_variants", "margin_oversize")
    op.drop_column("product_variants", "margin")
    op.drop_column("product_variants", "bag_fold_label_cost")
    # ### end Alembic commands ###

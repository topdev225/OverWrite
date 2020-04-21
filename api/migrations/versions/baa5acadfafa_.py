"""empty message

Revision ID: baa5acadfafa
Revises: 2e8a4ad50a1d
Create Date: 2020-01-10 15:05:45.870722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "baa5acadfafa"
down_revision = "2e8a4ad50a1d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("related_product_types", sa.Column("distributor_id", sa.Integer(), nullable=True))
    op.add_column("related_product_types", sa.Column("vendor_id", sa.Integer(), nullable=True))
    op.drop_constraint(
        "related_product_types_account_id_fkey", "related_product_types", type_="foreignkey"
    )
    op.create_foreign_key(None, "related_product_types", "vendors", ["vendor_id"], ["id"])
    op.create_foreign_key(None, "related_product_types", "distributors", ["distributor_id"], ["id"])
    op.drop_column("related_product_types", "account_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "related_product_types",
        sa.Column("account_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "related_product_types", type_="foreignkey")
    op.drop_constraint(None, "related_product_types", type_="foreignkey")
    op.create_foreign_key(
        "related_product_types_account_id_fkey",
        "related_product_types",
        "accounts",
        ["account_id"],
        ["id"],
    )
    op.drop_column("related_product_types", "vendor_id")
    op.drop_column("related_product_types", "distributor_id")
    # ### end Alembic commands ###
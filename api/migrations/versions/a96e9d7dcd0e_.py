"""Fix relationships between products, attributes, and values

Revision ID: a96e9d7dcd0e
Revises: 572e0dd8600e
Create Date: 2020-02-21 22:49:47.377491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a96e9d7dcd0e"
down_revision = "572e0dd8600e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "product_type_attributes",
        sa.Column("product_type_id", sa.Integer(), nullable=True),
        sa.Column("product_attribute_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["product_attribute_id"], ["product_attributes.id"],),
        sa.ForeignKeyConstraint(["product_type_id"], ["product_types.id"],),
    )
    op.drop_constraint(
        "product_attributes_product_type_id_fkey", "product_attributes", type_="foreignkey"
    )
    op.drop_column("product_attributes", "product_type_id")
    op.drop_constraint(
        "product_attributes_values_distributor_id_fkey",
        "product_attributes_values",
        type_="foreignkey",
    )
    op.drop_constraint(
        "product_attributes_values_account_id_fkey", "product_attributes_values", type_="foreignkey"
    )
    op.drop_column("product_attributes_values", "deleted")
    op.drop_column("product_attributes_values", "active")
    op.drop_column("product_attributes_values", "account_id")
    op.drop_column("product_attributes_values", "distributor_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "product_attributes_values",
        sa.Column("distributor_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_attributes_values",
        sa.Column("account_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_attributes_values",
        sa.Column("active", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_attributes_values",
        sa.Column("deleted", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "product_attributes_values_account_id_fkey",
        "product_attributes_values",
        "accounts",
        ["account_id"],
        ["id"],
    )
    op.create_foreign_key(
        "product_attributes_values_distributor_id_fkey",
        "product_attributes_values",
        "distributors",
        ["distributor_id"],
        ["id"],
    )
    op.add_column(
        "product_attributes",
        sa.Column("product_type_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "product_attributes_product_type_id_fkey",
        "product_attributes",
        "product_types",
        ["product_type_id"],
        ["id"],
    )
    op.drop_table("product_type_attributes")
    # ### end Alembic commands ###

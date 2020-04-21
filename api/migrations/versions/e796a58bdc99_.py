"""Drop RelatedProductTypes, replace with two join tables

Revision ID: e796a58bdc99
Revises: d8faec4baa2b
Create Date: 2020-02-19 14:53:27.049947

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e796a58bdc99"
down_revision = "d8faec4baa2b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "product_type_distributors",
        sa.Column("product_type_id", sa.Integer(), nullable=True),
        sa.Column("distributor_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["distributor_id"], ["distributors.id"],),
        sa.ForeignKeyConstraint(["product_type_id"], ["product_types.id"],),
    )
    op.create_table(
        "product_type_vendors",
        sa.Column("product_type_id", sa.Integer(), nullable=True),
        sa.Column("vendor_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["product_type_id"], ["product_types.id"],),
        sa.ForeignKeyConstraint(["vendor_id"], ["vendors.id"],),
    )
    op.drop_table("related_product_types")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "related_product_types",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("product_type_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("distributor_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("vendor_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "modified_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["distributor_id"],
            ["distributors.id"],
            name="related_product_types_distributor_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["product_type_id"],
            ["product_types.id"],
            name="related_product_types_product_type_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["vendor_id"], ["vendors.id"], name="related_product_types_vendor_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="related_product_types_pkey"),
    )
    op.drop_table("product_type_vendors")
    op.drop_table("product_type_distributors")
    # ### end Alembic commands ###
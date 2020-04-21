"""Link variants to values table, create CampaignProductVariant model

Revision ID: c78fe7219979
Revises: ac58ae797b72
Create Date: 2020-02-24 19:30:24.107415

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c78fe7219979"
down_revision = "ac58ae797b72"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "campaign_product_variants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bin_id", sa.Integer(), nullable=True),
        sa.Column("decorations", sa.JSON(), nullable=True),
        sa.Column("margin", sa.Float(), nullable=True),
        sa.Column("vendor_cost", sa.Float(), nullable=True),
        sa.Column("ow_cost", sa.Float(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("sku", sa.String(), nullable=True),
        sa.Column("attributes", sa.JSON(), nullable=True),
        sa.Column("supplier_name", sa.String(), nullable=True),
        sa.Column("supplier_email", sa.String(), nullable=True),
        sa.Column("supplier_address", sa.String(), nullable=True),
        sa.Column("decorator_name", sa.String(), nullable=True),
        sa.Column("decorator_email", sa.String(), nullable=True),
        sa.Column("decorator_address", sa.String(), nullable=True),
        sa.Column("product_name", sa.String(), nullable=True),
        sa.Column("product_type_name", sa.String(), nullable=True),
        sa.Column("product_variant_id", sa.Integer(), nullable=True),
        sa.Column("campaign_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaigns.id"],),
        sa.ForeignKeyConstraint(["product_variant_id"], ["product_variants.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product_variant_attribute_values",
        sa.Column("product_variant_id", sa.Integer(), nullable=True),
        sa.Column("product_attribute_value_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["product_attribute_value_id"], ["product_attributes_values.id"],),
        sa.ForeignKeyConstraint(["product_variant_id"], ["product_variants.id"],),
    )
    op.add_column("campaigns", sa.Column("created_by_id", sa.Integer(), nullable=True))
    op.add_column("campaigns", sa.Column("pick_pack_partner_id", sa.Integer(), nullable=True))
    op.add_column("campaigns", sa.Column("pick_pack_partner_message", sa.String(), nullable=True))
    op.drop_constraint("campaigns_vendor_partner_id_fkey", "campaigns", type_="foreignkey")
    op.drop_constraint("campaigns_created_by_fkey", "campaigns", type_="foreignkey")
    op.create_foreign_key(None, "campaigns", "vendors", ["pick_pack_partner_id"], ["id"])
    op.create_foreign_key(None, "campaigns", "accounts", ["created_by_id"], ["id"])
    op.drop_column("campaigns", "vendor_partner_message")
    op.drop_column("campaigns", "vendor_partner_id")
    op.drop_column("campaigns", "created_by")
    op.add_column(
        "order_items", sa.Column("campaign_product_variant_id", sa.Integer(), nullable=False)
    )
    op.drop_constraint("order_items_product_variant_id_fkey", "order_items", type_="foreignkey")
    op.create_foreign_key(
        None, "order_items", "campaign_product_variants", ["campaign_product_variant_id"], ["id"]
    )
    op.drop_column("order_items", "product_variant_id")
    op.add_column("product_variants", sa.Column("supplier_id", sa.Integer(), nullable=True))
    op.drop_constraint("product_variants_decorator_id_fkey", "product_variants", type_="foreignkey")
    op.drop_constraint("product_variants_vendor_id_fkey", "product_variants", type_="foreignkey")
    op.drop_constraint("product_variants_campaign_id_fkey", "product_variants", type_="foreignkey")
    op.create_foreign_key(None, "product_variants", "vendors", ["supplier_id"], ["id"])
    op.drop_column("product_variants", "vendor_id")
    op.drop_column("product_variants", "vendor_cost")
    op.drop_column("product_variants", "custom_vendor_cost")
    op.drop_column("product_variants", "campaign_id")
    op.drop_column("product_variants", "custom_margin")
    op.drop_column("product_variants", "attributes")
    op.drop_column("product_variants", "decorator_id")
    op.drop_column("product_variants", "bin")
    op.drop_column("product_variants", "vendor_name")
    op.drop_column("product_variants", "is_default")
    op.drop_column("product_variants", "decorations")
    op.drop_column("product_variants", "margin")
    op.drop_column("product_variants", "upcharged_attribute")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "product_variants",
        sa.Column("upcharged_attribute", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_variants",
        sa.Column(
            "margin", postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "product_variants",
        sa.Column(
            "decorations",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "product_variants",
        sa.Column("is_default", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_variants",
        sa.Column("vendor_name", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_variants", sa.Column("bin", sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "product_variants",
        sa.Column("decorator_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_variants",
        sa.Column(
            "attributes", postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "product_variants",
        sa.Column("custom_margin", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_variants",
        sa.Column("campaign_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_variants",
        sa.Column("custom_vendor_cost", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_variants",
        sa.Column(
            "vendor_cost",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "product_variants", sa.Column("vendor_id", sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.drop_constraint(None, "product_variants", type_="foreignkey")
    op.create_foreign_key(
        "product_variants_campaign_id_fkey",
        "product_variants",
        "campaigns",
        ["campaign_id"],
        ["id"],
    )
    op.create_foreign_key(
        "product_variants_vendor_id_fkey", "product_variants", "vendors", ["vendor_id"], ["id"]
    )
    op.create_foreign_key(
        "product_variants_decorator_id_fkey",
        "product_variants",
        "vendors",
        ["decorator_id"],
        ["id"],
    )
    op.drop_column("product_variants", "supplier_id")
    op.add_column(
        "order_items",
        sa.Column("product_variant_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "order_items", type_="foreignkey")
    op.create_foreign_key(
        "order_items_product_variant_id_fkey",
        "order_items",
        "product_variants",
        ["product_variant_id"],
        ["id"],
    )
    op.drop_column("order_items", "campaign_product_variant_id")
    op.add_column(
        "campaigns", sa.Column("created_by", sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "campaigns",
        sa.Column("vendor_partner_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "campaigns",
        sa.Column("vendor_partner_message", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "campaigns", type_="foreignkey")
    op.drop_constraint(None, "campaigns", type_="foreignkey")
    op.create_foreign_key(
        "campaigns_created_by_fkey", "campaigns", "accounts", ["created_by"], ["id"]
    )
    op.create_foreign_key(
        "campaigns_vendor_partner_id_fkey", "campaigns", "vendors", ["vendor_partner_id"], ["id"]
    )
    op.drop_column("campaigns", "pick_pack_partner_message")
    op.drop_column("campaigns", "pick_pack_partner_id")
    op.drop_column("campaigns", "created_by_id")
    op.drop_table("product_variant_attribute_values")
    op.drop_table("campaign_product_variants")
    # ### end Alembic commands ###
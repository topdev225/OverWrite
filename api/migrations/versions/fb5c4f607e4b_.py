"""Drop all created_at, updated_at, modified_at columns

Revision ID: fb5c4f607e4b
Revises: 23dce09534a3
Create Date: 2020-02-18 22:52:17.163904

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "fb5c4f607e4b"
down_revision = "23dce09534a3"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("campaigns", "created_at")
    op.drop_column("campaigns", "updated_at")
    op.drop_column("distributors", "created_at")
    op.drop_column("distributors", "modified_at")
    op.drop_column("order_events", "created_at")
    op.drop_column("order_notes", "created_at")
    op.drop_column("orders", "created_at")
    op.drop_column("product_attributes", "created_at")
    op.drop_column("product_attributes", "updated_at")
    op.drop_column("product_attributes_values", "created_at")
    op.drop_column("product_attributes_values", "updated_at")
    op.drop_column("product_types", "created_at")
    op.drop_column("product_types", "updated_at")
    op.drop_column("related_product_types", "created_at")
    op.drop_column("related_product_types", "updated_at")
    op.drop_column("rm_product_attributes_values", "created_at")
    op.drop_column("rm_product_attributes_values", "updated_at")


def downgrade():
    op.add_column(
        "rm_product_attributes_values",
        sa.Column("updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "rm_product_attributes_values",
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "related_product_types",
        sa.Column("updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "related_product_types",
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_types",
        sa.Column("updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_types",
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_attributes_values",
        sa.Column("updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_attributes_values",
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_attributes",
        sa.Column("updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "product_attributes",
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "orders",
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "order_notes",
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "order_events",
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "distributors",
        sa.Column(
            "modified_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("'2020-02-18 23:52:12.308217'::timestamp without time zone"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "distributors",
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("'2020-02-18 23:52:12.308217'::timestamp without time zone"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "campaigns",
        sa.Column("updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "campaigns",
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    )

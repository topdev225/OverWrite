"""empty message

Revision ID: c425675af96b
Revises: d2bda5070df2
Create Date: 2019-03-27 13:45:08.564219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c425675af96b"
down_revision = "d2bda5070df2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("product_variants", sa.Column("upcharged_attribute", sa.String(), nullable=True))
    op.drop_column("product_variants", "custom_margin")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "product_variants",
        sa.Column("custom_margin", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.drop_column("product_variants", "upcharged_attribute")
    # ### end Alembic commands ###

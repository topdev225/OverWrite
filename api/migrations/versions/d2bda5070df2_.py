"""empty message

Revision ID: d2bda5070df2
Revises: 47ee3533296a
Create Date: 2019-03-27 07:16:47.926486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d2bda5070df2"
down_revision = "47ee3533296a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("product_variants", sa.Column("custom_margin", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("product_variants", "custom_margin")
    # ### end Alembic commands ###

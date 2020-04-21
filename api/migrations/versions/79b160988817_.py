"""empty message

Revision ID: 79b160988817
Revises: c425675af96b
Create Date: 2019-03-27 14:02:48.399795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "79b160988817"
down_revision = "c425675af96b"
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
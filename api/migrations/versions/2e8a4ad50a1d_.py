"""empty message

Revision ID: 2e8a4ad50a1d
Revises: 77b04919a2c8
Create Date: 2020-01-10 09:33:13.087350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2e8a4ad50a1d"
down_revision = "77b04919a2c8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("product_attributes_values", sa.Column("active", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("product_attributes_values", "active")
    # ### end Alembic commands ###
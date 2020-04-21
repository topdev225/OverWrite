"""empty message

Revision ID: cbadbf7610bb
Revises: 97d657f8cad4
Create Date: 2019-02-04 16:30:06.292069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cbadbf7610bb"
down_revision = "97d657f8cad4"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("products", "item_number")
    op.add_column("products", sa.Column("item_number", sa.String(), nullable=True))


def downgrade():
    op.drop_column("products", "item_number")
    op.add_column("products", sa.Column("item_number", sa.Integer(), nullable=True))

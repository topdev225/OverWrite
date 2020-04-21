"""empty message

Revision ID: 8f9a35f1728e
Revises: e15781f13e75
Create Date: 2019-01-15 10:02:20.452461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8f9a35f1728e"
down_revision = "e15781f13e75"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("distributors", sa.Column("ow_cost", sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("distributors", "ow_cost")
    # ### end Alembic commands ###
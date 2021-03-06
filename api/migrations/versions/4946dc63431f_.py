"""empty message

Revision ID: 4946dc63431f
Revises: 2b2dfc850dc8
Create Date: 2019-11-25 16:17:09.369598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4946dc63431f"
down_revision = "2b2dfc850dc8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "campaigns", sa.Column("start_date_test", sa.DateTime(timezone=True), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("campaigns", "start_date_test")
    # ### end Alembic commands ###

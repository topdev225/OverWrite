"""empty message

Revision ID: 216f1c49cfe4
Revises: cbadbf7610bb
Create Date: 2019-02-05 13:49:56.704939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "216f1c49cfe4"
down_revision = "cbadbf7610bb"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("accounts", sa.Column("_password", sa.String(), nullable=True))
    op.drop_column("accounts", "password")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "accounts", sa.Column("password", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_column("accounts", "_password")
    # ### end Alembic commands ###

"""empty message

Revision ID: 669a066aa7cc
Revises: 7095bd817b5b
Create Date: 2018-12-17 13:01:37.870620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "669a066aa7cc"
down_revision = "7095bd817b5b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("departments_name_key", "departments", type_="unique")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("departments_name_key", "departments", ["name"])
    # ### end Alembic commands ###

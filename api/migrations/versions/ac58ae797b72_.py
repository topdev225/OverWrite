"""Drop JSON columns on Campaign for managers and departments

Revision ID: ac58ae797b72
Revises: 2993c317aeba
Create Date: 2020-02-23 20:28:36.369879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ac58ae797b72"
down_revision = "2993c317aeba"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("departments")
    op.add_column("campaigns", sa.Column("departments", sa.JSON(), nullable=True))
    op.add_column("campaigns", sa.Column("managers", sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("campaigns", "managers")
    op.drop_column("campaigns", "departments")
    op.create_table(
        "departments",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("campaign_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["campaign_id"], ["campaigns.id"], name="departments_campaign_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="departments_pkey"),
    )
    # ### end Alembic commands ###

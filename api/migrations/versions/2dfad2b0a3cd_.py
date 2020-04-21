"""empty message

Revision ID: 2dfad2b0a3cd
Revises: 36c58f2eab13
Create Date: 2019-08-19 14:44:09.056767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2dfad2b0a3cd"
down_revision = "36c58f2eab13"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "accounts_campaigns",
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("campaign_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"],),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaigns.id"],),
        sa.PrimaryKeyConstraint("account_id", "campaign_id"),
    )
    op.drop_constraint("accounts_campaign_id_fkey", "accounts", type_="foreignkey")
    op.drop_column("accounts", "campaign_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "accounts", sa.Column("campaign_id", sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.create_foreign_key(
        "accounts_campaign_id_fkey", "accounts", "campaigns", ["campaign_id"], ["id"]
    )
    op.drop_table("accounts_campaigns")
    # ### end Alembic commands ###

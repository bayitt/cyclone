"""Updated cascade relationships on foreign keys

Revision ID: feef1b627a1c
Revises: aeea7f3fc161
Create Date: 2023-05-14 22:30:28.079986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "feef1b627a1c"
down_revision = "aeea7f3fc161"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "credentials_application_uuid_fkey", "credentials", type_="foreignkey"
    )
    op.create_foreign_key(
        None,
        "credentials",
        "applications",
        ["application_uuid"],
        ["uuid"],
        ondelete="CASCADE",
    )
    op.drop_constraint("emails_application_uuid_fkey", "emails", type_="foreignkey")
    op.create_foreign_key(
        None,
        "emails",
        "applications",
        ["application_uuid"],
        ["uuid"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "emails", type_="foreignkey")
    op.create_foreign_key(
        "emails_application_uuid_fkey",
        "emails",
        "applications",
        ["application_uuid"],
        ["uuid"],
    )
    op.drop_constraint(None, "credentials", type_="foreignkey")
    op.create_foreign_key(
        "credentials_application_uuid_fkey",
        "credentials",
        "applications",
        ["application_uuid"],
        ["uuid"],
    )
    # ### end Alembic commands ###

"""update users table

Revision ID: 687fca3a52c3
Revises: 5668fd187fad
Create Date: 2024-12-18 19:27:04.242661

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "687fca3a52c3"
down_revision: Union[str, None] = "5668fd187fad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("full_name", sa.String(), nullable=False))
    op.add_column("users", sa.Column("age", sa.Integer(), nullable=False))
    op.create_unique_constraint(
        op.f("uq_users_full_name_age"), "users", ["full_name", "age"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("uq_users_full_name_age"), "users", type_="unique")
    op.drop_column("users", "age")
    op.drop_column("users", "full_name")
    # ### end Alembic commands ###

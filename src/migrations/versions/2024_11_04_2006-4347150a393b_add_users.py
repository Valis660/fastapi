"""Add Users

Revision ID: 4347150a393b
Revises: 73d6b03b21bf
Create Date: 2024-11-04 20:06:16.208040

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "4347150a393b"
down_revision: Union[str, None] = "73d6b03b21bf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")

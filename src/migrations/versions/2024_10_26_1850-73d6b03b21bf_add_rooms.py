"""Add Rooms

Revision ID: 73d6b03b21bf
Revises: 7ab91dab5978
Create Date: 2024-10-26 18:50:44.507956

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "73d6b03b21bf"
down_revision: Union[str, None] = "7ab91dab5978"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms")


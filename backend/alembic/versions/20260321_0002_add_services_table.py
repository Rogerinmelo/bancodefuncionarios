"""add services table

Revision ID: 20260321_0002
Revises: 20260321_0001
Create Date: 2026-03-21 00:30:01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260321_0002"
down_revision: Union[str, None] = "20260321_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "services",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("company_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("company_id", "name", name="uq_services_company_name"),
    )


def downgrade() -> None:
    op.drop_table("services")

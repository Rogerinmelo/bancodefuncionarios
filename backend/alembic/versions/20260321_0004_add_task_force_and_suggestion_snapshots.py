"""add task force and suggestion snapshots

Revision ID: 20260321_0004
Revises: 20260321_0003
Create Date: 2026-03-21 01:30:01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260321_0004"
down_revision: Union[str, None] = "20260321_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "task_forces",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("demand_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["demand_id"], ["demands.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "task_force_members",
        sa.Column("task_force_id", sa.Uuid(), nullable=False),
        sa.Column("employee_id", sa.Uuid(), nullable=False),
        sa.Column("role_in_team", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["task_force_id"], ["task_forces.id"]),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.PrimaryKeyConstraint("task_force_id", "employee_id"),
    )

    op.create_table(
        "demand_suggestion_snapshots",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("demand_id", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["demand_id"], ["demands.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "demand_suggestion_snapshot_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("snapshot_id", sa.Uuid(), nullable=False),
        sa.Column("employee_id", sa.Uuid(), nullable=False),
        sa.Column("employee_name", sa.Text(), nullable=False),
        sa.Column("score", sa.Numeric(10, 2), nullable=False),
        sa.Column("matched_required_skills", sa.Integer(), nullable=False),
        sa.Column("total_required_skills", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["snapshot_id"], ["demand_suggestion_snapshots.id"]),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("demand_suggestion_snapshot_items")
    op.drop_table("demand_suggestion_snapshots")
    op.drop_table("task_force_members")
    op.drop_table("task_forces")

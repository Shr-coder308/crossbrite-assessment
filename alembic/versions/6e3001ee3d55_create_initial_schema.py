"""create initial schema

Revision ID: 6e3001ee3d55
Revises:
Create Date: 2026-09-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6e3001ee3d55"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the initial database schema."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
    )

    op.create_index(
        "ix_users_id",
        "users",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=True,
    )

    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("teacher_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="scheduled",
        ),
        sa.Column("scheduled_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["teacher_id"],
            ["users.id"],
        ),
    )

    op.create_index(
        "ix_sessions_id",
        "sessions",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_sessions_teacher_id",
        "sessions",
        ["teacher_id"],
        unique=False,
    )

    op.create_table(
        "parent_children",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("parent_id", sa.Integer(), nullable=False),
        sa.Column("child_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["child_id"],
            ["users.id"],
        ),
        sa.UniqueConstraint(
            "parent_id",
            "child_id",
            name="uq_parent_child",
        ),
    )

    op.create_index(
        "ix_parent_children_id",
        "parent_children",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_parent_children_parent_id",
        "parent_children",
        ["parent_id"],
        unique=False,
    )

    op.create_index(
        "ix_parent_children_child_id",
        "parent_children",
        ["child_id"],
        unique=False,
    )

    op.create_table(
        "evaluations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["sessions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["users.id"],
        ),
    )

    op.create_index(
        "ix_evaluations_id",
        "evaluations",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_evaluations_session_id",
        "evaluations",
        ["session_id"],
        unique=False,
    )

    op.create_index(
        "ix_evaluations_student_id",
        "evaluations",
        ["student_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop the initial database schema."""

    op.drop_index(
        "ix_evaluations_student_id",
        table_name="evaluations",
    )
    op.drop_index(
        "ix_evaluations_session_id",
        table_name="evaluations",
    )
    op.drop_index(
        "ix_evaluations_id",
        table_name="evaluations",
    )
    op.drop_table("evaluations")

    op.drop_index(
        "ix_parent_children_child_id",
        table_name="parent_children",
    )
    op.drop_index(
        "ix_parent_children_parent_id",
        table_name="parent_children",
    )
    op.drop_index(
        "ix_parent_children_id",
        table_name="parent_children",
    )
    op.drop_table("parent_children")

    op.drop_index(
        "ix_sessions_teacher_id",
        table_name="sessions",
    )
    op.drop_index(
        "ix_sessions_id",
        table_name="sessions",
    )
    op.drop_table("sessions")

    op.drop_index(
        "ix_users_email",
        table_name="users",
    )
    op.drop_index(
        "ix_users_id",
        table_name="users",
    )
    op.drop_table("users")
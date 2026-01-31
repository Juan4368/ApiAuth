"""rename users tables to user

Revision ID: 20260131_0002
Revises: 20260130_0001
Create Date: 2026-01-31
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "20260131_0002"
down_revision = "20260130_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename users -> user only if the source table exists.
    op.execute('ALTER TABLE IF EXISTS users RENAME TO "user"')
    op.execute("ALTER INDEX IF EXISTS ix_users_id RENAME TO ix_user_id")
    op.execute("ALTER INDEX IF EXISTS ix_users_username RENAME TO ix_user_username")
    op.execute("ALTER INDEX IF EXISTS ix_users_email RENAME TO ix_user_email")
    op.execute(
        """
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_users_username') THEN
        ALTER TABLE "user" RENAME CONSTRAINT uq_users_username TO uq_user_username;
    END IF;
END
$$;
"""
    )
    op.execute(
        """
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_users_email') THEN
        ALTER TABLE "user" RENAME CONSTRAINT uq_users_email TO uq_user_email;
    END IF;
END
$$;
"""
    )

    # Keep join table name as user_roles to match existing schema.


def downgrade() -> None:
    # Keep join table name as user_roles to match existing schema.

    op.execute('ALTER TABLE IF EXISTS "user" RENAME TO users')
    op.execute("ALTER INDEX IF EXISTS ix_user_id RENAME TO ix_users_id")
    op.execute("ALTER INDEX IF EXISTS ix_user_username RENAME TO ix_users_username")
    op.execute("ALTER INDEX IF EXISTS ix_user_email RENAME TO ix_users_email")
    op.execute(
        """
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_user_username') THEN
        ALTER TABLE users RENAME CONSTRAINT uq_user_username TO uq_users_username;
    END IF;
END
$$;
"""
    )
    op.execute(
        """
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_user_email') THEN
        ALTER TABLE users RENAME CONSTRAINT uq_user_email TO uq_users_email;
    END IF;
END
$$;
"""
    )

"""make thelefone_number nullable

Revision ID: 20260131_0004
Revises: 20260131_0003
Create Date: 2026-01-31
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260131_0004"
down_revision = "20260131_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'user' AND relkind = 'r') THEN
        ALTER TABLE "user" ALTER COLUMN thelefone_number DROP NOT NULL;
    ELSIF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'users' AND relkind = 'r') THEN
        ALTER TABLE users ALTER COLUMN thelefone_number DROP NOT NULL;
    END IF;
END
$$;
"""
    )


def downgrade() -> None:
    op.execute(
        """
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'user' AND relkind = 'r') THEN
        ALTER TABLE "user" ALTER COLUMN thelefone_number SET NOT NULL;
    ELSIF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'users' AND relkind = 'r') THEN
        ALTER TABLE users ALTER COLUMN thelefone_number SET NOT NULL;
    END IF;
END
$$;
"""
    )

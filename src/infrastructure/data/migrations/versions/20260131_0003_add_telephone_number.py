"""add thelefone_number to user

Revision ID: 20260131_0003
Revises: 20260131_0002
Create Date: 2026-01-31
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260131_0003"
down_revision = "20260131_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'user' AND relkind = 'r') THEN
        ALTER TABLE "user" ADD COLUMN IF NOT EXISTS thelefone_number VARCHAR(255) DEFAULT '' NOT NULL;
        ALTER TABLE "user" ALTER COLUMN thelefone_number DROP DEFAULT;
    ELSIF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'users' AND relkind = 'r') THEN
        ALTER TABLE users ADD COLUMN IF NOT EXISTS thelefone_number VARCHAR(255) DEFAULT '' NOT NULL;
        ALTER TABLE users ALTER COLUMN thelefone_number DROP DEFAULT;
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
        ALTER TABLE "user" DROP COLUMN IF EXISTS thelefone_number;
    ELSIF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'users' AND relkind = 'r') THEN
        ALTER TABLE users DROP COLUMN IF EXISTS thelefone_number;
    END IF;
END
$$;
"""
    )

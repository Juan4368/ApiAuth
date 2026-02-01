"""rename thelefone_number to telephone_number

Revision ID: 20260201_0006
Revises: 20260131_0005
Create Date: 2026-02-01
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260201_0006"
down_revision = "20260131_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'user' AND column_name = 'thelefone_number'
    ) AND NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'user' AND column_name = 'telephone_number'
    ) THEN
        ALTER TABLE "user" RENAME COLUMN thelefone_number TO telephone_number;
    ELSIF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'users' AND column_name = 'thelefone_number'
    ) AND NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'users' AND column_name = 'telephone_number'
    ) THEN
        ALTER TABLE users RENAME COLUMN thelefone_number TO telephone_number;
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
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'user' AND column_name = 'telephone_number'
    ) AND NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'user' AND column_name = 'thelefone_number'
    ) THEN
        ALTER TABLE "user" RENAME COLUMN telephone_number TO thelefone_number;
    ELSIF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'users' AND column_name = 'telephone_number'
    ) AND NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'users' AND column_name = 'thelefone_number'
    ) THEN
        ALTER TABLE users RENAME COLUMN telephone_number TO thelefone_number;
    END IF;
END
$$;
"""
    )

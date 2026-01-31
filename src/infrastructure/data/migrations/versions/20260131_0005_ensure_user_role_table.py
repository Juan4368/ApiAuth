"""ensure user_roles table exists

Revision ID: 20260131_0005
Revises: 20260131_0004
Create Date: 2026-01-31
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "20260131_0005"
down_revision = "20260131_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'user_roles' AND relkind = 'r') THEN
        IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_roles') THEN
            EXECUTE 'DROP TYPE IF EXISTS user_roles';
        END IF;
        IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'user' AND relkind = 'r') THEN
            EXECUTE '
                CREATE TABLE user_roles (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
                    created_at TIMESTAMP NOT NULL DEFAULT now(),
                    CONSTRAINT uq_user_role UNIQUE (user_id, role_id)
                )';
        ELSIF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'users' AND relkind = 'r') THEN
            EXECUTE '
                CREATE TABLE user_roles (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
                    created_at TIMESTAMP NOT NULL DEFAULT now(),
                    CONSTRAINT uq_user_role UNIQUE (user_id, role_id)
                )';
        END IF;
    END IF;
END
$$;
"""
    )
    op.execute(
        """
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'user_roles' AND relkind = 'r') THEN
        EXECUTE 'CREATE INDEX IF NOT EXISTS ix_user_roles_id ON user_roles (id)';
    END IF;
END
$$;
"""
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_user_roles_id")
    op.execute("DROP TABLE IF EXISTS user_roles")

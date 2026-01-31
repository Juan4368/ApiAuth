from __future__ import annotations

from pathlib import Path
import sys

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
for path in (PROJECT_ROOT, SRC_DIR):
    if str(path) not in sys.path:
        sys.path.append(str(path))

from domain.entities.role import Role
from domain.entities.user import User
from infrastructure.data.db import SessionLocal
from infrastructure.repository.role_repository_sqlalchemy import RoleRepositorySQLAlchemy
from infrastructure.repository.user_repository_sqlalchemy import UserRepositorySQLAlchemy
from infrastructure.security.password_hasher import PasslibHasher


def seed_users_and_roles() -> None:
    load_dotenv(PROJECT_ROOT / ".env")

    db = SessionLocal()
    try:
        role_repo = RoleRepositorySQLAlchemy(db)
        user_repo = UserRepositorySQLAlchemy(db)
        hasher = PasslibHasher()

        roles_to_seed = [
            {"name": "admin", "description": "Administrador"},
            {"name": "user", "description": "Usuario"},
        ]

        role_ids: dict[str, int] = {}
        for role_data in roles_to_seed:
            existing = role_repo.get_by_name(role_data["name"])
            if existing:
                role_ids[role_data["name"]] = existing.id or 0
                continue
            created = role_repo.create(
                Role(
                    id=None,
                    name=role_data["name"],
                    description=role_data["description"],
                    created_at=None,
                    updated_at=None,
                )
            )
            role_ids[created.name] = created.id or 0

        users_to_seed = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "password": "Admin123!",
                "roles": ["admin"],
                "is_verified": True,
            },
            {
                "username": "demo",
                "email": "demo@example.com",
                "password": "Demo123!",
                "roles": ["user"],
                "is_verified": True,
            },
        ]

        for user_data in users_to_seed:
            existing = user_repo.get_by_username(user_data["username"])
            if not existing:
                user = User(
                    id=None,
                    username=user_data["username"],
                    email=user_data["email"],
                    password_hash=hasher.hash(user_data["password"]),
                    is_active=True,
                    is_verified=bool(user_data["is_verified"]),
                    created_at=None,
                    updated_at=None,
                    last_login_at=None,
                )
                created = user_repo.create(user)
                user_id = created.id or 0
            else:
                user_id = existing.id or 0

            current_roles = set(user_repo.get_roles(user_id))
            for role_name in user_data["roles"]:
                if role_name in current_roles:
                    continue
                role_id = role_ids.get(role_name)
                if role_id:
                    user_repo.add_role(user_id, role_id)
    finally:
        db.close()


if __name__ == "__main__":
    seed_users_and_roles()
    print("Seed completado: usuarios y roles creados/actualizados.")

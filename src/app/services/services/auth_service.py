from datetime import datetime

from app.services.interfaces.password_hasher import PasswordHasher
from app.services.interfaces.role_repository import RoleRepository
from app.services.interfaces.token_service import TokenService
from app.services.interfaces.user_repository import UserRepository
from domain.entities.role import Role
from domain.entities.user import User


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        role_repo: RoleRepository,
        hasher: PasswordHasher,
        token_service: TokenService,
        require_verified: bool = True,
    ) -> None:
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.hasher = hasher
        self.token_service = token_service
        self.require_verified = require_verified

    def register(self, username: str, email: str, password: str) -> User:
        if self.user_repo.get_by_username(username):
            raise ValueError("Username already exists")
        if self.user_repo.get_by_email(email):
            raise ValueError("Email already exists")

        user = User(
            id=None,
            username=username,
            email=email,
            password_hash=self.hasher.hash(password),
            is_active=True,
            is_verified=False,
            created_at=None,
            updated_at=None,
            last_login_at=None,
        )
        return self.user_repo.create(user)

    def authenticate(self, username: str, password: str) -> tuple[User, list[str], str]:
        user = self.user_repo.get_by_username(username)
        if not user or not self.hasher.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")
        if not user.is_active:
            raise ValueError("User is inactive")
        if self.require_verified and not user.is_verified:
            raise ValueError("User is not verified")

        roles = self.user_repo.get_roles(user.id or 0)
        token = self.token_service.create_access_token(
            subject=str(user.id),
            claims={"username": user.username, "roles": roles},
        )
        self.user_repo.update_last_login(user.id or 0)
        return user, roles, token

    def create_role(self, name: str, description: str | None) -> Role:
        existing = self.role_repo.get_by_name(name)
        if existing:
            raise ValueError("Role already exists")
        role = Role(
            id=None,
            name=name,
            description=description,
            created_at=None,
            updated_at=None,
        )
        return self.role_repo.create(role)

    def assign_role(self, username: str, role_name: str) -> None:
        user = self.user_repo.get_by_username(username)
        if not user:
            raise ValueError("User not found")
        role = self.role_repo.get_by_name(role_name)
        if not role:
            raise ValueError("Role not found")
        self.user_repo.add_role(user.id or 0, role.id or 0)

    def get_user_profile(self, user_id: int) -> tuple[User, list[str]]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        roles = self.user_repo.get_roles(user.id or 0)
        return user, roles

    def verify_user(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        updated = self.user_repo.set_verified(user_id, True)
        if not updated:
            raise ValueError("User not found")
        return updated

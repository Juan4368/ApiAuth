from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.services.interfaces.user_repository import UserRepository
from domain.entities.user import User
from infrastructure.data.models.role_model import RoleModel
from infrastructure.data.models.user_model import UserModel
from infrastructure.data.models.user_role_model import UserRoleModel


class UserRepositorySQLAlchemy(UserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        row = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(row)

    def get_by_username(self, username: str) -> User | None:
        row = self.db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_entity(row)

    def get_by_email(self, email: str) -> User | None:
        row = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(row)

    def create(self, user: User) -> User:
        row = UserModel(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._to_entity(row)

    def update_last_login(self, user_id: int) -> None:
        row = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not row:
            return
        row.last_login_at = datetime.now(timezone.utc)
        self.db.commit()

    def get_roles(self, user_id: int) -> list[str]:
        stmt = (
            select(RoleModel.name)
            .join(UserRoleModel, UserRoleModel.role_id == RoleModel.id)
            .where(UserRoleModel.user_id == user_id)
        )
        return [name for (name,) in self.db.execute(stmt).all()]

    def add_role(self, user_id: int, role_id: int) -> None:
        row = UserRoleModel(user_id=user_id, role_id=role_id)
        self.db.add(row)
        self.db.commit()

    def set_verified(self, user_id: int, is_verified: bool) -> User | None:
        row = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not row:
            return None
        row.is_verified = is_verified
        self.db.commit()
        self.db.refresh(row)
        return self._to_entity(row)

    @staticmethod
    def _to_entity(row: UserModel | None) -> User | None:
        if not row:
            return None
        return User(
            id=row.id,
            username=row.username,
            email=row.email,
            password_hash=row.password_hash,
            is_active=row.is_active,
            is_verified=row.is_verified,
            created_at=row.created_at,
            updated_at=row.updated_at,
            last_login_at=row.last_login_at,
        )

from sqlalchemy.orm import Session

from app.services.interfaces.role_repository import RoleRepository
from domain.entities.role import Role
from infrastructure.data.models.role_model import RoleModel


class RoleRepositorySQLAlchemy(RoleRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, role_id: int) -> Role | None:
        row = self.db.query(RoleModel).filter(RoleModel.id == role_id).first()
        return self._to_entity(row)

    def get_by_name(self, name: str) -> Role | None:
        row = self.db.query(RoleModel).filter(RoleModel.name == name).first()
        return self._to_entity(row)

    def create(self, role: Role) -> Role:
        row = RoleModel(name=role.name, description=role.description)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._to_entity(row)

    def list_all(self) -> list[Role]:
        rows = self.db.query(RoleModel).order_by(RoleModel.name).all()
        return [self._to_entity(row) for row in rows if row]

    def update(self, role: Role) -> Role | None:
        row = self.db.query(RoleModel).filter(RoleModel.id == role.id).first()
        if not row:
            return None
        row.name = role.name
        row.description = role.description
        self.db.commit()
        self.db.refresh(row)
        return self._to_entity(row)

    @staticmethod
    def _to_entity(row: RoleModel | None) -> Role | None:
        if not row:
            return None
        return Role(
            id=row.id,
            name=row.name,
            description=row.description,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

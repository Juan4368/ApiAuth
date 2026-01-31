from app.services.interfaces.role_repository import RoleRepository
from app.services.interfaces.role_service import RoleService
from domain.entities.role import Role


class RoleServiceImpl(RoleService):
    def __init__(self, role_repo: RoleRepository) -> None:
        self.role_repo = role_repo

    def list_roles(self) -> list[Role]:
        return self.role_repo.list_all()

    def get_role(self, role_id: int) -> Role:
        role = self.role_repo.get_by_id(role_id)
        if not role:
            raise ValueError("Role not found")
        return role

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

    def update_role(self, role_id: int, name: str, description: str | None) -> Role:
        role = self.get_role(role_id)
        existing = self.role_repo.get_by_name(name)
        if existing and existing.id != role_id:
            raise ValueError("Role already exists")

        role.name = name
        role.description = description

        updated = self.role_repo.update(role)
        if not updated:
            raise ValueError("Role not found")
        return updated

    def patch_role(self, role_id: int, name: str | None, description: str | None) -> Role:
        if name is None and description is None:
            raise ValueError("No fields to update")
        role = self.get_role(role_id)
        if name is not None:
            existing = self.role_repo.get_by_name(name)
            if existing and existing.id != role_id:
                raise ValueError("Role already exists")
            role.name = name
        if description is not None:
            role.description = description

        updated = self.role_repo.update(role)
        if not updated:
            raise ValueError("Role not found")
        return updated

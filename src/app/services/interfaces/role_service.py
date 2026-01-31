from abc import ABC, abstractmethod

from domain.entities.role import Role


class RoleService(ABC):
    @abstractmethod
    def list_roles(self) -> list[Role]: ...

    @abstractmethod
    def get_role(self, role_id: int) -> Role: ...

    @abstractmethod
    def create_role(self, name: str, description: str | None) -> Role: ...

    @abstractmethod
    def update_role(self, role_id: int, name: str, description: str | None) -> Role: ...

    @abstractmethod
    def patch_role(
        self,
        role_id: int,
        name: str | None,
        description: str | None,
    ) -> Role: ...

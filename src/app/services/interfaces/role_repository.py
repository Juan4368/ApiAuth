from abc import ABC, abstractmethod

from domain.entities.role import Role


class RoleRepository(ABC):
    @abstractmethod
    def get_by_id(self, role_id: int) -> Role | None: ...

    @abstractmethod
    def get_by_name(self, name: str) -> Role | None: ...

    @abstractmethod
    def create(self, role: Role) -> Role: ...

    @abstractmethod
    def list_all(self) -> list[Role]: ...

    @abstractmethod
    def update(self, role: Role) -> Role | None: ...

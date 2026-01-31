from abc import ABC, abstractmethod

from domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def create(self, user: User) -> User: ...

    @abstractmethod
    def update_last_login(self, user_id: int) -> None: ...

    @abstractmethod
    def get_roles(self, user_id: int) -> list[str]: ...

    @abstractmethod
    def add_role(self, user_id: int, role_id: int) -> None: ...

    @abstractmethod
    def set_verified(self, user_id: int, is_verified: bool) -> User | None: ...

from abc import ABC, abstractmethod


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, subject: str, claims: dict) -> str: ...

    @abstractmethod
    def verify_access_token(self, token: str) -> dict: ...

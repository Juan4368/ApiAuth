import bcrypt
from passlib.context import CryptContext

from app.services.interfaces.password_hasher import PasswordHasher


class PasslibHasher(PasswordHasher):
    def __init__(self) -> None:
        self._ctx = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

    @staticmethod
    def _normalize(plain: str) -> bytes:
        # bcrypt only accepts up to 72 bytes; truncate to avoid runtime errors.
        raw = plain.encode("utf-8")
        return raw[:72] if len(raw) > 72 else raw

    def hash(self, plain: str) -> str:
        # Use bcrypt_sha256 to avoid the 72-byte limit for new hashes.
        try:
            return self._ctx.hash(plain)
        except ValueError as exc:
            if "72 bytes" in str(exc):
                normalized = self._normalize(plain)
                return bcrypt.hashpw(normalized, bcrypt.gensalt()).decode("utf-8")
            raise

    def verify(self, plain: str, hashed: str) -> bool:
        try:
            if hashed.startswith("$bcrypt-sha256$"):
                return self._ctx.verify(plain, hashed)
            normalized = self._normalize(plain)
            return bcrypt.checkpw(normalized, hashed.encode("utf-8"))
        except ValueError as exc:
            if "72 bytes" in str(exc):
                normalized = self._normalize(plain)
                return bcrypt.checkpw(normalized, hashed.encode("utf-8"))
            raise

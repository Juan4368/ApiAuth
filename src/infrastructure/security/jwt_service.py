import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt

from app.services.interfaces.token_service import TokenService


load_dotenv()


class JwtService(TokenService):
    def __init__(
        self,
        secret_key: str | None = None,
        algorithm: str | None = None,
        access_token_minutes: int | None = None,
    ) -> None:
        self.secret_key = secret_key or os.getenv("JWT_SECRET_KEY", "")
        self.algorithm = algorithm or os.getenv("JWT_ALGORITHM", "HS256")
        minutes = access_token_minutes or int(os.getenv("JWT_ACCESS_MINUTES", "60"))
        self.access_token_minutes = minutes

        if not self.secret_key:
            raise ValueError("JWT_SECRET_KEY is not set")

    def create_access_token(self, subject: str, claims: dict) -> str:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_token_minutes)
        payload = {"sub": subject, "iat": now, "exp": expire}
        payload.update(claims or {})
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as exc:
            raise ValueError("Invalid or expired token") from exc

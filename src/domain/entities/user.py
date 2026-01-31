from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int | None
    username: str
    email: str
    password_hash: str
    is_active: bool
    is_verified: bool
    created_at: datetime | None
    updated_at: datetime | None
    last_login_at: datetime | None

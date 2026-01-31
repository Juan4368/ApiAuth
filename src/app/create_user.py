from pathlib import Path
import sys

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
for path in (SRC_DIR, PROJECT_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

load_dotenv(PROJECT_ROOT / ".env")

from infrastructure.data.db import SessionLocal
from infrastructure.data.models.user_model import UserModel
from infrastructure.security.password_hasher import PasslibHasher


def create_user(username: str, email: str, password: str, is_verified: bool = True) -> None:
    session = SessionLocal()
    try:
        existing = session.query(UserModel).filter(UserModel.username == username).first()
        if existing:
            raise ValueError(f"User '{username}' already exists")
        hasher = PasslibHasher()
        user = UserModel(
            username=username,
            email=email,
            password_hash=hasher.hash(password),
            is_active=True,
            is_verified=is_verified,
        )
        session.add(user)
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    create_user("juanfer", "juanfer@example.com", "Juan2026", is_verified=True)
    print("User created: juanfer / Juan2026")

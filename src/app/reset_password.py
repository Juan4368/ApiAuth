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


def reset_password(username: str, new_password: str) -> None:
    session = SessionLocal()
    try:
        user = session.query(UserModel).filter(UserModel.username == username).first()
        if not user:
            raise ValueError(f"User '{username}' not found")
        hasher = PasslibHasher()
        user.password_hash = hasher.hash(new_password)
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    reset_password("juanfer", "Juan2026")
    print("Password updated for juanfer")

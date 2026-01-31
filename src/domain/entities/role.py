from dataclasses import dataclass
from datetime import datetime


@dataclass
class Role:
    id: int | None
    name: str
    description: str | None
    created_at: datetime | None
    updated_at: datetime | None

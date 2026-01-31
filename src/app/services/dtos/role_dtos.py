from datetime import datetime
from pydantic import BaseModel, Field


class RoleCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=200)


class RoleUpdateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=200)


class RolePatchRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=200)


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime | None
    updated_at: datetime | None

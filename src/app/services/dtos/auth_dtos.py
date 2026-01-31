from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from app.services.dtos.role_dtos import RoleCreateRequest, RoleResponse


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class AssignRoleRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    role_name: str = Field(min_length=2, max_length=50)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    roles: list[str]
    created_at: datetime | None
    updated_at: datetime | None
    last_login_at: datetime | None


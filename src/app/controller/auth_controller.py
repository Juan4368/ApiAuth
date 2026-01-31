from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.services.dtos.auth_dtos import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.services.auth_service import AuthService
from infrastructure.data.db import get_db
from infrastructure.repository.role_repository_sqlalchemy import RoleRepositorySQLAlchemy
from infrastructure.repository.user_repository_sqlalchemy import UserRepositorySQLAlchemy
from infrastructure.security.jwt_service import JwtService
from infrastructure.security.password_hasher import PasslibHasher

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


def build_service(db: Session) -> AuthService:
    return AuthService(
        user_repo=UserRepositorySQLAlchemy(db),
        role_repo=RoleRepositorySQLAlchemy(db),
        hasher=PasslibHasher(),
        token_service=JwtService(),
        require_verified=True,
    )


def _user_response(service: AuthService, user_id: int) -> UserResponse:
    user, roles = service.get_user_profile(user_id)
    return UserResponse(
        id=user.id or 0,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        roles=roles,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login_at=user.last_login_at,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UserResponse:
    service = build_service(db)
    try:
        payload = service.token_service.verify_access_token(credentials.credentials)
        user_id = int(payload.get("sub", "0"))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    return _user_response(service, user_id)


def require_role(role_name: str):
    def _checker(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
        if role_name not in current_user.roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return current_user

    return _checker


@router.post("/register", response_model=UserResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)) -> UserResponse:
    service = build_service(db)
    try:
        user = service.register(data.username, data.email, data.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return _user_response(service, user.id or 0)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    service = build_service(db)
    try:
        _, _, token = service.authenticate(data.username, data.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return current_user


@router.patch("/users/{user_id}/verify", response_model=UserResponse)
def verify_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> UserResponse:
    service = build_service(db)
    try:
        user = service.verify_user(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return _user_response(service, user.id or 0)

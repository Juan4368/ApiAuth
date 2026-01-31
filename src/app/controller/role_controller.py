from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.services.dtos.auth_dtos import AssignRoleRequest, UserResponse
from app.services.dtos.role_dtos import (
    RoleCreateRequest,
    RolePatchRequest,
    RoleResponse,
    RoleUpdateRequest,
)
from app.services.services.auth_service import AuthService
from app.services.services.role_service import RoleServiceImpl
from domain.entities.role import Role
from infrastructure.data.db import get_db
from infrastructure.repository.user_repository_sqlalchemy import UserRepositorySQLAlchemy
from infrastructure.repository.role_repository_sqlalchemy import RoleRepositorySQLAlchemy
from infrastructure.security.password_hasher import PasslibHasher
from infrastructure.security.jwt_service import JwtService
from app.controller.auth_controller import require_role

router = APIRouter(prefix="/roles", tags=["roles"])


def build_service(db: Session) -> RoleServiceImpl:
    return RoleServiceImpl(role_repo=RoleRepositorySQLAlchemy(db))


def build_auth_service(db: Session) -> AuthService:
    return AuthService(
        user_repo=UserRepositorySQLAlchemy(db),
        role_repo=RoleRepositorySQLAlchemy(db),
        hasher=PasslibHasher(),
        token_service=JwtService(),
        require_verified=True,
    )


def _to_role_response(role: Role) -> RoleResponse:
    return RoleResponse(
        id=role.id or 0,
        name=role.name,
        description=role.description,
        created_at=role.created_at,
        updated_at=role.updated_at,
    )


def _handle_value_error(exc: ValueError) -> None:
    detail = str(exc)
    if detail == "Role not found":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail) from exc
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from exc


@router.get("/", response_model=list[RoleResponse])
def list_roles(db: Session = Depends(get_db)) -> list[RoleResponse]:
    service = build_service(db)
    roles = service.list_roles()
    return [_to_role_response(role) for role in roles]


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)) -> RoleResponse:
    service = build_service(db)
    try:
        role = service.get_role(role_id)
    except ValueError as exc:
        _handle_value_error(exc)
    return _to_role_response(role)


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(data: RoleCreateRequest, db: Session = Depends(get_db)) -> RoleResponse:
    service = build_service(db)
    try:
        role = service.create_role(data.name, data.description)
    except ValueError as exc:
        _handle_value_error(exc)
    return _to_role_response(role)


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    data: RoleUpdateRequest,
    db: Session = Depends(get_db),
) -> RoleResponse:
    service = build_service(db)
    try:
        role = service.update_role(role_id, data.name, data.description)
    except ValueError as exc:
        _handle_value_error(exc)
    return _to_role_response(role)


@router.patch("/{role_id}", response_model=RoleResponse)
def patch_role(
    role_id: int,
    data: RolePatchRequest,
    db: Session = Depends(get_db),
) -> RoleResponse:
    if data.name is None and data.description is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )
    service = build_service(db)
    try:
        role = service.patch_role(role_id, data.name, data.description)
    except ValueError as exc:
        _handle_value_error(exc)
    return _to_role_response(role)


@router.post("/assign")
def assign_role(
    data: AssignRoleRequest,
    db: Session = Depends(get_db),
) -> dict:
    service = build_auth_service(db)
    try:
        service.assign_role(data.username, data.role_name)
    except ValueError as exc:
        _handle_value_error(exc)
    return {"status": "ok"}

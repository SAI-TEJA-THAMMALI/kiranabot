from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.dependecies import get_current_user
from db.database import get_db
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.user_service import UserService

from schemas.user import (
    SignupRequest,
    SigninRequest,
    AuthResponse,
)


router = APIRouter(
    prefix="/users",
    tags=["User"]
)


def get_auth_service(db: Session = Depends(get_db)):
    repository = UserRepository(db)
    return AuthService(repository)


def get_user_service(db: Session = Depends(get_db)):
    repository = UserRepository(db)
    return UserService(repository)


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=201
)
def create_user(
    request: SignupRequest,
    service: AuthService = Depends(get_auth_service)
):
    result = service.signup(
        email=request.email,
        password=request.password
    )

    if result is None:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )

    return result


@router.post(
    "/signin",
    response_model=AuthResponse
)
def login_user(
    request: SigninRequest,
    service: AuthService = Depends(get_auth_service)
):
    result = service.signin(
        email=request.email,
        password=request.password
    )

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return result


@router.post("/logout")
def logout_user(
    current_user = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service)
):
    service.logout(current_user)

    return {
        "message": "Logged out successfully"
    }


@router.get("/{user_id}")
def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service)
):
    user = service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
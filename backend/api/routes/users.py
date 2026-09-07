from fastapi import APIRouter
from schemas.user import SigninRequest,SignupRequest
from uuid import UUID

router = APIRouter(prefix="/users",tags=["User"])

@router.post("/signup")
def create_user():
    pass

@router.post("/signin")
def login_user():
    pass
@router.post("/logout")
def logout_user():
    pass
@router.get("/")
def get_user(user_id:UUID):
    user = get_user(user_id)
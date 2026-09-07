import uuid
from auth.jwt import(
    create_access_token,
    create_refresh_token,
)
from auth.security import(
    hash_password,
    verify_password,
)
from db.models import User
from repositories.user_repository import UserRepository

class AuthService:
    def __init__(self,repository:UserRepository):
        self.repository  = repository
    def signup(self,email:str,password:str):
        existing_user = self.repository.get_by_email(email)
        if existing_user:
            return None
        password_hash = hash_password(password)
        user = User(
            email=email,
            password_hash=password_hash
        )
        self.repository.create(user)
        self.repository.db.flush()
        session_id = str(uuid.uuid4())
        access_token = create_access_token(
            user_id=str(user.id),session_id=str(session_id)
        )
        refresh_token = create_refresh_token(user_id=str(user.id),session_id=str(session_id))
        user.session_id = uuid.UUID(session_id)
        user.refresh_token = refresh_token
        self.repository.db.commit()
        self.repository.db.refresh(user)

        return {
            "user":user,
            "access_token":access_token,
            "refresh_token":refresh_token,
            "token_type":"bearer"
        }
    def signin(self, email: str, password: str):
        user = self.repository.get_by_email(email)

        if user is None:
            return None

        if not verify_password(password, user.password_hash):
            return None

        session_id = str(uuid.uuid4())

        access_token = create_access_token(
            user_id=str(user.id),
            session_id=session_id
        )

        refresh_token = create_refresh_token(
            user_id=str(user.id),
            session_id=session_id
        )

        # Store current session
        user.session_id = uuid.UUID(session_id)
        user.refresh_token = refresh_token

        self.repository.db.commit()
        self.repository.db.refresh(user)

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    def logout(self, user):
        user.session_id = None
        user.refresh_token = None

        self.repository.db.commit()

        return True

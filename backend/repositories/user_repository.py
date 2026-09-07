from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: UUID):
        stmt = select(User).where(User.id == user_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def create(self, user: User):
        self.db.add(user)
        return user

    def update(self, user: User):
        return user
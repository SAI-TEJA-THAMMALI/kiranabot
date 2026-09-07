from uuid import UUID

from repositories.user_repository import UserRepository


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, user_id: UUID):
        return self.repository.get_by_id(user_id)
    def create_user(self,email:str,password:str):
        return self.repository.create(email,password)
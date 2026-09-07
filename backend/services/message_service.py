from uuid import UUID

from db.models import Message
from repositories.message_repository import MessageRepository


class MessageService:

    def __init__(self, repository: MessageRepository):
        self.repository = repository

    def get_message(self, message_id: UUID):
        return self.repository.get_by_id(message_id)

    def get_conversation_messages(self, conversation_id: UUID):
        return self.repository.get_by_conversation_id(conversation_id)

    def create_message(self, message: Message):
        return self.repository.create(message)

    def update_message(self, message: Message):
        return self.repository.update(message)

    def delete_message(self, message_id: UUID):
        return self.repository.delete(message_id)
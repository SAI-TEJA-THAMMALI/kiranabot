from uuid import UUID

from db.models import Conversation
from repositories.conversation_repository import ConversationRepository


class ConversationService:

    def __init__(self, repository: ConversationRepository):
        self.repository = repository

    def get_conversation(self, conversation_id: UUID):
        return self.repository.get_by_id(conversation_id)

    def get_user_conversations(self, user_id: UUID):
        return self.repository.get_by_user_id(user_id)

    def create_conversation(self, conversation: Conversation):
        return self.repository.create(conversation)

    def update_conversation(self, conversation: Conversation):
        return self.repository.update(conversation)

    def delete_conversation(self, conversation_id: UUID):
        return self.repository.delete(conversation_id)
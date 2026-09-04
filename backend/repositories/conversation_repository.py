from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Conversation


class ConversationRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, conversation_id: UUID):
        stmt = select(Conversation).where(
            Conversation.id == conversation_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_user_id(self, user_id: UUID):
        stmt = select(Conversation).where(
            Conversation.user_id == user_id
        )

        result = self.db.execute(stmt)

        return result.scalars().all()

    def create(self, conversation: Conversation):
        self.db.add(conversation)
        self.db.flush()
        self.db.refresh(conversation)

        return conversation

    def update(self, conversation: Conversation):
        self.db.flush()
        self.db.refresh(conversation)

        return conversation

    def delete(self, conversation_id: UUID):
        conversation = self.get_by_id(conversation_id)

        if conversation is None:
            return None

        self.db.delete(conversation)
        self.db.flush()

        return conversation
    
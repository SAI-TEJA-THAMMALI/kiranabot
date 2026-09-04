from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Message


class MessageRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, message_id: UUID):
        stmt = select(Message).where(
            Message.id == message_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_conversation_id(self, conversation_id: UUID):
        stmt = select(Message).where(
            Message.conversation_id == conversation_id
        )

        result = self.db.execute(stmt)

        return result.scalars().all()

    def create(self, message: Message):
        self.db.add(message)
        self.db.flush()
        self.db.refresh(message)

        return message

    def update(self, message: Message):
        self.db.flush()
        self.db.refresh(message)

        return message

    def delete(self, message_id: UUID):
        message = self.get_by_id(message_id)

        if message is None:
            return None

        self.db.delete(message)
        self.db.flush()

        return message
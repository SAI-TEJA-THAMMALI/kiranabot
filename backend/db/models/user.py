import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    email: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    refresh_token: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    session_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now()
    )

    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="user"
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="user"
    )
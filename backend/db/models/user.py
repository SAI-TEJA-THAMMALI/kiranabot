import uuid
from datetime import datetime
from sqlalchemy import String,DateTime,func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import  Mapped,mapped_column
from .base import Base

class User(Base):
    __tablename__="users"

    id:Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    email:Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    created_at: Mapped[datetime]=mapped_column(
        DateTime(timezone=False),
        nullable=False
    )
    updated_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=False),
        nullable=False
    )
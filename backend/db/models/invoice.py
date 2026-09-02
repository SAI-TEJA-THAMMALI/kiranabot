from sqlalchemy import DateTime,ForeignKey,String,func
from sqlalchemy.orm import Mapped,mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID,JSONB
from datetime import datetime



from .base import Base
from sqlalchemy.orm import relationship

class Invoice(Base):
    __tablename__= "invoices"
    id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    file_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,

    )
    user_id: Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False

    )
    Invoice_file_link: Mapped[str | None]=mapped_column(
        String,
        nullable=True
    )
    ocr_result: Mapped[dict]=mapped_column(
        JSONB,
        nullable=False,
        server_default='{}'
    )
    status:Mapped[str] = mapped_column(
        JSONB,
        nullable=False,
        server_default="Processing"
    )
    validation_results: Mapped[dict]=mapped_column(
        JSONB,
        nullable=False,
        server_default='{}'
    )
    filename: Mapped[str]=mapped_column(
        String,
        nullable=False
    )
    created_at: Mapped[datetime | None]=mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now()
    )
    updated_at: Mapped[datetime | None]=mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now()

    )
    user: Mapped["User"] = relationship(
    back_populates="invoices"
    )

    jobs: Mapped[list["Job"]] = relationship(
        back_populates="invoice"
    )
    

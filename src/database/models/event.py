from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text

from src.database.database import Base

class Event(Base):
    __tablename__ = "event"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text('uuid_generate_v4()'))
    title: Mapped[str]
    description: Mapped[str]
    image_url: Mapped[str]
    date_event: Mapped[datetime]
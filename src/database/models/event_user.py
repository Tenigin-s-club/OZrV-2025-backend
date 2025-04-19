from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, ForeignKey

from src.database.database import Base

class EventUser(Base):
    __tablename__ = "event_user"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text('uuid_generate_v4()'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    event_id: Mapped[UUID] = mapped_column(ForeignKey("event.id"))
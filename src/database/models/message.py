import uuid
import datetime

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import DeclarativeBase


class Message(DeclarativeBase):
    __tablename__ = "message"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('uuid_generate_v4()'))
    is_human: Mapped[bool]
    content: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
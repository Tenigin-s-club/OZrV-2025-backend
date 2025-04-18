import uuid
import datetime

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base

class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('uuid_generate_v4()'))
    name: Mapped[str]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
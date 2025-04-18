import uuid

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('uuid_generate_v4()'))
    fio: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]

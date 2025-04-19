from datetime import date

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class Statistics(Base):
    __tablename__ = 'statistics'

    id: Mapped[int] = mapped_column(primary_key=True)
    request_time: Mapped[float]
    requested_at: Mapped[date] = mapped_column(server_default=text("CURRENT_DATE"))

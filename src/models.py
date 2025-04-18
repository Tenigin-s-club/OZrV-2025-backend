from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class QuestionAnswer(Base):
    __tablename__ = 'question_answers'

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str]
    answer: Mapped[str]
    embedding: Mapped[str]
    url: Mapped[str] = mapped_column(nullable=True)

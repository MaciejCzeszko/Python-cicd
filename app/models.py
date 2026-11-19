from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
from pydantic import BaseModel

class Score(Base):
    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    score: Mapped[int] = mapped_column(default=0)

class ScoreIn(BaseModel):
    name: str
    score: int
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String
from typing import Optional
class Debate():
    __tablename__ = "DEBATE"
    topic: Mapped[str] = mapped_column(String(255))
    user_analogy:Mapped[Optional[str]] = mapped_column(String(255))
    optimist_model: Mapped[str] = mapped_column(String(255))
    realist_model: Mapped[str] = mapped_column(String(255))
    skeptic_model:Mapped[str] = mapped_column(String(255))
    referee_model:Mapped[str|None] = mapped_column(default="gemini-2.5-pro")
    rounds_count:Mapped[int] = mapped_column(default =5)


from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id"),
        nullable=False,
        index=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending"
    )

    score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
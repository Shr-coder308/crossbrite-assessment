from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ParentChild(Base):
    __tablename__ = "parent_children"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    parent_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    child_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
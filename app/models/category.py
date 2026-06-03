from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.task import Task


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    color: Mapped[str] = mapped_column(String(7), nullable=False, default="#6c757d")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="category")

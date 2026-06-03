import enum
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, Date, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.category import Category


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, native_enum=False),
        nullable=False,
        default=TaskStatus.todo,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SAEnum(TaskPriority, native_enum=False),
        nullable=False,
        default=TaskPriority.medium,
    )
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    category: Mapped[Optional["Category"]] = relationship(
        "Category", back_populates="tasks"
    )

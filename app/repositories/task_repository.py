from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, or_, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from app.database import Base
from app.domain.task import Task, TaskPriority, TaskStatus


class TaskRecord(Base):
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

    category: Mapped[Optional["CategoryRecord"]] = relationship(  # noqa: F821
        "CategoryRecord", back_populates="tasks"
    )


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, record: TaskRecord) -> Task:
        return Task(
            id=record.id,
            title=record.title,
            description=record.description,
            status=record.status,
            priority=record.priority,
            due_date=record.due_date,
            category_id=record.category_id,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )

    def get_all(
        self,
        status: Optional[TaskStatus] = None,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
    ) -> list[Task]:
        query = self.db.query(TaskRecord)
        if status is not None:
            query = query.filter(TaskRecord.status == status)
        if category_id is not None:
            query = query.filter(TaskRecord.category_id == category_id)
        if search:
            query = query.filter(
                or_(
                    TaskRecord.title.ilike(f"%{search}%"),
                    TaskRecord.description.ilike(f"%{search}%"),
                )
            )
        return [self._to_domain(r) for r in query.order_by(TaskRecord.created_at.desc()).all()]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        record = self.db.query(TaskRecord).filter(TaskRecord.id == task_id).first()
        return self._to_domain(record) if record else None

    def get_overdue(self, today: date) -> list[Task]:
        records = (
            self.db.query(TaskRecord)
            .filter(
                TaskRecord.due_date < today,
                TaskRecord.status.notin_([TaskStatus.done, TaskStatus.cancelled]),
            )
            .all()
        )
        return [self._to_domain(r) for r in records]

    def count_by_status(self) -> dict[str, int]:
        counts = {s.value: 0 for s in TaskStatus}
        rows = (
            self.db.query(TaskRecord.status, func.count(TaskRecord.id))
            .group_by(TaskRecord.status)
            .all()
        )
        for status, count in rows:
            counts[status.value] = count
        return counts

    def create(self, task: Task) -> Task:
        record = TaskRecord(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            category_id=task.category_id,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return self._to_domain(record)

    def update(self, task: Task) -> Task:
        record = self.db.query(TaskRecord).filter(TaskRecord.id == task.id).first()
        record.title = task.title
        record.description = task.description
        record.status = task.status
        record.priority = task.priority
        record.due_date = task.due_date
        record.category_id = task.category_id
        self.db.commit()
        self.db.refresh(record)
        return self._to_domain(record)

    def nullify_category(self, category_id: int) -> None:
        self.db.query(TaskRecord).filter(TaskRecord.category_id == category_id).update(
            {"category_id": None}
        )
        self.db.commit()

    def count_in_progress_by_category(self, category_id: int) -> int:
        return (
            self.db.query(TaskRecord)
            .filter(
                TaskRecord.category_id == category_id,
                TaskRecord.status == TaskStatus.in_progress,
            )
            .count()
        )

    def delete(self, task: Task) -> None:
        record = self.db.query(TaskRecord).filter(TaskRecord.id == task.id).first()
        self.db.delete(record)
        self.db.commit()

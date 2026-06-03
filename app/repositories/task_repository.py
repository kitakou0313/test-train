from datetime import date
from typing import Optional
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus, TaskPriority


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        status: Optional[TaskStatus] = None,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
    ) -> list[Task]:
        query = self.db.query(Task)
        if status is not None:
            query = query.filter(Task.status == status)
        if category_id is not None:
            query = query.filter(Task.category_id == category_id)
        if search:
            query = query.filter(
                or_(
                    Task.title.ilike(f"%{search}%"),
                    Task.description.ilike(f"%{search}%"),
                )
            )
        return query.order_by(Task.created_at.desc()).all()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_overdue(self, today: date) -> list[Task]:
        return (
            self.db.query(Task)
            .filter(
                Task.due_date < today,
                Task.status.notin_([TaskStatus.done, TaskStatus.cancelled]),
            )
            .all()
        )

    def count_by_status(self) -> dict[str, int]:
        counts = {s.value: 0 for s in TaskStatus}
        rows = self.db.query(Task.status, func.count(Task.id)).group_by(Task.status).all()
        for status, count in rows:
            counts[status.value] = count
        return counts

    def create(
        self,
        title: str,
        description: Optional[str],
        priority: TaskPriority,
        due_date: Optional[date],
        category_id: Optional[int],
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            category_id=category_id,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task: Task, **kwargs) -> Task:
        for key, value in kwargs.items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def nullify_category(self, category_id: int) -> None:
        self.db.query(Task).filter(Task.category_id == category_id).update(
            {"category_id": None}
        )
        self.db.commit()

    def count_in_progress_by_category(self, category_id: int) -> int:
        return (
            self.db.query(Task)
            .filter(
                Task.category_id == category_id,
                Task.status == TaskStatus.in_progress,
            )
            .count()
        )

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()

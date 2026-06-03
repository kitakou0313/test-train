from datetime import date
from typing import Optional

from app.models.task import Task, TaskStatus, TaskPriority
from app.repositories.task_repository import TaskRepository
from app.repositories.category_repository import CategoryRepository
from app.exceptions import (
    NotFoundError,
    InvalidStatusTransitionError,
    InvalidDueDateError,
)

# ステータス遷移の許可ルール
ALLOWED_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.todo: {TaskStatus.in_progress, TaskStatus.cancelled},
    TaskStatus.in_progress: {TaskStatus.done, TaskStatus.todo, TaskStatus.cancelled},
    TaskStatus.done: {TaskStatus.todo},
    TaskStatus.cancelled: {TaskStatus.todo},
}


class TaskService:
    def __init__(self, task_repo: TaskRepository, category_repo: CategoryRepository):
        self.task_repo = task_repo
        self.category_repo = category_repo

    def get_tasks(
        self,
        status: Optional[TaskStatus] = None,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
    ) -> list[Task]:
        return self.task_repo.get_all(
            status=status, category_id=category_id, search=search
        )

    def get_task(self, task_id: int) -> Task:
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            raise NotFoundError(f"タスク ID={task_id} が見つかりません")
        return task

    def get_overdue_tasks(self) -> list[Task]:
        return self.task_repo.get_overdue(date.today())

    def count_by_status(self) -> dict[str, int]:
        return self.task_repo.count_by_status()

    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: TaskPriority = TaskPriority.medium,
        due_date: Optional[date] = None,
        category_id: Optional[int] = None,
    ) -> Task:
        if due_date is not None and due_date < date.today():
            raise InvalidDueDateError("期日に過去の日付は設定できません")
        if category_id is not None and self.category_repo.get_by_id(category_id) is None:
            raise NotFoundError(f"カテゴリ ID={category_id} が見つかりません")
        return self.task_repo.create(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            category_id=category_id,
        )

    def update_task(
        self,
        task_id: int,
        title: str,
        description: Optional[str],
        priority: TaskPriority,
        due_date: Optional[date],
        category_id: Optional[int],
    ) -> Task:
        task = self.get_task(task_id)
        if due_date is not None and due_date < date.today():
            raise InvalidDueDateError("期日に過去の日付は設定できません")
        if category_id is not None and self.category_repo.get_by_id(category_id) is None:
            raise NotFoundError(f"カテゴリ ID={category_id} が見つかりません")
        return self.task_repo.update(
            task,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            category_id=category_id,
        )

    def transition_status(self, task_id: int, new_status: TaskStatus) -> Task:
        task = self.get_task(task_id)
        current = task.status
        if current == new_status:
            raise InvalidStatusTransitionError(
                f"タスクはすでに「{new_status.value}」状態です"
            )
        if new_status not in ALLOWED_TRANSITIONS.get(current, set()):
            raise InvalidStatusTransitionError(
                f"「{current.value}」から「{new_status.value}」への遷移は許可されていません"
            )
        return self.task_repo.update(task, status=new_status)

    def get_allowed_transitions(self, task: Task) -> set[TaskStatus]:
        return ALLOWED_TRANSITIONS.get(task.status, set())

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)
        self.task_repo.delete(task)

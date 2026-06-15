from datetime import date
from typing import Optional

from app.domain.task import Task, TaskPriority, TaskStatus
from app.exceptions import NotFoundError
from app.repositories.category_repository import CategoryRepository
from app.repositories.task_repository import TaskRepository


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
        Task.validate_due_date(due_date)
        if category_id is not None and self.category_repo.get_by_id(category_id) is None:
            raise NotFoundError(f"カテゴリ ID={category_id} が見つかりません")
        task = Task(
            id=0,
            title=title,
            description=description,
            status=TaskStatus.todo,
            priority=priority,
            due_date=due_date,
            category_id=category_id,
        )
        return self.task_repo.create(task)

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
        Task.validate_due_date(due_date)
        if category_id is not None and self.category_repo.get_by_id(category_id) is None:
            raise NotFoundError(f"カテゴリ ID={category_id} が見つかりません")
        task.title = title
        task.description = description
        task.priority = priority
        task.due_date = due_date
        task.category_id = category_id
        return self.task_repo.update(task)

    def transition_status(self, task_id: int, new_status: TaskStatus) -> Task:
        task = self.get_task(task_id)
        task.transition_to(new_status)
        return self.task_repo.update(task)

    def get_allowed_transitions(self, task: Task) -> set[TaskStatus]:
        return task.get_allowed_transitions()

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)
        self.task_repo.delete(task)

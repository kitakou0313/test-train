import enum
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from app.exceptions import InvalidDueDateError, InvalidStatusTransitionError


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


_ALLOWED_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.todo: {TaskStatus.in_progress, TaskStatus.cancelled},
    TaskStatus.in_progress: {TaskStatus.done, TaskStatus.todo, TaskStatus.cancelled},
    TaskStatus.done: {TaskStatus.todo},
    TaskStatus.cancelled: {TaskStatus.todo},
}


@dataclass
class Task:
    id: int
    title: str
    status: TaskStatus
    priority: TaskPriority
    description: Optional[str] = None
    due_date: Optional[date] = None
    category_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_allowed_transitions(self) -> set[TaskStatus]:
        return _ALLOWED_TRANSITIONS.get(self.status, set())

    def validate_transition(self, new_status: TaskStatus) -> None:
        if self.status == new_status:
            raise InvalidStatusTransitionError(
                f"タスクはすでに「{new_status.value}」状態です"
            )
        if new_status not in _ALLOWED_TRANSITIONS.get(self.status, set()):
            raise InvalidStatusTransitionError(
                f"「{self.status.value}」から「{new_status.value}」への遷移は許可されていません"
            )

    def transition_to(self, new_status: TaskStatus) -> None:
        self.validate_transition(new_status)
        self.status = new_status

    @staticmethod
    def validate_due_date(due_date: Optional[date]) -> None:
        if due_date is not None and due_date < date.today():
            raise InvalidDueDateError("期日に過去の日付は設定できません")

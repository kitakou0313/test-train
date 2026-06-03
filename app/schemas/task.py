from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel

from app.models.task import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[date] = None
    category_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[date] = None
    category_id: Optional[int] = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[date]
    category_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

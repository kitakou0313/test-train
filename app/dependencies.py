from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.category_repository import CategoryRepository
from app.repositories.task_repository import TaskRepository
from app.services.category_service import CategoryService
from app.services.task_service import TaskService


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


def get_category_repository(db: Session = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)


def get_task_service(
    task_repo: TaskRepository = Depends(get_task_repository),
    category_repo: CategoryRepository = Depends(get_category_repository),
) -> TaskService:
    return TaskService(task_repo, category_repo)


def get_category_service(
    category_repo: CategoryRepository = Depends(get_category_repository),
    task_repo: TaskRepository = Depends(get_task_repository),
) -> CategoryService:
    return CategoryService(category_repo, task_repo)

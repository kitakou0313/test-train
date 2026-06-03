import re
from typing import Optional

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.repositories.task_repository import TaskRepository
from app.exceptions import (
    NotFoundError,
    CategoryInUseError,
    DuplicateNameError,
    InvalidColorError,
)

COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


class CategoryService:
    def __init__(self, category_repo: CategoryRepository, task_repo: TaskRepository):
        self.category_repo = category_repo
        self.task_repo = task_repo

    def get_categories(self) -> list[Category]:
        return self.category_repo.get_all()

    def get_category(self, category_id: int) -> Category:
        category = self.category_repo.get_by_id(category_id)
        if category is None:
            raise NotFoundError(f"カテゴリ ID={category_id} が見つかりません")
        return category

    def create_category(self, name: str, color: str = "#6c757d") -> Category:
        self._validate_color(color)
        if self.category_repo.get_by_name(name) is not None:
            raise DuplicateNameError(f"カテゴリ名「{name}」はすでに使用されています")
        return self.category_repo.create(name=name, color=color)

    def update_category(
        self,
        category_id: int,
        name: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Category:
        category = self.get_category(category_id)
        if color is not None:
            self._validate_color(color)
        if name is not None and name != category.name:
            if self.category_repo.get_by_name(name) is not None:
                raise DuplicateNameError(f"カテゴリ名「{name}」はすでに使用されています")
        return self.category_repo.update(category, name=name, color=color)

    def delete_category(self, category_id: int) -> None:
        category = self.get_category(category_id)
        in_progress_count = self.task_repo.count_in_progress_by_category(category_id)
        if in_progress_count > 0:
            raise CategoryInUseError(
                f"進行中のタスクが {in_progress_count} 件あるため、カテゴリを削除できません"
            )
        self.task_repo.nullify_category(category_id)
        self.category_repo.delete(category)

    def _validate_color(self, color: str) -> None:
        if not COLOR_PATTERN.match(color):
            raise InvalidColorError(
                "カラーコードは #RRGGBB 形式で入力してください（例: #ff0000）"
            )

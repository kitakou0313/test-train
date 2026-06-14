from typing import Optional

from app.domain.category import Category
from app.exceptions import CategoryInUseError, DuplicateNameError, NotFoundError
from app.repositories.category_repository import CategoryRepository
from app.repositories.task_repository import TaskRepository


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
        Category.validate_color(color)
        if self.category_repo.get_by_name(name) is not None:
            raise DuplicateNameError(f"カテゴリ名「{name}」はすでに使用されています")
        category = Category(id=0, name=name, color=color)
        return self.category_repo.create(category)

    def update_category(
        self,
        category_id: int,
        name: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Category:
        category = self.get_category(category_id)
        if color is not None:
            Category.validate_color(color)
        if name is not None and name != category.name:
            if self.category_repo.get_by_name(name) is not None:
                raise DuplicateNameError(f"カテゴリ名「{name}」はすでに使用されています")
        if name is not None:
            category.name = name
        if color is not None:
            category.color = color
        return self.category_repo.update(category)

    def delete_category(self, category_id: int) -> None:
        category = self.get_category(category_id)
        in_progress_count = self.task_repo.count_in_progress_by_category(category_id)
        if in_progress_count > 0:
            raise CategoryInUseError(
                f"進行中のタスクが {in_progress_count} 件あるため、カテゴリを削除できません"
            )
        self.task_repo.nullify_category(category_id)
        self.category_repo.delete(category)

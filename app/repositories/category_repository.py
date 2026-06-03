from typing import Optional
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Category]:
        return self.db.query(Category).order_by(Category.name).all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name == name).first()

    def create(self, name: str, color: str) -> Category:
        category = Category(name=name, color=color)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(
        self,
        category: Category,
        name: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Category:
        if name is not None:
            category.name = name
        if color is not None:
            category.color = color
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()

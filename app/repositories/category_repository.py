from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from app.database import Base
from app.domain.category import Category

if TYPE_CHECKING:
    from app.repositories.task_repository import TaskRecord


class CategoryRecord(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    color: Mapped[str] = mapped_column(String(7), nullable=False, default="#6c757d")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    tasks: Mapped[list["TaskRecord"]] = relationship("TaskRecord", back_populates="category")


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, record: CategoryRecord) -> Category:
        return Category(
            id=record.id,
            name=record.name,
            color=record.color,
            created_at=record.created_at,
        )

    def get_all(self) -> list[Category]:
        records = self.db.query(CategoryRecord).order_by(CategoryRecord.name).all()
        return [self._to_domain(r) for r in records]

    def get_by_id(self, category_id: int) -> Optional[Category]:
        record = (
            self.db.query(CategoryRecord).filter(CategoryRecord.id == category_id).first()
        )
        return self._to_domain(record) if record else None

    def get_by_name(self, name: str) -> Optional[Category]:
        record = (
            self.db.query(CategoryRecord).filter(CategoryRecord.name == name).first()
        )
        return self._to_domain(record) if record else None

    def create(self, category: Category) -> Category:
        record = CategoryRecord(name=category.name, color=category.color)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return self._to_domain(record)

    def update(self, category: Category) -> Category:
        record = (
            self.db.query(CategoryRecord).filter(CategoryRecord.id == category.id).first()
        )
        record.name = category.name
        record.color = category.color
        self.db.commit()
        self.db.refresh(record)
        return self._to_domain(record)

    def delete(self, category: Category) -> None:
        record = (
            self.db.query(CategoryRecord).filter(CategoryRecord.id == category.id).first()
        )
        self.db.delete(record)
        self.db.commit()

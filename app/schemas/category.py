import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


class CategoryCreate(BaseModel):
    name: str
    color: str = "#6c757d"

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str) -> str:
        if not COLOR_RE.match(v):
            raise ValueError("カラーコードは #RRGGBB 形式で入力してください")
        return v


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not COLOR_RE.match(v):
            raise ValueError("カラーコードは #RRGGBB 形式で入力してください")
        return v


class CategoryRead(BaseModel):
    id: int
    name: str
    color: str
    created_at: datetime

    model_config = {"from_attributes": True}

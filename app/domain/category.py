import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.exceptions import InvalidColorError

_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


@dataclass
class Category:
    id: int
    name: str
    color: str
    created_at: Optional[datetime] = None

    @staticmethod
    def validate_color(color: str) -> None:
        if not _COLOR_PATTERN.match(color):
            raise InvalidColorError(
                "カラーコードは #RRGGBB 形式で入力してください（例: #ff0000）"
            )

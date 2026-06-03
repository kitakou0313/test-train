from pathlib import Path

from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# テンプレートに共通で渡す定数
# env.globals ではなく各ルートのコンテキストに merge する
# （env.globals に dict を設定すると Jinja2 の LRU キャッシュキー生成で TypeError になるため）
TEMPLATE_GLOBALS: dict = {
    "STATUS_LABELS": {
        "todo": "未着手",
        "in_progress": "進行中",
        "done": "完了",
        "cancelled": "キャンセル",
    },
    "STATUS_COLORS": {
        "todo": "secondary",
        "in_progress": "primary",
        "done": "success",
        "cancelled": "dark",
    },
    "PRIORITY_LABELS": {
        "low": "低",
        "medium": "中",
        "high": "高",
    },
    "PRIORITY_COLORS": {
        "low": "secondary",
        "medium": "warning",
        "high": "danger",
    },
    "TRANSITION_LABELS": {
        "todo": "未着手に戻す",
        "in_progress": "開始する",
        "done": "完了にする",
        "cancelled": "キャンセルする",
    },
}


def render(request, template_name: str, context: dict):
    """共通定数をコンテキストにマージしてテンプレートレスポンスを返す"""
    merged = {**TEMPLATE_GLOBALS, **context}
    return templates.TemplateResponse(request, template_name, merged)

"""
CategoryService の Unit テスト

テスト対象: app.services.category_service.CategoryService

=== テストするビジネスルール ===

【1】カテゴリ名の一意性
  - 同じ名前のカテゴリを作成すると DuplicateNameError が発生する
  - 更新時に他のカテゴリと同名にしようとすると DuplicateNameError が発生する
  - 異なる名前なら作成・更新できる

【2】カラーコードのバリデーション
  - #RRGGBB 形式（例: #ff0000）以外は InvalidColorError が発生する
  - 有効な例: #000000, #ffffff, #a1b2c3
  - 無効な例: red, #fff, #GGGGGG, 空文字

【3】カテゴリ削除の制約
  - 進行中（in_progress）のタスクを持つカテゴリは CategoryInUseError で削除不可
  - todo・done・cancelled のタスクしか持たないカテゴリは削除できる
  - 削除されたカテゴリに紐づくタスクの category_id は None になる

=== 利用可能な fixture（tests/conftest.py より） ===

    db_session         : インメモリ SQLite セッション
    category_service   : CategoryService インスタンス
    task_service       : TaskService インスタンス（タスク作成時に使用）
    category_repository: CategoryRepository インスタンス
    task_repository    : TaskRepository インスタンス

=== 使用するクラス・例外 ===

    from app.models.task import TaskStatus
    from app.exceptions import (
        CategoryInUseError,
        DuplicateNameError,
        InvalidColorError,
        NotFoundError,
    )

=== サンプルテスト ===

    import pytest
    from app.exceptions import DuplicateNameError

    @pytest.mark.unit
    def test_duplicate_category_name_raises(category_service):
        category_service.create_category(name="仕事", color="#0d6efd")

        with pytest.raises(DuplicateNameError):
            category_service.create_category(name="仕事", color="#198754")
"""

import pytest

# TODO: ここにテストを実装してください
#
# ヒント: pytest.mark.unit デコレータを付けることで
#         `pytest -m unit` で Unit test だけを実行できます

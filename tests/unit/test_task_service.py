"""
TaskService の Unit テスト

テスト対象: app.services.task_service.TaskService

=== テストするビジネスルール ===

【1】ステータス遷移ルール
  許可される遷移:
    todo        → in_progress  （開始）
    todo        → cancelled    （キャンセル）
    in_progress → done         （完了）
    in_progress → todo         （一時中断）
    in_progress → cancelled    （キャンセル）
    done        → todo         （再オープン）
    cancelled   → todo         （再オープン）

  禁止される遷移（InvalidStatusTransitionError が発生すること）:
    done        → in_progress
    done        → cancelled
    cancelled   → in_progress
    cancelled   → done
    any         → 同じステータス

【2】期日バリデーション
  - 作成時: 過去の日付は InvalidDueDateError
  - 更新時: 過去の日付は InvalidDueDateError
  - 期日なし（None）は常に有効
  - ステータス遷移時: 既存の期日が過去でも遷移は成功する

【3】タスクフィルタリング
  - ステータスで絞り込み
  - カテゴリで絞り込み
  - キーワード検索（タイトル・説明）
  - 期限切れタスクの取得（done/cancelled は含まない）

=== 利用可能な fixture（tests/conftest.py より） ===

    db_session         : インメモリ SQLite セッション
    task_service       : TaskService インスタンス
    category_service   : CategoryService インスタンス（カテゴリ作成に使用）
    task_repository    : TaskRepository インスタンス
    category_repository: CategoryRepository インスタンス

=== 使用するクラス・例外 ===

    from app.models.task import TaskStatus, TaskPriority
    from app.exceptions import (
        InvalidStatusTransitionError,
        InvalidDueDateError,
        NotFoundError,
    )

=== サンプルテスト ===

    import pytest
    from datetime import date, timedelta
    from app.models.task import TaskStatus

    @pytest.mark.unit
    def test_start_task_from_todo(task_service):
        task = task_service.create_task(title="サンプルタスク")
        assert task.status == TaskStatus.todo

        updated = task_service.transition_status(task.id, TaskStatus.in_progress)
        assert updated.status == TaskStatus.in_progress
"""

import pytest
from app.models.task import TaskStatus
from app.exceptions import InvalidStatusTransitionError


def _make_in_progress(task_service, title="タスク"):
    task = task_service.create_task(title=title)
    return task_service.transition_status(task.id, TaskStatus.in_progress)


def _make_done(task_service, title="タスク"):
    task = _make_in_progress(task_service, title)
    return task_service.transition_status(task.id, TaskStatus.done)


def _make_cancelled(task_service, title="タスク"):
    task = task_service.create_task(title=title)
    return task_service.transition_status(task.id, TaskStatus.cancelled)


# todo → todo（不正: 同一ステータス）
@pytest.mark.unit
def test_transition_todo_to_todo_raises(task_service):
    task = task_service.create_task(title="遷移テスト")
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.todo)


# todo → in_progress（有効）
@pytest.mark.unit
def test_transition_todo_to_in_progress(task_service):
    task = task_service.create_task(title="遷移テスト")
    updated = task_service.transition_status(task.id, TaskStatus.in_progress)
    assert updated.status == TaskStatus.in_progress


# todo → done（不正）
@pytest.mark.unit
def test_transition_todo_to_done_raises(task_service):
    task = task_service.create_task(title="遷移テスト")
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.done)


# todo → cancelled（有効）
@pytest.mark.unit
def test_transition_todo_to_cancelled(task_service):
    task = task_service.create_task(title="遷移テスト")
    updated = task_service.transition_status(task.id, TaskStatus.cancelled)
    assert updated.status == TaskStatus.cancelled


# in_progress → todo（有効）
@pytest.mark.unit
def test_transition_in_progress_to_todo(task_service):
    task = _make_in_progress(task_service)
    updated = task_service.transition_status(task.id, TaskStatus.todo)
    assert updated.status == TaskStatus.todo


# in_progress → in_progress（不正: 同一ステータス）
@pytest.mark.unit
def test_transition_in_progress_to_in_progress_raises(task_service):
    task = _make_in_progress(task_service)
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.in_progress)


# in_progress → done（有効）
@pytest.mark.unit
def test_transition_in_progress_to_done(task_service):
    task = _make_in_progress(task_service)
    updated = task_service.transition_status(task.id, TaskStatus.done)
    assert updated.status == TaskStatus.done


# in_progress → cancelled（有効）
@pytest.mark.unit
def test_transition_in_progress_to_cancelled(task_service):
    task = _make_in_progress(task_service)
    updated = task_service.transition_status(task.id, TaskStatus.cancelled)
    assert updated.status == TaskStatus.cancelled


# done → todo（有効）
@pytest.mark.unit
def test_transition_done_to_todo(task_service):
    task = _make_done(task_service)
    updated = task_service.transition_status(task.id, TaskStatus.todo)
    assert updated.status == TaskStatus.todo


# done → in_progress（不正）
@pytest.mark.unit
def test_transition_done_to_in_progress_raises(task_service):
    task = task_service.create_task(title="遷移テスト")
    task_service.transition_status(task.id, TaskStatus.in_progress)
    task_service.transition_status(task.id, TaskStatus.done)

    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.in_progress)


# done → done（不正: 同一ステータス）
@pytest.mark.unit
def test_transition_done_to_done_raises(task_service):
    task = _make_done(task_service)
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.done)


# done → cancelled（不正）
@pytest.mark.unit
def test_transition_done_to_cancelled_raises(task_service):
    task = _make_done(task_service)
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.cancelled)


# cancelled → todo（有効）
@pytest.mark.unit
def test_transition_cancelled_to_todo(task_service):
    task = _make_cancelled(task_service)
    updated = task_service.transition_status(task.id, TaskStatus.todo)
    assert updated.status == TaskStatus.todo


# cancelled → in_progress（不正）
@pytest.mark.unit
def test_transition_cancelled_to_in_progress_raises(task_service):
    task = _make_cancelled(task_service)
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.in_progress)


# cancelled → done（不正）
@pytest.mark.unit
def test_transition_cancelled_to_done_raises(task_service):
    task = _make_cancelled(task_service)
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.done)


# cancelled → cancelled（不正: 同一ステータス）
@pytest.mark.unit
def test_transition_cancelled_to_cancelled_raises(task_service):
    task = _make_cancelled(task_service)
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.cancelled)

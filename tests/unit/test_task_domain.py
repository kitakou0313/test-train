"""
TaskService の Unit テスト

テスト対象: app.services.task_service.TaskService
"""

import pytest
from app.domain.task import TaskStatus, Task, TaskPriority
from app.exceptions import InvalidStatusTransitionError, InvalidDueDateError
from freezegun import freeze_time
from datetime import datetime, date

def _create_task_todo(): 
    task = Task(id=1, title="遷移テスト", status=TaskStatus.todo, priority=TaskPriority.medium)
    return task    
def _create_task_in_progress(): 
    task = Task(id=1, title="遷移テスト", status=TaskStatus.in_progress, priority=TaskPriority.medium)
    return task
def _create_task_done(): 
    task = Task(id=1, title="遷移テスト", status=TaskStatus.done, priority=TaskPriority.medium)
    return task
def _create_task_cancelled(): 
    task = Task(id=1, title="遷移テスト", status=TaskStatus.cancelled, priority=TaskPriority.medium)
    return task

# todo → todo（不正: 同一ステータス）
@pytest.mark.unit
def test_transition_todo_to_todo_raises():
    task = _create_task_todo()
    
    with pytest.raises(InvalidStatusTransitionError):
        task.transition_to(TaskStatus.todo)

# todo → in_progress（有効）
@pytest.mark.unit
def test_transition_todo_to_in_progress():
    task = _create_task_todo()

    task.transition_to(TaskStatus.in_progress)

    assert task.status == TaskStatus.in_progress


# todo → done（不正）
@pytest.mark.unit
def test_transition_todo_to_done_raises():
    task = _create_task_todo()    

    with pytest.raises(InvalidStatusTransitionError):
        task.transition_to(TaskStatus.done)


# todo → cancelled（有効）
@pytest.mark.unit
def test_transition_todo_to_cancelled():
    task = _create_task_todo()
    
    task.transition_to(TaskStatus.cancelled)

    assert task.status == TaskStatus.cancelled

# in_progress → todo（有効）
@pytest.mark.unit
def test_transition_in_progress_to_todo():
    task = _create_task_in_progress()
    
    task.transition_to(TaskStatus.todo)

    assert task.status == TaskStatus.todo


# in_progress → in_progress（不正: 同一ステータス）
@pytest.mark.unit
def test_transition_in_progress_to_in_progress_raises():
    task = _create_task_in_progress()

    with pytest.raises(InvalidStatusTransitionError):
        task.transition_to(TaskStatus.in_progress)


# in_progress → done（有効）
@pytest.mark.unit
def test_transition_in_progress_to_done():
    task = _create_task_in_progress()

    task.transition_to(TaskStatus.done)

    assert task.status == TaskStatus.done


# in_progress → cancelled（有効）
@pytest.mark.unit
def test_transition_in_progress_to_cancelled():
    task = _create_task_in_progress()
    
    task.transition_to(TaskStatus.cancelled)
    
    assert task.status == TaskStatus.cancelled
    


# done → todo（有効）
@pytest.mark.unit
def test_transition_done_to_todo():
    task = _create_task_done()
    
    task.transition_to(TaskStatus.todo)

    assert task.status == TaskStatus.todo


# done → in_progress（不正）
@pytest.mark.unit
def test_transition_done_to_in_progress_raises():
    task = _create_task_done()

    with pytest.raises(InvalidStatusTransitionError):
        task.transition_to(TaskStatus.in_progress)

# done → done（不正: 同一ステータス）
@pytest.mark.unit
def test_transition_done_to_done_raises():
    task = _create_task_done()

    with pytest.raises(InvalidStatusTransitionError):
        task.transition_to(TaskStatus.done)

# done → cancelled（不正）
@pytest.mark.unit
def test_transition_done_to_cancelled_raises():
    task = _create_task_done()

    with pytest.raises(InvalidStatusTransitionError):
        task.transition_to(TaskStatus.cancelled)

# cancelled → todo（有効）
@pytest.mark.unit
def test_transition_cancelled_to_todo():
    task = _create_task_cancelled()
    
    task.transition_to(TaskStatus.todo)
    
    assert task.status == TaskStatus.todo


# cancelled → in_progress（不正）
@pytest.mark.unit
def test_transition_cancelled_to_in_progress_raises():
    task = _create_task_cancelled()
    
    with pytest.raises(InvalidStatusTransitionError):
        task.transition_to(TaskStatus.in_progress)

# cancelled → done（不正）
@pytest.mark.unit
def test_transition_cancelled_to_done_raises():
    task = _create_task_cancelled()

    with pytest.raises(InvalidStatusTransitionError):
        task.transition_to(TaskStatus.done)

# cancelled → cancelled（不正: 同一ステータス）
@pytest.mark.unit
def test_transition_cancelled_to_cancelled_raises():
    task = _create_task_cancelled()

    with pytest.raises(InvalidStatusTransitionError):
        task.transition_to(TaskStatus.cancelled)


# 期日の設定テスト

# Noneの時
@pytest.mark.unit
def test_set_due_date_none():
    task = _create_task_todo()

    task.set_due_date(None)

    assert task.due_date == None

# 作成時の1日前
@pytest.mark.unit
@freeze_time("2026-06-10 10:00:00")
def test_set_due_date_before_creation_day():
    task = _create_task_todo()
    target_date = date(2026, 6, 9)

    with pytest.raises(InvalidDueDateError):
        task.set_due_date(target_date)

# 作成時の当日
@pytest.mark.unit
@freeze_time("2026-06-10 10:00:00")
def test_set_due_date_on_creation_day():
    task = _create_task_todo()
    target_date = date(2026, 6, 10)

    task.set_due_date(target_date)

    assert target_date == target_date

# 作成時の1日後
@pytest.mark.unit
@freeze_time("2026-06-10 10:00:00")
def test_set_due_date_after_creation_day():
    task = _create_task_todo()
    target_date = date(2026, 6, 11)

    task.set_due_date(target_date)

    assert task.due_date == target_date
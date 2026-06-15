"""
TaskService の Unit テスト

テスト対象: app.services.task_service.TaskService
"""

import pytest
from app.domain.task import TaskStatus, Task, TaskPriority
from app.exceptions import InvalidStatusTransitionError

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
def test_transition_todo_to_todo_raises(task_service):
    task = _create_task_todo()
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.todo)


# todo → in_progress（有効）
@pytest.mark.unit
def test_transition_todo_to_in_progress(task_service):
    task = _create_task_todo()
    updated = task_service.transition_status(task.id, TaskStatus.in_progress)
    assert updated.status == TaskStatus.in_progress


# todo → done（不正）
@pytest.mark.unit
def test_transition_todo_to_done_raises(task_service):
    task = _create_task_todo()
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.done)


# todo → cancelled（有効）
@pytest.mark.unit
def test_transition_todo_to_cancelled(task_service):
    task = _create_task_todo()
    updated = task_service.transition_status(task.id, TaskStatus.cancelled)
    assert updated.status == TaskStatus.cancelled


# in_progress → todo（有効）
@pytest.mark.unit
def test_transition_in_progress_to_todo(task_service):
    task = _create_task_in_progress()
    updated = task_service.transition_status(task.id, TaskStatus.todo)
    assert updated.status == TaskStatus.todo


# in_progress → in_progress（不正: 同一ステータス）
@pytest.mark.unit
def test_transition_in_progress_to_in_progress_raises(task_service):
    task = _create_task_in_progress()
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.in_progress)


# in_progress → done（有効）
@pytest.mark.unit
def test_transition_in_progress_to_done(task_service):
    task = _create_task_in_progress()
    updated = task_service.transition_status(task.id, TaskStatus.done)
    assert updated.status == TaskStatus.done


# in_progress → cancelled（有効）
@pytest.mark.unit
def test_transition_in_progress_to_cancelled(task_service):
    task = _create_task_in_progress()
    updated = task_service.transition_status(task.id, TaskStatus.cancelled)
    assert updated.status == TaskStatus.cancelled


# done → todo（有効）
@pytest.mark.unit
def test_transition_done_to_todo(task_service):
    task = _create_task_done()
    updated = task_service.transition_status(task.id, TaskStatus.todo)
    assert updated.status == TaskStatus.todo


# done → in_progress（不正）
@pytest.mark.unit
def test_transition_done_to_in_progress_raises(task_service):
    task = _create_task_done()
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.in_progress)


# done → done（不正: 同一ステータス）
@pytest.mark.unit
def test_transition_done_to_done_raises(task_service):
    task = _create_task_done()
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.done)


# done → cancelled（不正）
@pytest.mark.unit
def test_transition_done_to_cancelled_raises(task_service):
    task = _create_task_done()
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.cancelled)


# cancelled → todo（有効）
@pytest.mark.unit
def test_transition_cancelled_to_todo(task_service):
    task = _create_task_cancelled()
    updated = task_service.transition_status(task.id, TaskStatus.todo)
    assert updated.status == TaskStatus.todo


# cancelled → in_progress（不正）
@pytest.mark.unit
def test_transition_cancelled_to_in_progress_raises(task_service):
    task = _create_task_cancelled()
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.in_progress)


# cancelled → done（不正）
@pytest.mark.unit
def test_transition_cancelled_to_done_raises(task_service):
    task = _create_task_cancelled()
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.done)


# cancelled → cancelled（不正: 同一ステータス）
@pytest.mark.unit
def test_transition_cancelled_to_cancelled_raises(task_service):
    task = _create_task_cancelled()
    with pytest.raises(InvalidStatusTransitionError):
        task_service.transition_status(task.id, TaskStatus.cancelled)

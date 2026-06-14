from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from app.dependencies import get_category_service, get_task_service
from app.exceptions import AppError, NotFoundError
from app.domain.task import TaskPriority, TaskStatus
from app.services.category_service import CategoryService
from app.services.task_service import TaskService
from app.templates_config import render

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _pop_flash(request: Request) -> Optional[dict]:
    return request.session.pop("flash", None)


def _set_flash(request: Request, type_: str, message: str) -> None:
    request.session["flash"] = {"type": type_, "message": message}


@router.get("")
def list_tasks(
    request: Request,
    status: Optional[str] = None,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    service: TaskService = Depends(get_task_service),
    category_service: CategoryService = Depends(get_category_service),
):
    status_enum = TaskStatus(status) if status else None
    tasks = service.get_tasks(
        status=status_enum, category_id=category_id, search=search
    )
    categories = category_service.get_categories()
    return render(request, "tasks/list.html", {
        "tasks": tasks,
        "categories": categories,
        "flash": _pop_flash(request),
        "filter_status": status,
        "filter_category_id": category_id,
        "filter_search": search,
        "today": date.today(),
    })


@router.get("/new")
def new_task_form(
    request: Request,
    category_service: CategoryService = Depends(get_category_service),
):
    return render(request, "tasks/create.html", {
        "categories": category_service.get_categories(),
        "flash": _pop_flash(request),
    })


@router.post("")
def create_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("medium"),
    due_date: str = Form(""),
    category_id: str = Form(""),
    service: TaskService = Depends(get_task_service),
):
    due_date_parsed = date.fromisoformat(due_date) if due_date else None
    category_id_int = int(category_id) if category_id else None
    try:
        task = service.create_task(
            title=title,
            description=description or None,
            priority=TaskPriority(priority),
            due_date=due_date_parsed,
            category_id=category_id_int,
        )
        return RedirectResponse(url=f"/tasks/{task.id}", status_code=303)
    except AppError as e:
        _set_flash(request, "danger", str(e))
        return RedirectResponse(url="/tasks/new", status_code=303)


@router.get("/{task_id}")
def task_detail(
    task_id: int,
    request: Request,
    service: TaskService = Depends(get_task_service),
):
    try:
        task = service.get_task(task_id)
    except NotFoundError:
        _set_flash(request, "danger", f"タスク ID={task_id} が見つかりません")
        return RedirectResponse(url="/tasks", status_code=303)

    allowed_transitions = sorted(
        service.get_allowed_transitions(task), key=lambda s: s.value
    )
    return render(request, "tasks/detail.html", {
        "task": task,
        "allowed_transitions": allowed_transitions,
        "flash": _pop_flash(request),
        "today": date.today(),
    })


@router.get("/{task_id}/edit")
def edit_task_form(
    task_id: int,
    request: Request,
    service: TaskService = Depends(get_task_service),
    category_service: CategoryService = Depends(get_category_service),
):
    try:
        task = service.get_task(task_id)
    except NotFoundError:
        _set_flash(request, "danger", f"タスク ID={task_id} が見つかりません")
        return RedirectResponse(url="/tasks", status_code=303)

    return render(request, "tasks/edit.html", {
        "task": task,
        "categories": category_service.get_categories(),
        "flash": _pop_flash(request),
    })


@router.post("/{task_id}")
def update_task(
    task_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("medium"),
    due_date: str = Form(""),
    category_id: str = Form(""),
    service: TaskService = Depends(get_task_service),
):
    due_date_parsed = date.fromisoformat(due_date) if due_date else None
    category_id_int = int(category_id) if category_id else None
    try:
        service.update_task(
            task_id=task_id,
            title=title,
            description=description or None,
            priority=TaskPriority(priority),
            due_date=due_date_parsed,
            category_id=category_id_int,
        )
        return RedirectResponse(url=f"/tasks/{task_id}", status_code=303)
    except AppError as e:
        _set_flash(request, "danger", str(e))
        return RedirectResponse(url=f"/tasks/{task_id}/edit", status_code=303)


@router.post("/{task_id}/status")
def transition_status(
    task_id: int,
    request: Request,
    new_status: str = Form(...),
    service: TaskService = Depends(get_task_service),
):
    try:
        service.transition_status(task_id, TaskStatus(new_status))
    except AppError as e:
        _set_flash(request, "danger", str(e))
    return RedirectResponse(url=f"/tasks/{task_id}", status_code=303)


@router.post("/{task_id}/delete")
def delete_task(
    task_id: int,
    request: Request,
    service: TaskService = Depends(get_task_service),
):
    try:
        service.delete_task(task_id)
        _set_flash(request, "success", "タスクを削除しました")
    except AppError as e:
        _set_flash(request, "danger", str(e))
    return RedirectResponse(url="/tasks", status_code=303)

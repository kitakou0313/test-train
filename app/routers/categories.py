from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from app.dependencies import get_category_service
from app.exceptions import AppError, NotFoundError
from app.services.category_service import CategoryService
from app.templates_config import render

router = APIRouter(prefix="/categories", tags=["categories"])


def _pop_flash(request: Request) -> Optional[dict]:
    return request.session.pop("flash", None)


def _set_flash(request: Request, type_: str, message: str) -> None:
    request.session["flash"] = {"type": type_, "message": message}


@router.get("")
def list_categories(
    request: Request,
    service: CategoryService = Depends(get_category_service),
):
    return render(request, "categories/list.html", {
        "categories": service.get_categories(),
        "flash": _pop_flash(request),
    })


@router.get("/new")
def new_category_form(request: Request):
    return render(request, "categories/create.html", {
        "flash": _pop_flash(request),
    })


@router.post("")
def create_category(
    request: Request,
    name: str = Form(...),
    color: str = Form("#6c757d"),
    service: CategoryService = Depends(get_category_service),
):
    try:
        service.create_category(name=name, color=color)
        _set_flash(request, "success", f"カテゴリ「{name}」を作成しました")
        return RedirectResponse(url="/categories", status_code=303)
    except AppError as e:
        _set_flash(request, "danger", str(e))
        return RedirectResponse(url="/categories/new", status_code=303)


@router.get("/{category_id}/edit")
def edit_category_form(
    category_id: int,
    request: Request,
    service: CategoryService = Depends(get_category_service),
):
    try:
        category = service.get_category(category_id)
    except NotFoundError:
        _set_flash(request, "danger", f"カテゴリ ID={category_id} が見つかりません")
        return RedirectResponse(url="/categories", status_code=303)

    return render(request, "categories/edit.html", {
        "category": category,
        "flash": _pop_flash(request),
    })


@router.post("/{category_id}")
def update_category(
    category_id: int,
    request: Request,
    name: str = Form(...),
    color: str = Form(...),
    service: CategoryService = Depends(get_category_service),
):
    try:
        service.update_category(category_id, name=name, color=color)
        _set_flash(request, "success", "カテゴリを更新しました")
        return RedirectResponse(url="/categories", status_code=303)
    except AppError as e:
        _set_flash(request, "danger", str(e))
        return RedirectResponse(url=f"/categories/{category_id}/edit", status_code=303)


@router.post("/{category_id}/delete")
def delete_category(
    category_id: int,
    request: Request,
    service: CategoryService = Depends(get_category_service),
):
    try:
        service.delete_category(category_id)
        _set_flash(request, "success", "カテゴリを削除しました")
    except AppError as e:
        _set_flash(request, "danger", str(e))
    return RedirectResponse(url="/categories", status_code=303)

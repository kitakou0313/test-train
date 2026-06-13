from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.database import Base, engine
from app.dependencies import get_category_service, get_task_service
from app.routers import categories, tasks
from app.services.category_service import CategoryService
from app.services.task_service import TaskService
from app.templates_config import render

BASE_DIR = Path(__file__).parent


class CacheControlStaticFiles(StaticFiles):
    def file_response(self, full_path, stat_result, scope, status_code=200):
        response = super().file_response(full_path, stat_result, scope, status_code)
        if response.status_code == 200:
            response.headers["Cache-Control"] = "public, max-age=86400, must-revalidate"
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="タスク管理アプリ", lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.mount("/static", CacheControlStaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(tasks.router)
app.include_router(categories.router)


@app.get("/")
def dashboard(
    request: Request,
    service: TaskService = Depends(get_task_service),
):
    counts = service.count_by_status()
    overdue = service.get_overdue_tasks()
    return render(request, "index.html", {
        "counts": counts,
        "overdue_count": len(overdue),
        "today": date.today(),
    })


@app.get("/api/tasks/overdue")
def api_overdue_tasks(service: TaskService = Depends(get_task_service)):
    overdue = service.get_overdue_tasks()
    return {
        "count": len(overdue),
        "tasks": [
            {"id": t.id, "title": t.title, "due_date": str(t.due_date)}
            for t in overdue
        ],
    }

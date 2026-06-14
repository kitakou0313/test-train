# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI task management app used as a sandbox for exploring various testing techniques (unit tests, e2e with Playwright, performance testing). The codebase follows DDD (Domain-Driven Design) principles.

## Setup

```bash
pip install -r requirements-dev.txt
playwright install chromium --with-deps
```

## Running the App

```bash
python scripts/seed.py          # seed initial data (first time only)
uvicorn app.main:app --reload --port 8000
```

## Tests

```bash
pytest -m unit       # unit tests only (no browser, no server)
pytest -m e2e        # e2e tests only (Playwright, requires no server pre-running)
pytest               # all tests
pytest tests/unit/test_task_service.py::test_transition_todo_to_in_progress  # single test
```

## Architecture

The app uses a strict layered DDD structure:

```
app/domain/       ← Pure Python dataclasses with business logic (no DB dependency)
app/repositories/ ← SQLAlchemy ORM models + data access; maps ORM records → domain objects
app/services/     ← Application services; orchestrate domain + repository calls
app/routers/      ← FastAPI route handlers; delegate to services, handle HTTP concerns
app/dependencies.py ← FastAPI DI wiring (constructs repos and services per request)
```

**Domain layer** (`app/domain/task.py`, `app/domain/category.py`): Domain objects are plain dataclasses. Business rules live here — status transition validation (`_ALLOWED_TRANSITIONS`), due date validation, color format validation. Raises custom exceptions from `app/exceptions.py`.

**Repository layer**: Each repository file contains both the SQLAlchemy ORM model (`TaskRecord`, `CategoryRecord`) and the repository class. The `_to_domain()` method converts ORM records to domain dataclasses, keeping the domain layer free of SQLAlchemy.

**Service layer**: Services receive repositories via constructor injection. `TaskService` depends on both `TaskRepository` and `CategoryRepository` (cross-entity validation). Domain logic is invoked here before calling the repository.

**Router layer**: Routers use session-based flash messages for user feedback (`_set_flash` / `_pop_flash`). HTML form submissions use POST-redirect-GET pattern to avoid duplicate submissions.

## Testing Architecture

**Unit tests** (`tests/unit/`, marker: `@pytest.mark.unit`):
- Use in-memory SQLite via fixtures in `tests/conftest.py`
- Each test gets a fresh `db_session` that auto-rolls back after the test
- Test the service layer directly; no HTTP, no browser
- Available fixtures: `db_session`, `task_repository`, `category_repository`, `task_service`, `category_service`

**E2e tests** (`tests/e2e/`, marker: `@pytest.mark.e2e`):
- Start a real uvicorn server on port 8001 (scope=session, started once per test run)
- Use a real SQLite file `test_e2e.sqlite3` (not in-memory)
- `seed_data` fixture resets and repopulates the DB before each test
- Use Playwright `page` fixture for browser interaction
- Server overrides `get_db` dependency to point at the test DB

## Key Domain Rules

**Task status transitions** (defined in `app/domain/task.py`):
- `todo` → `in_progress`, `cancelled`
- `in_progress` → `done`, `todo`, `cancelled`
- `done` → `todo`
- `cancelled` → `todo`
- Same-status transitions raise `InvalidStatusTransitionError`

**Exceptions** (all in `app/exceptions.py`): `NotFoundError`, `InvalidStatusTransitionError`, `InvalidDueDateError`, `CategoryInUseError`, `DuplicateNameError`, `InvalidColorError` — all extend `AppError`.

"""
e2e テスト用の shared fixture

このファイルが提供するものを使うことで、ブラウザを使った
エンドツーエンドテストを書くことができます。

利用可能な fixture:
    live_server : バックグラウンドで起動した FastAPI サーバーの URL（str）
                  テストセッション中は起動し続け、終了時に自動停止します。
    seed_data   : テストデータ（カテゴリ3件・タスク5件）をDBに投入します。
                  テストごとにDBをリセットして再投入するため、テスト間の干渉がありません。
    page        : pytest-playwright が提供する Page フィクスチャ（ブラウザページ）
                  live_server フィクスチャを合わせて使います。

使い方:
    @pytest.mark.e2e
    def test_view_task_list(page, live_server):
        page.goto(f"{live_server}/tasks")
        expect(page.locator("[data-testid='task-table']")).to_be_visible()

=== シードデータの内容（seed_data fixture 使用時） ===

カテゴリ:
    - "仕事"     (color=#0d6efd)
    - "個人"     (color=#198754)
    - "学習"     (color=#ffc107)

タスク:
    - "プロジェクト資料作成"  status=todo,        priority=high,   category=仕事
    - "週次レポート"         status=in_progress, priority=medium, category=仕事, due_date=今日+2日
    - "ジム"                status=todo,        priority=low,    category=個人
    - "Pytestドキュメント読む" status=done,        priority=high,   category=学習
    - "期限切れタスク"        status=todo,        priority=medium, due_date=昨日（期限切れ）

=== Playwright の主要 API ===

    page.goto(url)                   : ページに移動
    page.fill(selector, text)        : テキストフィールドに入力
    page.click(selector)             : 要素をクリック
    page.select_option(selector, value): セレクトボックスを選択
    page.locator(selector)           : 要素を取得（遅延評価）
    expect(locator).to_be_visible()  : 要素が表示されていることを確認
    expect(locator).to_have_text()   : テキストが一致することを確認
    page.wait_for_url(url_pattern)   : URLの変化を待つ
"""

import threading
import time
from datetime import date, timedelta
from typing import Generator

import httpx
import pytest
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "sqlite:///./test_e2e.sqlite3"
TEST_PORT = 8001

_test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
_TestingSessionLocal = sessionmaker(bind=_test_engine)


@pytest.fixture(scope="session")
def live_server() -> Generator[str, None, None]:
    """
    テスト用の FastAPI サーバーをバックグラウンドスレッドで起動する。

    - テストセッション全体で1回だけ起動（scope="session"）
    - テスト用DBを使うために get_db 依存性をオーバーライドする
    - サーバーURL（http://127.0.0.1:8001）を返す
    """
    from app.database import Base, get_db
    from app.main import app

    # テスト用DBのテーブルを作成
    Base.metadata.create_all(bind=_test_engine)

    # get_db をテスト用DBセッションに差し替える
    def override_get_db():
        db = _TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # uvicorn をバックグラウンドスレッドで起動
    config = uvicorn.Config(app, host="127.0.0.1", port=TEST_PORT, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # サーバーが起動するまで待機
    base_url = f"http://127.0.0.1:{TEST_PORT}"
    for _ in range(50):
        try:
            httpx.get(base_url, timeout=1.0)
            break
        except Exception:
            time.sleep(0.1)

    yield base_url

    # テスト終了後にサーバーを停止
    server.should_exit = True
    _test_engine.dispose()


@pytest.fixture
def seed_data(live_server: str):
    """
    テスト用のサンプルデータをDBに投入する。

    テストごとにDBをリセットして再投入するため、
    各テストは同じ初期状態から実行される。
    """
    from app.models.category import Category
    from app.models.task import Task, TaskPriority, TaskStatus

    db = _TestingSessionLocal()
    try:
        # テーブルをリセット
        db.query(Task).delete()
        db.query(Category).delete()
        db.commit()

        # カテゴリを作成
        work = Category(name="仕事", color="#0d6efd")
        personal = Category(name="個人", color="#198754")
        learning = Category(name="学習", color="#ffc107")
        db.add_all([work, personal, learning])
        db.commit()

        # タスクを作成
        today = date.today()
        db.add_all([
            Task(
                title="プロジェクト資料作成",
                status=TaskStatus.todo,
                priority=TaskPriority.high,
                category_id=work.id,
            ),
            Task(
                title="週次レポート",
                status=TaskStatus.in_progress,
                priority=TaskPriority.medium,
                category_id=work.id,
                due_date=today + timedelta(days=2),
            ),
            Task(
                title="ジム",
                status=TaskStatus.todo,
                priority=TaskPriority.low,
                category_id=personal.id,
            ),
            Task(
                title="Pytestドキュメント読む",
                status=TaskStatus.done,
                priority=TaskPriority.high,
                category_id=learning.id,
            ),
            Task(
                title="期限切れタスク",
                status=TaskStatus.todo,
                priority=TaskPriority.medium,
                due_date=today - timedelta(days=1),
            ),
        ])
        db.commit()
    finally:
        db.close()

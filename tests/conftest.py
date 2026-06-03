"""
Unit test 用の共有 fixture

このファイルが提供するものを使うことで、テストからDBの詳細を
意識せずにサービス層のテストを書くことができます。

利用可能な fixture:
    db_session         : インメモリSQLiteの Session（テスト後に自動ロールバック）
    task_repository    : TaskRepository インスタンス
    category_repository: CategoryRepository インスタンス
    task_service       : TaskService インスタンス（task_repo + category_repo 注入済み）
    category_service   : CategoryService インスタンス（category_repo + task_repo 注入済み）

使い方:
    def test_something(task_service, db_session):
        task = task_service.create_task(title="テスト")
        assert task.id is not None
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.repositories.category_repository import CategoryRepository
from app.repositories.task_repository import TaskRepository
from app.services.category_service import CategoryService
from app.services.task_service import TaskService


@pytest.fixture(scope="function")
def db_engine():
    """テスト用のインメモリ SQLite エンジンを作成する。テスト終了後にテーブルを削除する。"""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """テスト用のDBセッション。テスト終了後にロールバックしてクリーンな状態に戻す。"""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def task_repository(db_session):
    """TaskRepository インスタンス（テスト用DBに接続済み）"""
    return TaskRepository(db_session)


@pytest.fixture
def category_repository(db_session):
    """CategoryRepository インスタンス（テスト用DBに接続済み）"""
    return CategoryRepository(db_session)


@pytest.fixture
def task_service(task_repository, category_repository):
    """TaskService インスタンス（依存性注入済み）

    このサービスが Unit test の主要なテスト対象です。
    ビジネスルール（ステータス遷移、期日バリデーションなど）のテストに使います。
    """
    return TaskService(task_repository, category_repository)


@pytest.fixture
def category_service(category_repository, task_repository):
    """CategoryService インスタンス（依存性注入済み）"""
    return CategoryService(category_repository, task_repository)

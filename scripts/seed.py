"""
開発用シードデータ投入スクリプト

使い方:
    python scripts/seed.py

実行後、http://localhost:8000 でアプリを起動するとサンプルデータが確認できます。
"""

import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.category import Category
from app.models.task import Task, TaskPriority, TaskStatus

DATABASE_URL = "sqlite:///./taskdb.sqlite3"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

db = Session()

try:
    # 既存データをクリア
    db.query(Task).delete()
    db.query(Category).delete()
    db.commit()

    # カテゴリを作成
    work = Category(name="仕事", color="#0d6efd")
    personal = Category(name="個人", color="#198754")
    learning = Category(name="学習", color="#ffc107")
    other = Category(name="その他", color="#6c757d")
    db.add_all([work, personal, learning, other])
    db.commit()

    today = date.today()

    tasks = [
        Task(
            title="プロジェクト計画書を作成する",
            description="Q3のロードマップを含める",
            status=TaskStatus.todo,
            priority=TaskPriority.high,
            category_id=work.id,
            due_date=today + timedelta(days=3),
        ),
        Task(
            title="週次レポートの提出",
            description="先週の進捗と今週の予定を記入",
            status=TaskStatus.in_progress,
            priority=TaskPriority.medium,
            category_id=work.id,
            due_date=today + timedelta(days=1),
        ),
        Task(
            title="コードレビュー",
            status=TaskStatus.todo,
            priority=TaskPriority.high,
            category_id=work.id,
        ),
        Task(
            title="ジムに行く",
            status=TaskStatus.todo,
            priority=TaskPriority.low,
            category_id=personal.id,
        ),
        Task(
            title="歯医者の予約",
            status=TaskStatus.done,
            priority=TaskPriority.medium,
            category_id=personal.id,
        ),
        Task(
            title="Pytestのドキュメントを読む",
            description="フィクスチャとパラメトライズを重点的に",
            status=TaskStatus.done,
            priority=TaskPriority.high,
            category_id=learning.id,
        ),
        Task(
            title="Playwright入門",
            description="公式チュートリアルを最後までやる",
            status=TaskStatus.in_progress,
            priority=TaskPriority.high,
            category_id=learning.id,
            due_date=today + timedelta(days=7),
        ),
        Task(
            title="期限切れタスク（サンプル）",
            description="これは期限切れタスクのサンプルです",
            status=TaskStatus.todo,
            priority=TaskPriority.medium,
            due_date=today - timedelta(days=2),
        ),
        Task(
            title="キャンセルされたタスク",
            status=TaskStatus.cancelled,
            priority=TaskPriority.low,
            category_id=other.id,
        ),
    ]

    db.add_all(tasks)
    db.commit()

    print(f"✓ カテゴリ {db.query(Category).count()} 件")
    print(f"✓ タスク   {db.query(Task).count()} 件")
    print("シードデータの投入が完了しました。")

except Exception as e:
    db.rollback()
    print(f"エラーが発生しました: {e}", file=sys.stderr)
    sys.exit(1)

finally:
    db.close()

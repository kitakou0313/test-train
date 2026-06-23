import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_task_detail_page_content_without_due_date(page: Page, live_server: str, seed_data):
    # task詳細ページへ遷移
    page.goto(f"{live_server}/tasks/1")

    # 検証

    # 表示内容の検証
    # タイトル
    expect(page.locator("[data-testid='task-title']")).to_have_text("プロジェクト資料作成")
    # 説明
    expect(page.locator('[data-testid="task-description"]')).to_have_text("プロジェクトのキックオフのための資料を作成")
    # ステータス
    expect(page.locator('[data-testid="task-status-badge"]')).to_have_text("未着手")
    # 優先度
    expect(page.locator('[data-testid="task-priority"]')).to_have_text("高")
    # 期日
    expect(page.locator('[data-testid="task-due-date"]')).to_have_text("未設定")
    # カテゴリ名
    expect(page.locator('[data-testid="task-category"]')).to_have_text("なし")
    # 作成日時
    expect(page.locator('[data-testid="task-created-at"]')).to_have_text("2026/06/10 10:00")
    # 更新日時
    expect(page.locator('[data-testid="task-updated-at"]')).to_have_text("2026/06/10 10:00")
    # ステータス遷移ボタン
    expect(page.locator('[data-testid="btn-edit-task"]'))
    # 編集・削除ボタン
    expect(page.locator('[data-testid="btn-edit-task"]')).to_have_count(1)
    expect(page.locator('[data-testid="btn-delete-task"]')).to_have_count(1)

@pytest.mark.e2e
def test_task_detail_page_content_with_due_date(page: Page, live_server: str, seed_data):
    # task詳細ページへ遷移
    page.goto(f"{live_server}/tasks/2")

    # 検証

    # 表示内容の検証
    # 期日
    expect(page.locator('[data-testid="task-due-date"]')).to_have_text("2026/06/12 00:00")


import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_task_detail_page_content(page: Page, live_server: str, seed_data):

    # task詳細ページへ遷移
    page.goto(f"{live_server}/tasks/1")

    # 検証
    expect(page.locator("[data-testid='task-title']")).to_have_text("プロジェクト資料作成")
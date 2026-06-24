import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_todo_to_in_progress(page: Page, live_server: str, seed_data):
    # テストの前準備
    page.goto(f"{live_server}/tasks/1")

    # 検証
    # 有効な遷移が可能か

def test_status_transition_list_in_todo_task(page: Page, live_server: str, seed_data):
    # テストの前準備
    page.goto(f"{live_server}/tasks/1")

    # 検証
    # 不可能な遷移が表示されていないか
    expect(page.locator('[data-testid="btn-transition-todo"]')).to_have_count(0)
    expect(page.locator('[data-testid="btn-transition-in_progress"]')).to_have_count(1)
    expect(page.locator('[data-testid="btn-transition-done"]')).to_have_count(1)
    expect(page.locator('[data-testid="btn-transition-cancelled"]')).to_have_count(1)


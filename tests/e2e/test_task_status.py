import pytest
from playwright.sync_api import Page, expect


# ========================================================
# ボタン表示テスト（遷移先の表示/非表示確認）
# ========================================================

@pytest.mark.e2e
class TestTransitionButtonVisibility:
    """各ステータスで表示される/されないボタンを検証する"""

    # --- todo ---

    def test_todo_shows_valid_transition_buttons(self, page: Page, live_server: str, seed_data):
        """todo状態では in_progress・done・cancelled ボタンが表示される"""
        page.goto(f"{live_server}/tasks/1")  # Task 1: status=todo

        expect(page.locator('[data-testid="btn-transition-in_progress"]')).to_have_count(1)
        expect(page.locator('[data-testid="btn-transition-done"]')).to_have_count(1)
        expect(page.locator('[data-testid="btn-transition-cancelled"]')).to_have_count(1)

    def test_todo_hides_invalid_transition_buttons(self, page: Page, live_server: str, seed_data):
        """todo状態では todo ボタンが表示されない"""
        page.goto(f"{live_server}/tasks/1")  # Task 1: status=todo

        expect(page.locator('[data-testid="btn-transition-todo"]')).to_have_count(0)

    # --- in_progress ---

    def test_in_progress_shows_valid_transition_buttons(self, page: Page, live_server: str, seed_data):
        """in_progress状態では done・todo・cancelled ボタンが表示される"""
        page.goto(f"{live_server}/tasks/2")  # Task 2: status=in_progress

        expect(page.locator('[data-testid="btn-transition-done"]')).to_have_count(1)
        expect(page.locator('[data-testid="btn-transition-todo"]')).to_have_count(1)
        expect(page.locator('[data-testid="btn-transition-cancelled"]')).to_have_count(1)

    def test_in_progress_hides_invalid_transition_buttons(self, page: Page, live_server: str, seed_data):
        """in_progress状態では in_progress ボタンが表示されない"""
        page.goto(f"{live_server}/tasks/2")  # Task 2: status=in_progress

        expect(page.locator('[data-testid="btn-transition-in_progress"]')).to_have_count(0)

    # --- done ---

    def test_done_shows_valid_transition_buttons(self, page: Page, live_server: str, seed_data):
        """done状態では todo ボタンのみが表示される"""
        page.goto(f"{live_server}/tasks/4")  # Task 4: status=done

        expect(page.locator('[data-testid="btn-transition-todo"]')).to_have_count(1)

    def test_done_hides_invalid_transition_buttons(self, page: Page, live_server: str, seed_data):
        """done状態では done・in_progress・cancelled ボタンが表示されない"""
        page.goto(f"{live_server}/tasks/4")  # Task 4: status=done

        expect(page.locator('[data-testid="btn-transition-done"]')).to_have_count(0)
        expect(page.locator('[data-testid="btn-transition-in_progress"]')).to_have_count(0)
        expect(page.locator('[data-testid="btn-transition-cancelled"]')).to_have_count(0)

    # --- cancelled ---

    def test_cancelled_shows_valid_transition_buttons(self, page: Page, live_server: str, seed_data):
        """cancelled状態では todo ボタンのみが表示される"""
        # todo → cancelled に遷移させてから検証
        page.goto(f"{live_server}/tasks/1")
        page.locator('[data-testid="btn-transition-cancelled"]').click()
        page.wait_for_url(f"{live_server}/tasks/1")

        expect(page.locator('[data-testid="btn-transition-todo"]')).to_have_count(1)

    def test_cancelled_hides_invalid_transition_buttons(self, page: Page, live_server: str, seed_data):
        """cancelled状態では done・in_progress・cancelled ボタンが表示されない"""
        # todo → cancelled に遷移させてから検証
        page.goto(f"{live_server}/tasks/1")
        page.locator('[data-testid="btn-transition-cancelled"]').click()
        page.wait_for_url(f"{live_server}/tasks/1")

        expect(page.locator('[data-testid="btn-transition-done"]')).to_have_count(0)
        expect(page.locator('[data-testid="btn-transition-in_progress"]')).to_have_count(0)
        expect(page.locator('[data-testid="btn-transition-cancelled"]')).to_have_count(0)


# ========================================================
# 遷移実行テスト（ボタンクリック後にステータスが変わるか確認）
# ========================================================

@pytest.mark.e2e
class TestStatusTransition:
    """各ステータスから有効な遷移先へ実際に遷移できるかを検証する"""

    # --- todo からの遷移 ---

    def test_todo_to_in_progress(self, page: Page, live_server: str, seed_data):
        """todo → in_progress に遷移できる"""
        page.goto(f"{live_server}/tasks/1")
        page.locator('[data-testid="btn-transition-in_progress"]').click()
        page.wait_for_url(f"{live_server}/tasks/1")

        expect(page.locator('[data-testid="task-status-badge"]')).to_have_text("進行中")

    def test_todo_to_done(self, page: Page, live_server: str, seed_data):
        """todo → done に遷移できる"""
        page.goto(f"{live_server}/tasks/1")
        page.locator('[data-testid="btn-transition-done"]').click()
        page.wait_for_url(f"{live_server}/tasks/1")

        expect(page.locator('[data-testid="task-status-badge"]')).to_have_text("完了")

    def test_todo_to_cancelled(self, page: Page, live_server: str, seed_data):
        """todo → cancelled に遷移できる"""
        page.goto(f"{live_server}/tasks/1")
        page.locator('[data-testid="btn-transition-cancelled"]').click()
        page.wait_for_url(f"{live_server}/tasks/1")

        expect(page.locator('[data-testid="task-status-badge"]')).to_have_text("キャンセル")

    # --- in_progress からの遷移 ---

    def test_in_progress_to_done(self, page: Page, live_server: str, seed_data):
        """in_progress → done に遷移できる"""
        page.goto(f"{live_server}/tasks/2")
        page.locator('[data-testid="btn-transition-done"]').click()
        page.wait_for_url(f"{live_server}/tasks/2")

        expect(page.locator('[data-testid="task-status-badge"]')).to_have_text("完了")

    def test_in_progress_to_todo(self, page: Page, live_server: str, seed_data):
        """in_progress → todo に遷移できる"""
        page.goto(f"{live_server}/tasks/2")
        page.locator('[data-testid="btn-transition-todo"]').click()
        page.wait_for_url(f"{live_server}/tasks/2")

        expect(page.locator('[data-testid="task-status-badge"]')).to_have_text("未着手")

    def test_in_progress_to_cancelled(self, page: Page, live_server: str, seed_data):
        """in_progress → cancelled に遷移できる"""
        page.goto(f"{live_server}/tasks/2")
        page.locator('[data-testid="btn-transition-cancelled"]').click()
        page.wait_for_url(f"{live_server}/tasks/2")

        expect(page.locator('[data-testid="task-status-badge"]')).to_have_text("キャンセル")

    # --- done からの遷移 ---

    def test_done_to_todo(self, page: Page, live_server: str, seed_data):
        """done → todo に遷移できる"""
        page.goto(f"{live_server}/tasks/4")
        page.locator('[data-testid="btn-transition-todo"]').click()
        page.wait_for_url(f"{live_server}/tasks/4")

        expect(page.locator('[data-testid="task-status-badge"]')).to_have_text("未着手")

    # --- cancelled からの遷移 ---

    def test_cancelled_to_todo(self, page: Page, live_server: str, seed_data):
        """cancelled → todo に遷移できる"""
        # todo → cancelled → todo の順で検証
        page.goto(f"{live_server}/tasks/1")
        page.locator('[data-testid="btn-transition-cancelled"]').click()
        page.wait_for_url(f"{live_server}/tasks/1")

        page.locator('[data-testid="btn-transition-todo"]').click()
        page.wait_for_url(f"{live_server}/tasks/1")

        expect(page.locator('[data-testid="task-status-badge"]')).to_have_text("未着手")

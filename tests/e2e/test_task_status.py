"""
タスクのステータス遷移 e2e テスト

テスト対象の操作:
  - タスク詳細画面でのステータス遷移ボタンの表示確認
  - ステータス遷移の実行と結果確認
  - 禁止されている遷移のボタンが表示されないことの確認

=== テスト対象となる主要なシナリオ ===

1. todo 状態のタスク詳細で「開始する」「キャンセルする」ボタンが表示される
2. todo → in_progress の遷移が成功し、ステータスバッジが変わる
3. in_progress → done の遷移が成功する（todo→in_progress→done の連続遷移）
4. done → todo（再オープン）の遷移が成功する
5. cancelled → todo（再オープン）の遷移が成功する
6. done 状態では「in_progress に戻す」ボタンが表示されない
7. done 状態では「キャンセル」ボタンが表示されない
8. cancelled 状態では「開始する」ボタンが表示されない

=== 参考: data-testid 一覧（ステータス遷移関連） ===

    [data-testid='task-status-badge']            : 現在のステータスバッジ
    [data-testid='status-actions']               : ステータス遷移ボタン群
    [data-testid='btn-transition-todo']          : 「未着手に戻す」ボタン
    [data-testid='btn-transition-in_progress']   : 「開始する」ボタン
    [data-testid='btn-transition-done']          : 「完了にする」ボタン
    [data-testid='btn-transition-cancelled']     : 「キャンセルする」ボタン

=== 参考: ステータス遷移ルール ===

    許可:
      todo        → in_progress, cancelled
      in_progress → done, todo, cancelled
      done        → todo
      cancelled   → todo

    禁止:
      done        → in_progress, cancelled
      cancelled   → in_progress, done
      任意        → 同じステータス
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_todo_to_in_progress(page: Page, live_server: str, seed_data):
    """todo → in_progress 遷移が成功し、ステータスバッジが変わる"""
    page.goto(f"{live_server}/tasks")

    # seed_data の "プロジェクト資料作成"（status=todo）の詳細ページへ移動
    page.locator("[data-testid='task-title']", has_text="プロジェクト資料作成").click()
    page.wait_for_url(f"{live_server}/tasks/*")

    # 初期ステータスが todo（未着手）であることを確認
    expect(page.locator("[data-testid='task-status-badge']")).to_have_text("未着手")

    # 「開始する」ボタンをクリックして in_progress へ遷移
    page.locator("[data-testid='btn-transition-in_progress']").click()

    # ステータスバッジが in_progress（進行中）に変わることを確認
    expect(page.locator("[data-testid='task-status-badge']")).to_have_text("進行中")

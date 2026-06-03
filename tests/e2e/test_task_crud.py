"""
タスク CRUD の e2e テスト

テスト対象の操作:
  - タスクの作成（正常系・バリデーションエラー）
  - タスクの編集
  - タスクの削除
  - タスク一覧でのフィルタリング
  - 期限切れタスクの表示

=== 使い方 ===

    @pytest.mark.e2e
    def test_create_task_and_see_in_list(page, live_server, seed_data):
        page.goto(f"{live_server}/tasks/new")
        page.fill("[data-testid='input-title']", "新しいタスク")
        page.click("[data-testid='btn-submit']")

        # 作成後はタスク詳細ページにリダイレクトされる
        page.wait_for_url(f"{live_server}/tasks/*")
        expect(page.locator("[data-testid='task-title']")).to_have_text("新しいタスク")

=== テスト対象となる主要なシナリオ ===

1. タスクを作成して一覧に表示されることを確認
2. 過去の期日でタスクを作成するとエラーメッセージが表示される
3. タスクのタイトルを編集して変更が反映される
4. タスクを削除すると一覧から消える
5. 期限切れタスクが一覧で赤色ハイライトされる
6. ステータスフィルタで絞り込みが機能する
7. カテゴリフィルタで絞り込みが機能する
8. キーワード検索が機能する

=== 参考: data-testid 一覧（テンプレートに付与済み） ===

    [data-testid='btn-create-task']  : タスク作成ボタン
    [data-testid='filter-form']      : フィルタフォーム
    [data-testid='filter-status']    : ステータスフィルタ（select）
    [data-testid='filter-category']  : カテゴリフィルタ（select）
    [data-testid='filter-search']    : キーワード検索（input）
    [data-testid='task-table']       : タスクテーブル
    [data-testid='task-row']         : タスクの行（複数）
    [data-testid='task-title']       : タスクタイトルリンク
    [data-testid='task-status']      : ステータスバッジ
    [data-testid='task-due-date']    : 期日セル
    [data-testid='btn-delete-task']  : 削除ボタン
    [data-testid='input-title']      : タイトル入力フィールド
    [data-testid='input-due-date']   : 期日入力フィールド
    [data-testid='select-priority']  : 優先度セレクト
    [data-testid='select-category']  : カテゴリセレクト
    [data-testid='btn-submit']       : フォーム送信ボタン
    [data-testid='flash-message']    : フラッシュメッセージ（エラー・成功）
    [data-testid='empty-task-list']  : タスクなし状態の表示
"""

import pytest
from playwright.sync_api import Page, expect

# TODO: ここにテストを実装してください
#
# ヒント: pytest.mark.e2e デコレータを付けることで
#         `pytest -m e2e` で e2e テストだけを実行できます
#
# 例:
# @pytest.mark.e2e
# def test_xxx(page: Page, live_server: str, seed_data):
#     page.goto(f"{live_server}/tasks")
#     ...

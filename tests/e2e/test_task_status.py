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

# TODO: ここにテストを実装してください

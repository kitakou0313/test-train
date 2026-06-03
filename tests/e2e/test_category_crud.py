"""
カテゴリ CRUD の e2e テスト

テスト対象の操作:
  - カテゴリの作成（正常系・バリデーションエラー）
  - カテゴリの編集
  - カテゴリの削除（正常系・削除制約エラー）
  - タスク作成フォームへのカテゴリ反映
  - タスク一覧のカテゴリフィルタ

=== テスト対象となる主要なシナリオ ===

1. カテゴリを作成するとカテゴリ一覧に表示される
2. カラーコードのバリデーション（不正形式でエラーが表示される）
3. 同名カテゴリを作成するとエラーが表示される
4. カテゴリを作成するとタスク作成フォームのカテゴリ選択肢に追加される
5. タスク一覧でカテゴリフィルタが機能する
6. 進行中タスクを持つカテゴリを削除しようとするとエラーが表示される
7. 進行中タスクを持たないカテゴリを削除すると一覧から消える
8. カテゴリを削除するとそのカテゴリを持つタスクのカテゴリが「なし」になる

=== 参考: data-testid 一覧（カテゴリ関連） ===

    [data-testid='btn-create-category'] : カテゴリ作成ボタン
    [data-testid='category-table']      : カテゴリテーブル
    [data-testid='category-row']        : カテゴリの行（複数）
    [data-testid='category-name']       : カテゴリ名セル
    [data-testid='category-color']      : カラースウォッチ
    [data-testid='btn-delete-category'] : 削除ボタン
    [data-testid='input-name']          : 名前入力フィールド
    [data-testid='input-color']         : カラーコード入力フィールド
    [data-testid='btn-submit']          : フォーム送信ボタン
    [data-testid='flash-message']       : フラッシュメッセージ（エラー・成功）
    [data-testid='empty-category-list'] : カテゴリなし状態の表示
    [data-testid='select-category']     : タスクフォームのカテゴリ選択（select）
"""

import pytest
from playwright.sync_api import Page, expect

# TODO: ここにテストを実装してください

# e2e テスト 概要

Playwright を使ったブラウザベースのエンドツーエンドテストについて説明します。

---

## e2e テストとは

e2e（エンドツーエンド）テストは、実際のブラウザを使いアプリ全体をユーザー視点で検証するテストです。

- ユニットテストと異なり、**HTML のレンダリング・フォーム送信・リダイレクト・フラッシュメッセージ**まで含めて検証できます
- DB・サーバー・ブラウザをすべて起動した状態で動作するため、結合度の高い検証ができます
- ただし実行時間はユニットテストより長く、環境依存も高くなります

---

## Playwright とは

[Playwright](https://playwright.dev/python/) は Microsoft が開発したブラウザ自動化ライブラリです。
Python から Chromium・Firefox・WebKit を操作でき、ページ遷移・フォーム入力・クリックなどの操作をコードで記述できます。

このプロジェクトでは **pytest-playwright** プラグインを使います。
pytest-playwright は Playwright を pytest に統合するプラグインで、ブラウザや `Page` オブジェクトをフィクスチャとして提供します。

---

## フィクスチャとは

**フィクスチャ（fixture）** は pytest が提供するテスト補助機能で、テスト関数の引数として宣言するだけで自動的に注入されるオブジェクトや処理のことです。
データベース接続・サーバー起動・初期データ投入など、テストの事前準備・後片付けをフィクスチャにまとめることで、各テスト関数をシンプルに保てます。

```python
# 引数名でフィクスチャを宣言するだけで pytest が自動的に注入する
def test_example(page, live_server, seed_data):
    ...
```

### スコープ

フィクスチャには **スコープ（scope）** があり、何回生成・破棄されるかを制御します。

| スコープ | 生成タイミング | 破棄タイミング |
|---------|-------------|-------------|
| `function`（デフォルト） | テスト関数ごと | テスト関数終了時 |
| `session` | テスト実行の最初 | 全テスト終了時 |

### conftest.py

フィクスチャは **conftest.py** に定義します。
pytest は自動的に conftest.py を読み込み、同じディレクトリ以下のすべてのテストでそのフィクスチャを利用できるようにします。
このプロジェクトの e2e フィクスチャは `tests/e2e/conftest.py` に定義されています。

---

## テストファイルの構成

```
tests/e2e/
├── conftest.py           # 共有フィクスチャ（サーバー起動・シードデータ）
├── test_task_crud.py     # タスク CRUD テスト
├── test_task_status.py   # タスクステータス遷移テスト
└── test_category_crud.py # カテゴリ CRUD テスト
```

---

## このプロジェクトのフィクスチャ

### `live_server`

テスト用 FastAPI サーバーをバックグラウンドスレッドで起動し、ベース URL（`http://127.0.0.1:8001`）を文字列で返します。

- スコープは `session`（テストセッション全体で1回だけ起動し、終了時に自動停止）
- ポート `8001` を使用（開発サーバーの `8000` と競合しない）
- `get_db` 依存性をテスト用 SQLite DB に差し替え済みのため、開発用 DB には影響しません

```python
def test_example(page: Page, live_server: str):
    page.goto(f"{live_server}/tasks")  # http://127.0.0.1:8001/tasks に移動
```

### `seed_data`

テスト用のサンプルデータを DB に投入します。

- スコープはデフォルト（`function`）— テストごとに DB をリセットして再投入するため、テスト間でデータが干渉しません
- 内部で `live_server` に依存しているため、`seed_data` を引数に加えるだけで自動的に解決されます

```python
def test_example(page: Page, live_server: str, seed_data):
    # この時点でカテゴリ3件・タスク5件が投入済み
    page.goto(f"{live_server}/tasks")
```

#### シードデータの内容

| 種別 | データ |
|------|--------|
| カテゴリ | 仕事（青 #0d6efd）、個人（緑 #198754）、学習（黄 #ffc107） |
| タスク | プロジェクト資料作成（todo / high / 仕事） |
| | 週次レポート（in_progress / medium / 仕事 / 期日=今日+2日） |
| | ジム（todo / low / 個人） |
| | Pytestドキュメント読む（done / high / 学習） |
| | 期限切れタスク（todo / medium / 期日=昨日） |

### `page`

pytest-playwright が提供するフィクスチャです。Playwright の `Page` オブジェクト（ブラウザタブ1つ）が注入されます。
スコープは `function`（テストごとに新しいタブが開かれ、終了時に閉じられます）。

```python
from playwright.sync_api import Page, expect

def test_example(page: Page, live_server: str):
    page.goto(f"{live_server}/tasks")
    expect(page.locator("[data-testid='task-table']")).to_be_visible()
```

---

## テストの基本構造

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e           # ← pytest マーカー（後述）
def test_view_task_list(page: Page, live_server: str, seed_data):
    # 1. ページに移動
    page.goto(f"{live_server}/tasks")

    # 2. 要素の存在・テキストを確認
    expect(page.locator("[data-testid='task-table']")).to_be_visible()
    expect(page.locator("[data-testid='task-row']")).to_have_count(5)
```

### pytest マーカー（`@pytest.mark.e2e`）

**マーカー** は pytest でテストにタグを付ける機能です。
`@pytest.mark.e2e` を付けると、`pytest -m e2e` でこのマーカーが付いたテストだけを選んで実行できます。
e2e テストはユニットテストより実行時間が長いため、普段はユニットテストだけを `pytest -m unit` で実行し、必要なときだけ e2e テストを実行する使い分けが可能です。

---

## テストの実行

```bash
# e2e テストのみ実行
pytest -m e2e

# 特定ファイルのみ
pytest tests/e2e/test_task_crud.py -m e2e

# 特定テストのみ
pytest tests/e2e/test_task_crud.py::test_create_task -m e2e
```

---

## Playwright の主要 API

### Page オブジェクト

`page` フィクスチャから得られる `Page` オブジェクトは、ブラウザタブ1つを表します。
このオブジェクトを通じてページへの移動・要素の操作・情報の取得を行います。

### ナビゲーション

```python
page.goto(url)               # 指定 URL に移動（ページの読み込み完了まで自動待機）
page.wait_for_url(pattern)   # URL が指定パターンに変わるまで待機（glob パターン使用可）
page.go_back()               # ブラウザの「戻る」と同じ操作
page.reload()                # ページをリロード
```

`wait_for_url` の glob パターン例：

```python
page.wait_for_url(f"{live_server}/tasks/*")   # /tasks/123 など任意の ID にマッチ
page.wait_for_url(f"{live_server}/tasks")     # 完全一致
```

### セレクター

**セレクター（selector）** は、HTML ページの中から操作したい要素を特定するための文字列です。
CSS セレクター・XPath・テキスト内容など複数の記法が使えます。

このプロジェクトでは **`data-testid` 属性** をセレクターとして統一的に使います。
`data-testid` はテスト専用の HTML 属性で、デザイン変更やクラス名の変更に影響されません。

```html
<!-- HTML 側の例 -->
<table data-testid="task-table">...</table>
```

```python
# Python 側での参照
page.locator("[data-testid='task-table']")
```

CSS セレクター / XPath との比較：

| 記法 | 例 | 問題点 |
|------|-----|--------|
| CSS クラス | `.task-table` | デザイン変更でクラス名が変わると壊れる |
| XPath | `//table[@id='tasks']` | 構造変更に弱い・可読性が低い |
| **data-testid** | `[data-testid='task-table']` | テスト目的専用のため安定している |

### Locator

**Locator（ロケーター）** は、`page.locator(selector)` で取得できるオブジェクトです。
セレクターに一致する要素を「遅延評価」で参照します。実際の DOM 操作はクリックやアサーションを呼び出したときに初めて実行されます。

```python
# locator を取得しただけでは DOM へのアクセスは発生しない
locator = page.locator("[data-testid='task-row']")

# click() や expect() を呼んだときに DOM を探す
locator.first.click()
expect(locator).to_have_count(5)
```

Locator はチェーン（連鎖）できます：

```python
# task-row の中にある btn-delete-task を探す（スコープを限定できる）
row = page.locator("[data-testid='task-row']", has_text="週次レポート")
row.locator("[data-testid='btn-delete-task']").click()
```

複数要素への絞り込み：

```python
page.locator("[data-testid='task-row']").first        # 最初の要素
page.locator("[data-testid='task-row']").last         # 最後の要素
page.locator("[data-testid='task-row']").nth(2)       # 3番目（0-indexed）
page.locator("[data-testid='task-row']", has_text="週次レポート")  # テキストで絞り込み
```

### 要素の操作

```python
page.fill(selector, text)              # テキストフィールドを text で上書き入力
page.click(selector)                   # 要素をクリック
page.select_option(selector, value)    # <select> の value で選択
page.select_option(selector, label="ラベル")  # <select> の表示テキストで選択
page.get_by_text("ラベル").click()     # テキスト内容で要素を取得してクリック
page.get_by_role("button", name="送信").click()  # ロールとアクセシブル名で取得
```

### 自動待機

Playwright はほとんどの操作で **自動的に要素が現れるまで待機** します（デフォルト 30 秒）。
`sleep` を使う必要はありません。

```python
# NG: 不要な sleep
page.click("[data-testid='btn-submit']")
import time; time.sleep(2)  # ← 不要。Playwright が待機してくれる
expect(page.locator(...)).to_be_visible()

# OK: そのまま続けるだけでよい
page.click("[data-testid='btn-submit']")
expect(page.locator(...)).to_be_visible()
```

### アサーション（`expect` を使う）

`expect(locator)` は **自動リトライ付きのアサーション** です。
条件が満たされるまで一定時間リトライし続けるため、非同期な DOM 更新に対しても安定したアサーションが書けます。

```python
from playwright.sync_api import expect

expect(locator).to_be_visible()           # 要素が表示されている
expect(locator).not_to_be_visible()       # 要素が非表示（または存在しない）
expect(locator).to_have_text("テキスト")  # テキストが完全一致
expect(locator).to_contain_text("一部")   # テキストを部分一致で含む
expect(locator).to_have_count(n)          # ロケーターに一致する要素が n 個ある
expect(locator).to_have_value("値")       # <input> の現在の値が一致
expect(locator).to_have_class("cls")      # 要素が指定クラスを持つ
expect(page).to_have_url("http://...")    # ページの現在 URL が一致
```

`expect()` に渡す `locator` は複数要素にマッチしていても構いません。
`to_have_count()` のように複数要素を対象にしたアサーションに使えます。

---

## よくあるパターン

### フォーム送信

```python
page.goto(f"{live_server}/tasks/new")
page.fill("[data-testid='input-title']", "新しいタスク")
page.select_option("[data-testid='select-priority']", "high")
page.click("[data-testid='btn-submit']")
```

### POST-Redirect-GET パターン後の確認

**POST-Redirect-GET（PRG）パターン** とは、フォーム送信（POST）後にサーバーがリダイレクト（302）を返し、ブラウザが別ページに GET リクエストを送る設計です。
このアプリはこのパターンを採用しているため、フォーム送信後は URL が変わります。
`page.wait_for_url()` でリダイレクト先の URL への遷移を待ってからアサーションを行います。

```python
page.click("[data-testid='btn-submit']")
# 送信後は /tasks/new → /tasks/{id} にリダイレクトされる
page.wait_for_url(f"{live_server}/tasks/*")
expect(page.locator("[data-testid='task-title']")).to_have_text("新しいタスク")
```

### フラッシュメッセージの確認

**フラッシュメッセージ** とは、操作の成功・失敗をユーザーに伝えるための一時的なメッセージです。
このアプリではセッションに保存し、次のページ表示時に1回だけ表示します。
エラーが発生したとき（バリデーション失敗・制約違反など）や、操作が成功したときに表示されます。

```python
page.click("[data-testid='btn-submit']")
# バリデーションエラー時はリダイレクトせずフォームページに留まり、
# フラッシュメッセージが表示される
expect(page.locator("[data-testid='flash-message']")).to_be_visible()
```

### 特定行への操作

```python
# "週次レポート" を含む行の削除ボタンをクリック
row = page.locator("[data-testid='task-row']", has_text="週次レポート")
row.locator("[data-testid='btn-delete-task']").click()
```

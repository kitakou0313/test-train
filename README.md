# test-train
いろんなテスト技法を試す

## ToDo
- Unit test
- e2e test
    - Playwright
- Perfornamce Test
    - Lighthouse
- 各テストの品質の評価

## セットアップ

```bash
# 依存パッケージのインストール
pip install -r requirements-dev.txt

# Playwright ブラウザのインストール（e2e テスト用）
playwright install chromium --with-deps
```

## アプリの起動

```bash
# シードデータの投入（初回のみ）
python scripts/seed.py

# サーバー起動
uvicorn app.main:app --reload --port 8000
```

ブラウザで http://localhost:8000 にアクセス。

## テストの実行

```bash
# Unit test のみ
pytest -m unit

# e2e test のみ
pytest -m e2e

# すべてのテスト
pytest
```

## 想定するシチュエーション
- 機能要件からのテストの定義
    - ソフトウェアの受け入れ基準の決定
## 修正点
- ドメインモデルがない
    - 状態遷移に関わるドメインルールがServiceに入っている
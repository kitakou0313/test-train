# ブラックボックステスト

## 全遷移テスト
- 全状態の数 * 全遷移の検証
- 今回は遷移のイベントが与えられていないので、各状態への遷移についてそれぞれ検証する

### テストケース
以下4状態なので4*4で16種
- todo
- in_progress
- done
- cancelled

テストケースは以下
- todo -> todo
    - 不正
- todo -> in_progress
    - 有効
- todo -> done
    - 不正
- todo -> cancelled
    - 有効
- in_progress -> todo
    - 有効
- in_progress -> in_progress
    - 不正
- in_progress -> done
    - 有効
- in_progress -> cancelled
    - 有効
- done -> todo
    - 有効
- done -> in_progress
    - 不正
- done -> done
    - 不正
- done -> cancelled
    - 不正
- cancelled -> todo
    - 有効
- cancelled -> in_progress
    - 不正
- cancelled -> done
    - 不正
- cancelled -> cancelled
    - 不正



# ホワイトボックステスト

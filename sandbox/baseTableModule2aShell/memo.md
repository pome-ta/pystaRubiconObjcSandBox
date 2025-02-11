# 📝 2025/02/11

## a-shell で再度読み込み時の落ちる原因を探す

- `_prototype` の`overrideCell` method を除去して`initWithStyle_reuseIdentifier_` に全部入れた
  - 違うぽいので、戻す
- 各セルのinstance method 呼び出しがダメっぽい。それ以外を一度整備するか？

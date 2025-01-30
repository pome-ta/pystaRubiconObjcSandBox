# 📝 2025/01/30

## `eventloop.py` 調査

a-shell でのUIKit 実装挙動安定化の調査


Pyto では、Pythonista3 と似た感じの処理をしていたので、a-shell 実行のための直接的なヒントにはならなそう。

`eventloop.py` でのライフサイクル・イベントループ処理を把握することが必要そう。

[eventloopMemo.py at main · pome-ta/pystaRubiconObjcSandBox · GitHub](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/ashellTest/pyrubicon/objc/eventloopMemo.py) ごにょごにょとメモを付け足していく


## memo

### `contextvars`

- [contextvars --- コンテキスト変数 — Python 3.10.16 ドキュメント](https://docs.python.org/ja/3.10/library/contextvars.html)

> 状態を持っているコンテキストマネージャは threading.local() ではなくコンテキスト変数を使い、並行処理のコードから状態が意図せず他のコードへ漏れ出すのを避けるべきです。




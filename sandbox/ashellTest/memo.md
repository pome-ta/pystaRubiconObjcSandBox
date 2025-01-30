# 📝 2025/01/30

## `eventloop.py` 調査

a-shell でのUIKit 実装挙動安定化の調査


Pyto では、Pythonista3 と似た感じの処理をしていたので、a-shell 実行のための直接的なヒントにはならなそう。

`eventloop.py` でのライフサイクル・イベントループ処理を把握することが必要そう。

[eventloopMemo.py at main · pome-ta/pystaRubiconObjcSandBox · GitHub](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/ashellTest/pyrubicon/objc/eventloopMemo.py) ごにょごにょとメモを付け足していく


## memo

### `contextvars`

- [contextvars --- コンテキスト変数 — Python 3.10.16 ドキュメント](https://docs.python.org/ja/3.10/library/contextvars.html)

> 状態を持っているコンテキストマネージャは `threading.local()` ではなくコンテキスト変数を使い、並行処理のコードから状態が意図せず他のコードへ漏れ出すのを避けるべきです。


### `iOSLifecycle`

(多分) a-shell の場合には、App が走っている状態だから不要なはず。。。

- [macOS/iOSスレッドプログラミング（ThreadとRunLoop） #Objective-C - Qiita](https://qiita.com/cubenoy22/items/098a90133dfdc3f33ccc)
- [run | Apple Developer Documentation](https://developer.apple.com/documentation/foundation/nsrunloop/1412430-run)
  - > 実行ループを終了したい場合は、このメソッドを使用しないでください。代わりに、他の実行メソッドの 1 つを使用し、ループで独自の他の任意の条件もチェックします。簡単な例は：


### `CFLifecycle`

- [CFRunLoopによるCore Animationの逐次的アニメーション #Objective-C - Qiita](https://qiita.com/icecocoa6/items/6d5c023ada5e30eb209c)


### CFRunLoop

- [CFRunLoop | Apple Developer Documentation](https://developer.apple.com/documentation/corefoundation/cfrunloop?language=objc)
- [Run Loops](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Multithreading/RunLoopManagement/RunLoopManagement.html#//apple_ref/doc/uid/10000057i-CH16)
- [Introduction | Threading Programming Guide](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Multithreading/Introduction/Introduction.html#//apple_ref/doc/uid/10000057i)






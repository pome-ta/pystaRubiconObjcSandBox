# 📝 2025/01/31

## `asyncio` オベンキョ


### [Pythonにasyncioってあるけどよく知らなかったので調べた](https://zenn.dev/knowhere_imai/articles/ba850780152b01) めも

> シングルスレッドで動作する**並行**処理


> Pythonでは`await` 無しでコルーチンを実行することはできません

`await` 無しだから、これが出たのかな？


```
RuntimeWarning: coroutine 'BaseEventLoop.shutdown_asyncgens' was never awaited
  loop.shutdown_asyncgens()
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```


### Pythonista3 Discord

[18.5.3. タスクとコルーチン — Python 3.6.15 ドキュメント](https://docs.python.org/ja/3.6/library/asyncio-task.html#example-hello-world-coroutine)


3.10 のドキュメントない？


現在、Pythonista3 Pyto a-Shell ごとに挙動が違う

- Pythonista3 
  - `#### ベース` 以下の通り
- Pyto
  - `### ベース` だと初動から、`RuntimeError: Event loop is closed`

- a-Shell
  - `DeprecationWarning` は出るが、動く


#### ベース

> 2回目以降は`RuntimeError: Event loop is closed`


```python
import asyncio


async def hello_world():
  print("Hello World!")


loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
loop.run_until_complete(hello_world())
loop.close()
```


#### 提案

```
DeprecationWarning: There is no current event loop
  loop = asyncio.get_event_loop()
```

とは、出るけど、動いてる

```python
import asyncio


async def hello_world():
  print("Hello World!")

asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
loop.run_until_complete(hello_world())
loop.close()
```


#### 追加

これだと、エラーもWarning も出ないけど、同じ処理になってるのかしら？

```python
import asyncio


async def hello_world():
  print("Hello World!")


loop = asyncio.new_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
loop.run_until_complete(hello_world())
loop.close()
```




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









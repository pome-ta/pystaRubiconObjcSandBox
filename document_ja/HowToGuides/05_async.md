# Rubion による非同期プログラミング

> [Asynchronous Programming with Rubicon - Rubicon 0.5.0](https://rubicon-objc.readthedocs.io/en/stable/how-to/async.html#)


Python3 の目玉機能の1つは、[`asyncio`](https://docs.python.org/ja/3.10/library/asyncio.html#module-asyncio) で実装されたネイティブ非同期プログラミングの導入です。

非同期プログラミングの使用の概要については、[非同期モジュールのドキュメント](https://docs.python.org/ja/3.10/library/asyncio.html) を参照してください。


## asyncio とCoreFoundation の統合

[`asyncio`](https://docs.python.org/ja/3.10/library/asyncio.html#module-asyncio) モジュールは、非同期機能を調整するためのイベントループを提供します。ただし、Objective C GUI アプリケーションを実行している場合は、CoreFoundation が提供するイベントループがすでにある可能性があります。このCoreFoundation イベントループは、エンドユーザーコードで`NSApplication` または`UIApplication` によってラップされます。

ただし、2つのイベントループを同時に実行することはできませんので、2つを統合する方法が必要です。幸いなことに、[`asyncio`](https://docs.python.org/ja/3.10/library/asyncio.html#module-asyncio) はイベントループをカスタマイズする方法を提供し、他のイベントソースと統合できます。

イベントループポリシーを使用してこれを行います。Rubicon は、Core Foundation イベント処理をasyncio イベントループに挿入するCore Foundation イベントループポリシーを提供します。

純粋な Core Foundation アプリケーションで asyncio を使用するには、次の操作を行います。

```python
# Import the Event Loop Policy
from rubicon.objc.eventloop import EventLoopPolicy

# Install the event loop policy
asyncio.set_event_loop_policy(EventLoopPolicy())

# Create an event loop, and run it!
loop = asyncio.new_event_loop()
loop.run_forever()
```

最後の呼び出し（`loop.run_forever()` ）は、名前が示すように、イベントハンドラーが`loop.stop()` を呼び出してイベントループを終了するまで、永遠に実行されます。


## asyncio をAppKit および`NSApplication` と統合する

AppKit と NSApplication を使用している場合は、CoreFoundation イベントループを開始するだけでなく、`NSApplication` のライフサイクル全体を開始する必要があります。これを行うには、アプリケーションインスタンスを`loop.run_forever()` の呼び出しに渡します。


```python
# Import the Event Loop Policy and lifecycle
from rubicon.objc.eventloop import EventLoopPolicy, CocoaLifecycle

# Install the event loop policy
asyncio.set_event_loop_policy(EventLoopPolicy())

# Get a handle to the shared NSApplication
from ctypes import cdll, util
from rubicon.objc import ObjCClass

appkit = cdll.LoadLibrary(util.find_library('AppKit'))
NSApplication = ObjCClass('NSApplication')
NSApplication.declare_class_property('sharedApplication')
app = NSApplication.sharedApplication

# Create an event loop, and run it, using the NSApplication!
loop = asyncio.new_event_loop()
loop.run_forever(lifecycle=CocoaLifecycle(app))
```

繰り返しになりますが、これは「永遠に」実行されます。`loop.stop()`が呼び出されるか、NSApplication で`terminate:` が呼び出されるまで。



## asyncio とiOS およびUIApplication の統合


iOS で UIKit と UIApplication を使用している場合は、iOS のライフサイクルを使用する必要があります。これを行うには、`loop.run_forever()` の呼び出しに `iOSLifecycle` オブジェクトを渡します。


```python
# Import the Event Loop Policy and lifecycle
from rubicon.objc.eventloop import EventLoopPolicy, iOSLifecycle

# Install the event loop policy
asyncio.set_event_loop_policy(EventLoopPolicy())

# Create an event loop, and run it, using the UIApplication!
loop = asyncio.new_event_loop()
loop.run_forever(lifecycle=iOSLifecycle())
```


繰り返しになりますが、これは「永遠に」実行されます。`loop.stop()`が呼び出されるか、UIApplication で`terminate:` が呼び出されるまで。


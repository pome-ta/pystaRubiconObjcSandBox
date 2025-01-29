# 📝 2025/01/29


[`rubicon-objc` と`toga` と `Pyto` と - pome-ta_hugo-blog](https://pome-ta.github.io/pome-ta_hugo-blog/posts/notebooks/20250128a/)


テキストとして残そうとしたけど、アクセス的に不便なので、続きはこっちに書く



### life cycle とは？

toga では、iOS のlifecycle はずっとぶん回す(という雑な理解) かたちでの実装をしているが、Pythonista3 で`eventloop.py` を呼び出すときには、`iOSLifecycle` を使わないと実行ができる。

toga は、無の状態(と、表現をしていいのか？) からのスタートだから、そういった仕様としている？でもPyto も同じ？(いや、オーバーライド時に上書きして消してる？)


## Pyto のコードで気になる部分追っかけ


- [pyto_ui.py #L8039](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/1571e7898b69459fdc0538cfaaf6dcd9efe372aa/sandbox/pytoTest/intoPytoModules/Lib/pyto_ui.py#L8039) `def show_view_controller(view_controller: "UIViewController"):`
  - [#Using UIViewController | pyto_ui — Pyto documentation](https://pyto.readthedocs.io/en/latest/library/pyto_ui.html#using-uiviewcontroller)



### Semaphore

Python デフォではなくて、Swift Python 呼んでる感じだ


- [Pyto/Pyto/Model/Python Bridging/PyMainThread.swift at main · pome-ta/Pyto · GitHub](https://github.com/pome-ta/Pyto/blob/main/Pyto/Model/Python%20Bridging/PyMainThread.swift)
  - `let semaphore = Python.Semaphore(value: 0)` ってところ
  - `semaphore?.signal()` ってなんやろか？
- [Semaphoreを使ってPythonの非同期処理の平行処理数をコントロールする](https://zenn.dev/yosemat/articles/39c36d0ed88a7c)
- [【Swift】@escaping属性のクロージャとは #Xcode - Qiita](https://qiita.com/imchino/items/48564b0c23a64f539060)



### 終了状態を検知できるか？

- [iOSアプリのライフサイクル #Swift - Qiita](https://qiita.com/KenNagami/items/766d5f95940c76a8c3cd)
  - `applicationWillResignActive` これとか？
- [NotificationCenterを使用して、アプリの状態を認識する #iOS - Qiita](https://qiita.com/tosh_3/items/df52802514cc9737e75b)

### Python を埋め込む

- [iOSのSwift,Objective-CでPythonを呼び出す #Python - Qiita](https://qiita.com/Hiroki_Kawakami/items/830baa5adcce5e483764)
- [1. 他のアプリケーションへの Python の埋め込み — Python 3.10.16 ドキュメント](https://docs.python.org/ja/3.10/extending/embedding.html)



# 📝 2025/01/27

## Pyto で(独自の)Rubicon

- Pyto 自体のRubicon とバッティングしてる？
- `Loaded modules` 内の処理を調査？

## Pyto 内のtoga とかpyto_ui とかの処理を確認する


モジュールをぶっ込んだけど

`.gitignore` に`lib` って入れてるから、Lib のやつ入ってないわ😂


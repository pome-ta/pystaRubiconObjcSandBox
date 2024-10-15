# あなたの最初の橋: Your first bridge

> [Your first bridge - Rubicon 0.4.9](https://rubicon-objc.readthedocs.io/en/stable/tutorial/tutorial-1.html)

この例では、Rubicon を使用してObjective-C Foundationライブラリとそのライブラリの`NSURL` クラスにアクセスします。`NSURL` は、URLの表現と操作に使用されるクラスです。


このチュートリアルでは、[Rubicon を使い始める: Getting Started with Rubicon](../HowToGuides/01_GettingStartedWithRubicon.md) に記載されているように環境を設定したことを前提としています。


## NSURL へのアクセス: Accessing NSURL

Python を起動し、Objective-C クラスへの参照を取得します。この例では、`NSURL` クラス、Objective-C のURL 表現を使用します:


```python
from rubicon.objc import ObjCClass
NSURL = ObjCClass("NSURL")
```

これにより、Objective-C ランタイムの`NSURL` クラスに透過的にブリッジされたPythonの`NSURL` クラスが得られます。[`NSURL` に関するAppleのドキュメント](https://developer.apple.com/documentation/foundation/nsurl?language=objc) に記載されているすべての方法またはプロパティは、このブリッジを介してアクセスできます。


`NSURL` オブジェクトのインスタンスを作成しましょう。`NSURL` ドキュメントでは、静的コンストラクタ `+URLWithString:` が記述されています。このコンストラクタは次のように呼び出すことができます:

```python
base = NSURL.URLWithString("https://beeware.org/")
```

つまり、Python のメソッドの名前はObjective-C のメソッドと同じです。最初の引数は`NSString *` として宣言されます。Rubicon は、メソッドの呼び出しの一部としてPython [`str`](https://docs.python.org/ja/3.10/library/stdtypes.html#str) を`NSString` インスタンスに変換します。


`NSURL` には別の静的コンストラクタがあります:  
`+URLWithString:relativeToURL:` このコンストラクタを呼び出すこともできます:

```python
full = NSURL.URLWithString("contributing/", relativeToURL=base)
```

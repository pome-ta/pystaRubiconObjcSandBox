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


`NSURL` オブジェクトのインスタンスを作成しましょう。`NSURL` ドキュメントでは、静的コンストラクタ(static constructor) `+URLWithString:` が記述されています。このコンストラクタは次のように呼び出すことができます:

```python
base = NSURL.URLWithString("https://beeware.org/")
```

つまり、Python のメソッドの名前はObjective-C のメソッドと同じです。最初の引数は`NSString *` として宣言されます。Rubicon は、メソッドの呼び出しの一部としてPython [`str`](https://docs.python.org/ja/3.10/library/stdtypes.html#str) を`NSString` インスタンスに変換します。


`NSURL` には別の静的コンストラクタがあります:  
`+URLWithString:relativeToURL:` このコンストラクタを呼び出すこともできます:

```python
full = NSURL.URLWithString("contributing/", relativeToURL=base)
```


2番目の引数(`relativeToURL`) は、キーワード引数としてアクセスされます。この引数はタイプ`NSURL *` であると宣言されます。`base` は`NSURL` のインスタンスであるため、Rubicon はこのインスタンスを通過できます。

時々、Objective-C メソッド定義は同じキーワード引数名を2回使用します(たとえば、`NSLayoutConstraint` には`+constraintWithItem:attribute:relatedBy:toItem:attribute:multiplier:constant:` selector があり、属性キーワードを2回使用します)。これはObjective-C では合法ですが、メソッド呼び出しでキーワード引数を繰り返すことができないため、Pythonでは合法ではありません。この場合、あいまいなキーワード引数に`__` 接尾辞を使用して一意にすることができます。Objective-C 呼び出しを行うと、`__` 以降のコンテンツが削除されます。


```python
constraint = NSLayoutConstraint.constraintWithItem(
  first_item,
  attribute__1=first_attribute,
  relatedBy=relation,
  toItem=second_item,
  attribute__2=second_attribute,
  multiplier=2.0,
  constant=1.0
)
```

## インスタンスメソッド: Instance methods



これまで、'`+URLWithString:` 静的コンストラクタ(g: static constructor) を使用してきました。ただし、`NSUR` Lは初期化メソッド`-initWithString:` も提供します。この方法を使用するには、まずObjective-C ランタイムにインスタンスのメモリを割り当てるように指示し、次に初期化子を呼び出す必要があります:

```python
base = NSURL.alloc().initWithString("https://beeware.org/")
```

`NSURL` のインスタンスがあるので、操作する必要があります。`NSURL` は `absoluteURL` プロパティを記述します。このプロパティは Python 属性としてアクセスできます。


```python
absolute = full.absoluteURL
```

インスタンスでメソッドを呼び出すこともできます:

```python
longer = absolute.URLByAppendingPathComponent('how/first-time/')
```


コンソールでオブジェクトを出力する場合は、Objective-C プロパティの説明を使用するか、デバッグ出力には`debugDescription` を使用できます:


```python
longer.description
# > 'https://beeware.org/contributing/how/first-time/'

longer.debugDescription
# > 'https://beeware.org/contributing/how/first-time/'
```

内部的には、`description` と`debugDescription` は、それぞれPythonの同等の`__str__()` と`__repr__()` に接続されています。


```python
str(absolute)
# > 'https://beeware.org/contributing/'

repr(absolute)
# > '<ObjCInstance: NSURL at 0x1114a3cf8: https://beeware.org/contributing/>'

print(absolute)
# > https://beeware.org/contributing/
```

## 世界を乗っ取る時が来た！: Time to take over the world!

これで、どのクラスでも、どのライブラリでも、macOSまたはiOSエコシステム全体で、あらゆる方法にアクセスできます!Objective-C で何かを呼び出すことができれば、Python で呼び出すことができます。必要なのは:

> - ctypesでライブラリをロード
> - 使用したいクラスを登録、そして
> - これらのクラスをPythonで書かれたかのように使用してください。


## 次のステップ: Next steps

次のステップは、独自のクラスを作成し、それらをObjective-C ランタイムに公開することです。それが次のチュートリアルの主題です。


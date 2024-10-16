# チュートリアル2 - あなた自身のクラスを書く: Tutorial 2 - Writing your own class

> [Tutorial 2 - Writing your own class - Rubicon 0.4.9](https://rubicon-objc.readthedocs.io/en/stable/tutorial/tutorial-2.html)

最終的には、クラスインスタンスを引数として提供する必要があるObjective-C APIに出くわすでしょう。たとえば、macOS や iOS GUI クラスを使用する場合、GUI 要素がマウスクリックやキーを押す際にどのように反応するかを説明するために、「delegate」クラスを定義する必要があることがよくあります。



2つのメソッドで`Handler` クラスを定義しましょう:


> - `-initWithValue:.` 整数を受け入れるコンストラクタ、そして
> - `-pokeWithValue:andName:` 整数と文字列を受け入れ、文字列を出力し、値の半分である浮動小数点数を返すメソッド。


このクラスの宣言は次のようになります:

```python
from rubicon.objc import NSObject, objc_method


class Handler(NSObject):

  @objc_method
  def initWithValue_(self, v: int):
    self.value = v
    return self

  @objc_method
  def pokeWithValue_andName_(self, v: int, name) -> float:
    print("My name is", name)
    return v / 2.0
```


このコードには、いくつかの興味深い実装の詳細があります:

> - `Handler` クラスは`NSObject` を拡張します。これは、Objective-C ランタイムで登録できる方法でクラスを構築するようにRubicon に指示します
> - Objective-C に公開したい各メソッドは、`@objc_method` で装飾されています。メソッド名は、公開したいObjective-C記述子と一致しますが、コロン(`:`) はアンダースコア(`_`) に置き換えられます。これは、[あなたの最初の橋: Your first bridge](./01_YourFirstBridge.md) で議論されたメソッドを呼び出す「長い形式」の方法と一致します
> - `initWithValue_()` の`v` 引数は、Python 3のタイプアノテーションを使用してタイプを宣言します。Objective-C は静的タイピングを持つ言語であるため、Python で定義されたメソッドは、このタイピング情報を提供する必要があります。注釈が付けられていない引数は、タイプ`id` 、つまりObjective-Cオブジェクトへのポインタであると想定されます
> - `pokeWithValue_andName_()` メソッドは、整数引数に注釈を付け、戻り値タイプを浮動小数点数として注釈付けします。繰り返しになりますが、これはObjective-C タイピング操作をサポートするためのものです。戻り型アノテーションのない関数は、`id` を返すと想定されます。`None` の戻り値型アノテーションは、Objective-C の`void` メソッドとして解釈されます。名前引数は文字列として渡されるため、注釈を付ける必要はありません。文字列はObjective-Cの`NSObject` サブクラスです
> - `initWithValue_()` はコンストラクタなので、`self` を返します


クラスを宣言した後、インスタンス化して使用できます:

```python
my_handler = Handler.alloc().initWithValue(42)
print(my_handler.value)
# > 42
print(my_handler.pokeWithValue(37, andName="Alice"))
# > My name is Alice
#   18.5
```

## Objective-C プロパティ: Objective-C properties

`Handler` の初期化子を定義するとき、提供された値をクラスの値属性として保存しました。ただし、この属性はObjective-C に宣言されていないため、Objective-C ランタイムには表示されません。Python 内から値にアクセスできますが、Objective-C コードではアクセスできません。

Objective-C ランタイムに値を公開するには、小さな変更を1つ行い、値をObjective-C プロパティとして明示的に宣言する必要があります:

```python
from rubicon.objc import NSObject, objc_method, objc_property


class PureHandler(NSObject):

  value = objc_property()

  @objc_method
  def initWithValue_(self, v: int):
    self.value = v
    return self
```

これは、属性へのアクセスまたは変更方法に何も変更しません。Objective-C コードが属性も表示できることを意味します。

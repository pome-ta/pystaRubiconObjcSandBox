# あなたは私のタイプではありません:PythonでObjective-Cタイプを使用する: You’re just not my type: Using Objective-C types in Python

> [You’re just not my type: Using Objective-C types in Python - Rubicon 0.4.9](https://rubicon-objc.readthedocs.io/en/stable/how-to/type-mapping.html)


Objective-Cは、強力で静的に型付けされた言語です。すべての変数には特定のタイプがあり、そのタイプは時間の経過とともに変更できません。関数パラメータにも固定型があり、関数は正しい型の引数のみを受け入れます。

一方、Pythonは強力ですが、動的に型式化された言語です。すべてのオブジェクトには特定のタイプがありますが、すべての変数は任意のタイプのオブジェクトを保持できます。関数が引数を受け入れると、Python は任意のタイプのオブジェクトを渡すことができます。

したがって、Objective-C とPython を橋渡ししたい場合は、Rubicon が任意のタイプのPythonオブジェクトをObjective-Cの期待に一致する特定のタイプに変換する方法を解決できるように、静的タイピング情報を提供できる必要があります。


## タイプアノテーション: Type annotations

ライブラリで定義されたObjective-C メソッドを呼び出す場合、そのタイプはObjective-C ランタイムとRubicon にすでに知られています。ただし、Python で新しいメソッド(またはメソッドオーバーライド)を定義する場合は、そのタイプを手動で提供する必要があります。これは、Python 3 のタイプアノテーション構文を使用して行われます。

Objective-Cオブジェクトの渡しと返すには、追加の作業は必要ありません。パラメータや戻り値タイプに注釈を付けない場合、RubiconはObjective-Cオブジェクトであると仮定します。(何も返さないメソッドを定義するには、明示的`->None` アノテーションを追加する必要があります。)



他のすべてのパラメータと戻り値タイプ(プリミティブ、ポインタ、構造体)は、Rubicon とObjective-C にどのタイプを期待するかを伝えるために注釈付けする必要があります。これらのアノテーションは、[`NSInteger`](https://rubicon-objc.readthedocs.io/en/stable/reference/rubicon-objc-types.html#rubicon.objc.types.NSInteger) や[`NSRange`](https://rubicon-objc.readthedocs.io/en/stable/reference/rubicon-objc-types.html#rubicon.objc.types.NSRange) などのRubiconによって定義された型と、[`c_byte`](https://docs.python.org/ja/3.10/library/ctypes.html#ctypes.c_byte) や[`c_double`](https://docs.python.org/ja/3.10/library/ctypes.html#ctypes.c_double) などの[`ctypes`](https://docs.python.org/ja/3.10/library/ctypes.html#module-ctypes) モジュールの標準C型を使用できます。

たとえば、C `double` を取り、`NSInteger` を返すメソッドは、次のように定義され、注釈付けされます。


```python
@objc_method
def roundToZero_(self, value: c_double) -> NSInteger:
    return int(value)
```

また、Rubicon は特定のPythonタイプをメソッドシグネチャで使用でき、それらを一致するプリミティブ`ctypes` タイプに変換します。たとえば、Python [`int`](https://docs.python.org/ja/3.10/library/functions.html#int) は [`c_int`](https://docs.python.org/ja/3.10/library/ctypes.html#ctypes.c_int) として扱われ、[`float`](https://docs.python.org/ja/3.10/library/functions.html#float) は [`c_double`](https://docs.python.org/ja/3.10/library/ctypes.html#ctypes.c_double) として扱われます。



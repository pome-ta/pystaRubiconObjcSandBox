# あなたは私のタイプではありません:Python で Objective-C タイプを使用する: You’re just not my type: Using Objective-C types in Python

> [You’re just not my type: Using Objective-C types in Python - Rubicon 0.4.9](https://rubicon-objc.readthedocs.io/en/stable/how-to/type-mapping.html)

Objective-C は、強力で静的に型付けされた言語です。すべての変数には特定のタイプがあり、そのタイプは時間の経過とともに変更できません。関数パラメータにも固定型があり、関数は正しい型の引数のみを受け入れます。

一方、Python は強力ですが、動的に型式化された言語です。すべてのオブジェクトには特定のタイプがありますが、すべての変数は任意のタイプのオブジェクトを保持できます。関数が引数を受け入れると、Python は任意のタイプのオブジェクトを渡すことができます。

したがって、Objective-C と Python を橋渡ししたい場合は、Rubicon が任意のタイプの Python オブジェクトを Objective-C の期待に一致する特定のタイプに変換する方法を解決できるように、静的タイピング情報を提供できる必要があります。

## タイプアノテーション: Type annotations

ライブラリで定義された Objective-C メソッドを呼び出す場合、そのタイプは Objective-C ランタイムと Rubicon にすでに知られています。ただし、Python で新しいメソッド(またはメソッドオーバーライド)を定義する場合は、そのタイプを手動で提供する必要があります。これは、Python 3 のタイプアノテーション構文を使用して行われます。

Objective-C オブジェクトの渡しと返すには、追加の作業は必要ありません。パラメータや戻り値タイプに注釈を付けない場合、Rubicon は Objective-C オブジェクトであると仮定します。(何も返さないメソッドを定義するには、明示的`->None` アノテーションを追加する必要があります。)

他のすべてのパラメータと戻り値タイプ(プリミティブ、ポインタ、構造体)は、Rubicon と Objective-C にどのタイプを期待するかを伝えるために注釈付けする必要があります。これらのアノテーションは、[`NSInteger`](https://rubicon-objc.readthedocs.io/en/stable/reference/rubicon-objc-types.html#rubicon.objc.types.NSInteger) や[`NSRange`](https://rubicon-objc.readthedocs.io/en/stable/reference/rubicon-objc-types.html#rubicon.objc.types.NSRange) などの Rubicon によって定義された型と、[`c_byte`](https://docs.python.org/ja/3.10/library/ctypes.html#ctypes.c_byte) や[`c_double`](https://docs.python.org/ja/3.10/library/ctypes.html#ctypes.c_double) などの[`ctypes`](https://docs.python.org/ja/3.10/library/ctypes.html#module-ctypes) モジュールの標準 C 型を使用できます。

たとえば、C `double` を取り、`NSInteger` を返すメソッドは、次のように定義され、注釈付けされます。

```python
@objc_method
def roundToZero_(self, value: c_double) -> NSInteger:
    return int(value)
```

また、Rubicon は特定の Python タイプをメソッドシグネチャで使用でき、それらを一致するプリミティブ`ctypes` タイプに変換します。たとえば、Python [`int`](https://docs.python.org/ja/3.10/library/functions.html#int) は [`c_int`](https://docs.python.org/ja/3.10/library/ctypes.html#ctypes.c_int) として扱われ、[`float`](https://docs.python.org/ja/3.10/library/functions.html#float) は [`c_double`](https://docs.python.org/ja/3.10/library/ctypes.html#ctypes.c_double) として扱われます。

> [!NOTE]
> [rubicon.objc.types](https://rubicon-objc.readthedocs.io/en/stable/reference/rubicon-objc-types.html#module-rubicon.objc.types) 参照ドキュメントには、Rubicon が提供するすべての C 型定義が一覧表示され、Rubicon が型をどのように変換するかに関する追加情報が記載されています。

## タイプ変換: Type conversions

既存の Objective-C メソッドを呼び出すと、Rubicon は各引数に必要な型と返されるものをすでに知っています。この型情報に基づいて、Rubicon は渡された引数を適切な Objective-C 型に自動的に変換し、戻り値を適切な Python 型に変換します。これにより、多くの場合、Python と Objective-C タイプ間の明示的なタイプ変換が不要になります。

### 引数変換: Argument conversion

Objective-C メソッドが C プリミティブ引数を期待する場合、代わりに同等の Python 値を渡すことができます。たとえば、Python の`int`値は任意の整数引数(`int`、`NSInteger`、`uint8_t`、...)に渡され、Python `float`値は任意の浮動小数点引数(`double`、`CGFloat`、...)に渡すことができます。

C 構造を引数として渡すには、通常、構造インスタンスを名前で構築する必要があります。これは、特にネストされた構造(例:`NSRect(NSPoint(1.2, 3.4), NSSize(5.6, 7.8))`)。略語として、ルビコンは構造オブジェクトの代わりにタプルを渡すことができます(例:`((1.2, 3.4), (5.6, 7.8))`)およびそれらを必要な構造タイプに自動的に変換します。

パラメータが Objective-C オブジェクトを期待している場合、特定の Python オブジェクトを渡すこともできます。これは自動的に Objective-C オブジェクトに変換されます。たとえば、Python `str` は `NSString` に変換され、`bytes` は `NSData` などに変換されます。コレクションもサポートされています。リストと辞書は`NSArray`と`NSDictionary`に変換され、それらの要素は再帰的に変換されます。

> [!NOTE]
> これらの変換はすべて手動で実行することもできます。詳細については、手動変換を参照してください。



### 戻り値の変換とラッピング: Return value conversion and wrapping

メソッドから返されたプリミティブ値は、通常の`ctypes` 変換を使用して変換されます。C 整数は Python `int` に変換され、浮動小数点値は Python `float` に変換されます。



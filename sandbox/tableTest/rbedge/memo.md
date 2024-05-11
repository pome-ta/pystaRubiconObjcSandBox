# 📝 2024/04/21


class をまるっと定義して、呼び出すか？オーバーヘッドが無駄すぎるかな？


# 📝 2024/04/19


## `enumerations.py` の命名定義

基本的に、objc の名前で揃える。

Swift だと`.` が入ったり、Document で、Enumeration として型表記になってない場合もある。
その場合には、値としてDocument で参照しやすい方にする。



`.` は、`_` で繋ぐ


[pystaUIKitCatalogChallenge/objcista/constants.py at objc_util · pome-ta/pystaUIKitCatalogChallenge · GitHub](https://github.com/pome-ta/pystaUIKitCatalogChallenge/blob/objc_util/objcista/constants.py)

基本的には、ここをコピペ、使用するタイミングで、都度Document を参照する。


## `tests` ディレクトリ

``` .py
parent_level = 3
sys.path.append(str(pathlib.Path(__file__, '../' * parent_level).resolve()))
```

無理やりmodule をブチ込む、`sandbox` として、test 前の実験の場合は、level を階層に応じて指定する（test の意味とは）

まぁ、iPhone とworking copy との`.cloud` ファイル問題なんだけど、、、



# 📝 2026/01/24





## `enumerations.py` やら`globalVariables.py` やら`functions.py`

[GitHub - madsmtm/objc2: Bindings to Apple frameworks in Rust](https://github.com/madsmtm/objc2)
[GitHub - madsmtm/objc2-generated: Automatically generated code; see the `objc2` project for details.](https://github.com/madsmtm/objc2-generated)

を見習って、Framework ごとにフォルダ分けしてみた
入力が面倒だけど、整理できるから頑張るか、、、

[https://x.com/pome_ta93/status/2014994520849686955?s=12](https://x.com/pome_ta93/status/2014994520849686955?s=12) 面白現象も目撃できたし

### `__init__.py` での呼び出し

どうしよう、まるっとまとめちゃうかな？
ファイル名まで追っかける必要はないかしら？

## rubicon サブモジュールにする？

a-shell がとてもお行儀がいいので、読み込みでエラー吐くね、、、
Pythonista3 に`setuptools_scm` が無いからなんだが、、、


とりま、Pythonista3 実行想定でいくか、、、

a-shell は、改めて考えるか、、、


## mac 実行

Pythonista3 だと大丈夫だけど、a-shell だとclose 時に落ちる、、、
iPhone だとどうにか両方大丈夫なんだけどな、、、


# 📝 2026/01/23

## 無理やりimport

`modules` ディレクトリに逃して、実行するファイルのみで呼ぶようにしてみる。


```py
_TOP_DIR_NAME = 'pystaRubiconObjcSandBox'
_MODULES_DIR_NAME = 'modules'

# todo: `./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME}` にあるpackage のimport 準備
if __name__ == '__main__' and not __file__[:__file__.rfind('/')].endswith(
    _TOP_DIR_NAME):
  import pathlib
  import sys
  __parents = pathlib.Path(__file__).resolve().parents
  for __dir_path in __parents:
    if __dir_path.name == _TOP_DIR_NAME and (__modules_path := __dir_path /
                                             _MODULES_DIR_NAME).exists():
      sys.path.insert(0, str(__modules_path))
      break
  else:
    import warnings
    with warnings.catch_warnings():
      warnings.simplefilter('always', ImportWarning)
      __warning_message = f'./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME} not found in parent directories'
      warnings.warn(__warning_message, ImportWarning)
```

### Pythonista3 設定

`EXTERNAL FILES` で、`pystaRubiconObjcSandBox` を読んでおく必要あり。


## `enumerations.py` `globalVariables.py` など

一つにまとめちゃうと、無駄に`load_library` しちゃうから、
分割を意識した方がいいのかな？

- [objc2_ar_kit - Rust](https://docs.rs/objc2-ar-kit/latest/objc2_ar_kit/)
- [objc2_scene_kit - Rust](https://docs.rs/objc2-scene-kit/latest/objc2_scene_kit/)



# 📝 2026/01/21

## れあどめ整理

れあどめを丁寧に書くか
- import について
- リポジトリの構成
  - 増えていくたびに、追記
- Pythonista3 で実行の注意点


## 無理やりimport について

`sys.path.append` で、リポジトリ全体はまずいか？

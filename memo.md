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
  for path in __parents:
    if path.name == _TOP_DIR_NAME and (__modules_path :=
                                       path / _MODULES_DIR_NAME).exists():
      sys.path.insert(0, str(__modules_path))
      break
  else:
    import warnings
    with warnings.catch_warnings():
      warnings.simplefilter('always', ImportWarning)
      __warning_message = f'./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME} not found in parent directories'
      warnings.warn(__warning_message, ImportWarning)
```




# 📝 2026/01/21

## れあどめ整理

れあどめを丁寧に書くか
- import について
- リポジトリの構成
  - 増えていくたびに、追記
- Pythonista3 で実行の注意点


## 無理やりimport について

`sys.path.append` で、リポジトリ全体はまずいか？
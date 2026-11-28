# 📝 2026/11/28

## catalog やる

まずは、storyboard かな？




# 📝 2026/11/27

## プロジェクト内module の取得

一旦これで着地かな？


### 概要というか、意図というか、、、

- `bootstrap.py` をtop ディレクトリに置く
- コード実行時、真っ先に読み込ませる

全体的に:

- inspector に無駄な情報を出したくない
  - 「無駄」とは、bootstrap を使いローカルmodule をimport できるようにする処理の形跡のこと
- 実行ファイル側のボイラープレートをできるだけ簡素にする
  - 何をしてるのか？は、判断できる程度に




### コード

#### `./bootstrap.py`


```python
# Pythonista3 直接実行用: もろもろのpath の依存関係を通す
from pathlib import Path as _Path
import sys as _sys

__all__: list[str] = [
  '_setup',
]

_SRC_DIR_NAME = 'app'
_MODULES_DIR_NAME = 'pystaRubiconModules'

# 上に書いたディレクトリほど import 探索の優先度が高くなる
SEARCH_DIRS = (
  _SRC_DIR_NAME,  # 1. 作業用トップディレクトリ(最優先)
  _MODULES_DIR_NAME,  # 2. 共通ローカルモジュール群
)
ROOT_DIR = _Path(__file__).resolve().parent


def _setup(root_dir: _Path = ROOT_DIR) -> None:
  _target_paths = []
  for dir_name in SEARCH_DIRS:
    if not (dir_path := root_dir / dir_name).is_dir():
      raise FileNotFoundError(f'Directory not found: {dir_path}')
    _target_paths.append(str(dir_path))

  target_set = set(_target_paths)
  _sys.path[:] = [
    *_target_paths,
    *(p for p in _sys.path if p not in target_set),
  ]


_setup()

```


#### 実行したいファイルの先頭

```python
# `bootstrap.py` ファイルを`bootstrap` としてimport したい場合
if __name__ == '__main__':
  try:
    import bootstrap
  except ModuleNotFoundError as e:
    _TARGET_NAME = 'bootstrap'
    if e.name != _TARGET_NAME:
      raise
    import pathlib as _pathlib, runpy as _runpy
    
    _runpy.run_path(
      next(
        filter(
          _pathlib.Path.is_file,
          (_dir / f'{_TARGET_NAME}.py'
           for _dir in _pathlib.Path(__file__).resolve().parents),
        ),
        f'{_TARGET_NAME} not found',
      ))
```


# 📝 2026/11/09

いや、root ディレクトリに`bootstrap.py` は、意味なさすぎ？
わざわざトップに顔を出す必要あるか？

a-shell で、`python -m app` 実行すると、親ディレクトリを拾う。


```
hoge
file_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/app/__main__.py
hoge_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/bootstrap.py

sys.path:
---
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python313.zip
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13/lib-dynload
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13/site-packages

```


```
hoge
file_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/app/__main__.py
hoge_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/bootstrap.py

sys.path:
---
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/app
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python313.zip
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13/lib-dynload
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13/site-packages

```



```
hoge
file_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/app/__main__.py
hoge_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/bootstrap.py

sys.path:
---
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/app
---
/private/var/mobile/Containers/Shared/AppGroup//Pythonista3/Documents/site-packages-3
---
/private/var/mobile/Containers/Shared/AppGroup//Pythonista3/Documents/site-packages
---
/var/containers/Bundle/Application//Pythonista3.app/Frameworks/Py3Kit.framework/pylib
---
/var/containers/Bundle/Application//Pythonista3.app/Frameworks/Py3Kit.framework/pylib/site-packages
---
/var/containers/Bundle/Application//Pythonista3.app/Frameworks/Py3Kit.framework/pylib/site-packages/pythonista
---
/var/containers/Bundle/Application//Pythonista3.app/Frameworks/Py3Kit.framework/pylib/site-packages/PIL_compat


```


# 📝 2026/11/08

`bootstrap.py` から、module をいい感じに取り回す。

今までは、`playground` としていだが、`app` ？`src` ？

UIKitCatalog なら、`catalog` とかにするかな？

# 📝 2026/11/27

## プロジェクト内module の取得

一旦これで着地かな？


### 概要というか、意図というか、、、

- `bootstrap.py` をtop ディレクトリに置く
- コード実行時、真っ先に読み込ませる

全体的に:

- inspector に無駄な情報を出したくない
  - 「無駄」とは、bootstrap を使いローカルmodule をimport できるようにする処理の形跡のこと
- 実行ファイル側のボイラーテンプレートをできるだけ簡素にする
  - 何をしてるのか？は、判断できる程度に




### コード

#### `./bootstrap.py`


```python
# Pythonista3 直接実行用、もろもろのpath の依存関係を通す
import sys
import pathlib

# main とする作業ディレクトリ名`$ python -m app` としたいところ
_SRC_DIR_NAME = 'app'
# リポジトリ的にtop 階層となるディレクトリ名
_ROOT_DIR_NAME = 'modulesBootstrap'
# 取り込みたいmodule 一式が格納されてるディレクトリ名
_MODULES_DIR_NAME = 'pystaRubiconModules'


def _insert(path: pathlib.Path) -> None:
  sys.path.insert(0, str(path))


def _setup_module(
  dir_path: pathlib.Path,
  module_name: str,
) -> None:
  if (module_path := dir_path / module_name).exists():
    _insert(module_path)

  else:
    raise ModuleNotFoundError(f'{module_path}')


def _main(file_path: str) -> None:
  try:
    _dir_path = next((p for _p in pathlib.Path(file_path).resolve().parents
                      if (p := _p).name == _ROOT_DIR_NAME), )
  except StopIteration:
    raise FileNotFoundError(f'./{_ROOT_DIR_NAME} not found')

  _setup_module(_dir_path, _MODULES_DIR_NAME)
  _setup_module(_dir_path, _SRC_DIR_NAME)


# todo: 副作用的に実行
_main(__file__)


```


#### 実行したいファイルの先頭

```python
# `bootstrap.py` ファイルを`bootstrap` としてimport したい場合
if __name__ == '__main__':
  try:
    import bootstrap

  except ModuleNotFoundError:
    import pathlib, runpy

    _SCRIPT_NAME = 'bootstrap.py'
    try:
      next(_script_path for _dir in pathlib.Path(__file__).resolve().parents
           if (_script_path := _dir / _SCRIPT_NAME).is_file())
    except StopIteration:
      raise FileNotFoundError(f'{_SCRIPT_NAME} not found')

    runpy.run_path(_script_path)
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

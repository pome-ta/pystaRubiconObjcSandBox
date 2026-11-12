# Pythonista3 直接実行用、もろもろのpath の依存関係を通す
import sys
import pathlib
from pprint import pprint

_SRC_DIR_NAME = 'app'
_ROOT_DIR_NAME = 'modulesBootstrap'
_MODULES_DIR_NAME = 'pystaRubiconModules'


def _clear_local_modules(
  base_dir: pathlib.Path,
  *dir_names: str,
) -> list[str]:
  """
  実行スクリプトと同じ階層の指定ディレクトリ（複数可）配下から
  読み込まれたモジュールのキャッシュを一括で削除する
  """

  # ターゲットディレクトリをすべて絶対パス化
  resolved_targets = [(base_dir / name).resolve() for name in dir_names]

  keys_to_delete = []

  for name, module in sys.modules.items():

    # 実ファイルを持たないモジュール(組み込み等)はスキップ (importに失敗した残骸(None)はスキップ)
    if not (mod_file := getattr(module, '__file__', None)):
      continue

    # パスを解決(シンボリックリンクなどを排除した絶対パス化)
    mod_path = pathlib.Path(mod_file).resolve()

    # 指定したターゲットディレクトリのいずれかの配下にあるか判定
    if any(mod_path.is_relative_to(t) for t in resolved_targets):
      keys_to_delete.append(name)

  # 該当したモジュールを sys.modules から一括削除
  for k in keys_to_delete:
    del sys.modules[k]
    #pass

  # 削除したモジュール名を返す(デバッグ確認用)
  return keys_to_delete


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
  '''
  if _dir_path is None:
    raise FileNotFoundError(f'./{_ROOT_DIR_NAME} not found')
  '''
  cache=_clear_local_modules(_dir_path, _MODULES_DIR_NAME, _SRC_DIR_NAME)
  _setup_module(_dir_path, _MODULES_DIR_NAME)
  _setup_module(_dir_path, _SRC_DIR_NAME)
  
  pprint(cache)
  '''

  for _dir_path in pathlib.Path(file_path).resolve().parents:
    if _dir_path.name != _ROOT_DIR_NAME:
      continue
    _setup_module(_dir_path, _MODULES_DIR_NAME)
    _setup_module(_dir_path, _DEV_DIR_NAME)
    break
  else:
    import warnings
    with warnings.catch_warnings():
      warnings.simplefilter('always', ImportWarning)
      __warning_message = f'./{_ROOT_DIR_NAME}/{_MODULES_DIR_NAME} not found in parent directories'
      warnings.warn(__warning_message, ImportWarning)
  '''


# todo: 副作用的に実行
_main(__file__)



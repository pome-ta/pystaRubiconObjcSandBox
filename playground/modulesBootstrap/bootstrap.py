# Pythonista3 直接実行用、もろもろのpath の依存関係を通す
import sys
import pathlib

_SRC_DIR_NAME = 'app'
_ROOT_DIR_NAME = 'modulesBootstrap'
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


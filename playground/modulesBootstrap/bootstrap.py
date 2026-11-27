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


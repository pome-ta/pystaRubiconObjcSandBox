
if __name__ == '__main__':
  try:
    import bootstrap

  except ModuleNotFoundError:
    import pathlib as _pathlib, runpy as _runpy

    _SCRIPT_NAME = 'bootstrap.py'
    try:
      next(_script_path for _dir in _pathlib.Path(__file__).resolve().parents
           if (_script_path := _dir / _SCRIPT_NAME).is_file())
    except StopIteration:
      raise FileNotFoundError(f'{_SCRIPT_NAME} not found')

    _runpy.run_path(_script_path)

from py_utils.add_prototype_decorator import (
  CellPrototype,
  create_prototype_decorator,
)

from py_utils.storyboard_prototype import PrototypeTableViewCell

prototypes: list[CellPrototype] = []
add_prototype = create_prototype_decorator(prototypes)


import sys


for p in sys.path:
  print('')
  print(p)

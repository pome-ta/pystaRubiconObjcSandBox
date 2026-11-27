if __name__ == '__main__':
  try:
    import bootstrap

  except ModuleNotFoundError as e:
    if e.name != 'bootstrap':
      raise

    import pathlib as _pathlib, runpy as _runpy

    _SCRIPT_NAME = 'bootstrap.py'
    _runpy.run_path(
      next(
        filter(
          _pathlib.Path.is_file,
          (_dir / _SCRIPT_NAME
           for _dir in _pathlib.Path(__file__).resolve().parents),
        ),
        f'{_SCRIPT_NAME} not found',
      ))

from py_utils.add_prototype_decorator import (
  CellPrototype,
  create_prototype_decorator,
)

from py_utils.storyboard_prototype import PrototypeTableViewCell

prototypes: list[CellPrototype] = []
add_prototype = create_prototype_decorator(prototypes)


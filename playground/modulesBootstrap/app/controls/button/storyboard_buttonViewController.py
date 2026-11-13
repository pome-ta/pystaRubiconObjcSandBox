if __name__ == '__main__':
  try:
    import bootstrap
    
  except ModuleNotFoundError:
    import pathlib, importlib.util
    
    _BOOTSTRAP_NAME = 'bootstrap.py'

    def _bootsetup(file_path: str) -> None:
      _spec = importlib.util.spec_from_file_location(
        _BOOTSTRAP_NAME,
        next((p for _p in pathlib.Path(__file__).resolve().parents
              if (p := _p / _BOOTSTRAP_NAME).is_file()), None))
      _spec.loader.exec_module(importlib.util.module_from_spec(_spec))

    _bootsetup(__file__)

from py_utils.add_prototype_decorator import (
  CellPrototype,
  create_prototype_decorator,
)

from py_utils.storyboard_prototype import PrototypeTableViewCell

prototypes: list[CellPrototype] = []
add_prototype = create_prototype_decorator(prototypes)


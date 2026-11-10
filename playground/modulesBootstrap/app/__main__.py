if __name__ == '__main__':
  try:
    import bootstrap
  except ModuleNotFoundError:
    import pathlib
    import importlib.util

    _BOOTSTRAP_NAME = 'bootstrap.py'

    def _bootsetup(file_path: str) -> None:

      _path = next((p for _p in pathlib.Path(__file__).resolve().parents
                    if (p := _p / _BOOTSTRAP_NAME).is_file()), None)
      _spec = importlib.util.spec_from_file_location(_BOOTSTRAP_NAME, _path)
      bootstrap = importlib.util.module_from_spec(_spec)
      _spec.loader.exec_module(bootstrap)

    _bootsetup(__file__)


from pyrubicon.objc.api import ObjCClass, ObjCProtocol

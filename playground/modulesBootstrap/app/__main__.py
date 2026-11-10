if __name__ == '__main__':
  try:
    import bootstrap
  except ModuleNotFoundError:
    import pathlib
    import importlib.util

    _MODULE_NAME = 'bootstrap.py'
    __parent = pathlib.Path(__file__).resolve().parent
    __target = next((__p / _MODULE_NAME
                     for __p in [__parent, *__parent.parents]
                     if (__p / _MODULE_NAME).is_file()), None)
    __spec = importlib.util.spec_from_file_location(_MODULE_NAME, __target)
    bootstrap = importlib.util.module_from_spec(__spec)
    __spec.loader.exec_module(bootstrap)
'''
from pathlib import Path
import importlib.util

name = 'bootstrap.py'

target = next(
  (p / name for p in
   [Path(__file__).resolve().parent, *Path(__file__).resolve().parent.parents]
   if (p / name).is_file()), None)

#print(target)

file_path = target

spec = importlib.util.spec_from_file_location(name, file_path)
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


import bootstrap

bootstrap.hoge(__file__)
'''
print('')
print('---main')


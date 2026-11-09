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
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

module.hoge(__file__)


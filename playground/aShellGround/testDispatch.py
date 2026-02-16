_TOP_DIR_NAME = 'pystaRubiconObjcSandBox'
_MODULES_DIR_NAME = 'modules'

# todo: `./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME}` にあるpackage のimport 準備
if __name__ == '__main__' and not __file__[:__file__.rfind('/')].endswith(
    _TOP_DIR_NAME):
  import pathlib
  import sys
  __parents = pathlib.Path(__file__).resolve().parents
  for __dir_path in __parents:
    if __dir_path.name == _TOP_DIR_NAME and (__modules_path := __dir_path /
                                             _MODULES_DIR_NAME).exists():
      sys.path.insert(0, str(__modules_path))
      break
  else:
    import warnings
    with warnings.catch_warnings():
      warnings.simplefilter('always', ImportWarning)
      __warning_message = f'./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME} not found in parent directories'
      warnings.warn(__warning_message, ImportWarning)

import ctypes
from pyrubicon.objc.runtime import libobjc, load_library
from rbedge import pdbr
Dispatch = load_library('dispatch')

#pdbr.state(libobjc)
print(libobjc)

_libdispatch = 1

'''
def dispatch_semaphore_create(value: int) -> ObjCInstance:

  func = _libdispatch.dispatch_semaphore_create

  # --- Lazy Initialization ---
  if not func.argtypes:
    func.restype = objc_id  # 戻り値はオブジェクト
    func.argtypes = [c_long]  # 引数は long
  # ---------------------------

  ptr = func(value)
  if ptr is None:
    return None
  return ObjCInstance(ptr)
'''

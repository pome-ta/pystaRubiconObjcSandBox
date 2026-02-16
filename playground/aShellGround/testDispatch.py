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
from pyrubicon.objc.api import Block, ObjCClass, ObjCInstance
from pyrubicon.objc.runtime import libobjc, objc_block, objc_id, load_library
from rbedge import pdbr
#Dispatch = load_library('dispatch')

#pdbr.state(libobjc)
#print(libobjc)

#_libdispatch = 1
dispatch_time_t = ctypes.c_uint64

# DISPATCH_TIME_FOREVER (~0ull)
DISPATCH_TIME_FOREVER = dispatch_time_t(2**64 - 1)  # ~0ull
DISPATCH_TIME_NOW = dispatch_time_t(0)


def dispatch_semaphore_create(value: int) -> ObjCInstance:
  _function = libobjc.dispatch_semaphore_create
  if not _function.argtypes:
    _function.restype = objc_id
    _function.argtypes = [
      ctypes.c_long,
    ]

  _ptr = _function(value)
  if _ptr is None:
    return None
  return ObjCInstance(_ptr)


def dispatch_semaphore_wait(dsema: ObjCInstance, timeout: int = None) -> int:
  _function = libobjc.dispatch_semaphore_wait

  if not _function.argtypes:
    _function.restype = ctypes.c_long
    _function.argtypes = [
      objc_id,
      ctypes.c_uint64,
    ]

  t = DISPATCH_TIME_FOREVER if timeout is None else ctypes.c_uint64(timeout)

  return _function(dsema, t)


def dispatch_semaphore_signal(dsema: ObjCInstance) -> int:
  _function = libobjc.dispatch_semaphore_signal

  if not _function.argtypes:
    _function.restype = ctypes.c_long
    _function.argtypes = [
      objc_id,
    ]

  return _function(dsema)


if __name__ == '__main__':
  sema = dispatch_semaphore_create(0)

  print("Waiting...")

  # --- 本来は別のスレッドで実行する処理 ---
  def worker():
    import time
    time.sleep(2)
    print("Signaling!")
    dispatch_semaphore_signal(sema)

  import threading

  threading.Thread(target=worker).start()
  # ------------------------------------

  # 待機: signal が来るまでここで止まる
  result = dispatch_semaphore_wait(sema)

  print(f"Finished! (Result: {result})")


import ctypes
import functools

from pyrubicon.objc.api import ObjCInstance
from pyrubicon.objc.runtime import libobjc, objc_id

dispatch_time_t = ctypes.c_uint64

# DISPATCH_TIME_FOREVER (~0ull)
DISPATCH_TIME_FOREVER = dispatch_time_t(2**64 - 1)  # ~0ull
DISPATCH_TIME_NOW = dispatch_time_t(0)


class struct_dispatch_queue_s(ctypes.Structure):
  pass  # No _fields_, because this is an opaque structure.


_dispatch_main_q = struct_dispatch_queue_s.in_dll(libobjc, '_dispatch_main_q')


def dispatch_get_main_queue():
  return ObjCInstance(ctypes.cast(ctypes.byref(_dispatch_main_q), objc_id))


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

  t = DISPATCH_TIME_FOREVER if timeout is None else timeout

  return _function(dsema, t)


def dispatch_semaphore_signal(dsema: ObjCInstance) -> int:
  _function = libobjc.dispatch_semaphore_signal

  if not _function.argtypes:
    _function.restype = ctypes.c_long
    _function.argtypes = [
      objc_id,
    ]

  return _function(dsema)


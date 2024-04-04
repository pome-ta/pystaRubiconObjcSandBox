from ctypes import byref, cast, Structure, c_void_p


from pyrubicon.objc import ObjCInstance
from pyrubicon.objc.runtime import objc_id, load_library


class struct_dispatch_queue_s(Structure):
  pass  # No _fields_, because this is an opaque structure.


libSystem = load_library('System')
libdispatch = libSystem

_dispatch_sync = libdispatch.dispatch_sync
_dispatch_sync.restype = c_void_p
_dispatch_sync.argtypes = [c_void_p, c_void_p]

_dispatch_main_q = struct_dispatch_queue_s.in_dll(libdispatch,
                                                  '_dispatch_main_q')


def dispatch_get_main_queue():
  return ObjCInstance(cast(byref(_dispatch_main_q), objc_id))


def dispatch_sync(block_func):
  _dispatch_sync(dispatch_get_main_queue(), block_func)

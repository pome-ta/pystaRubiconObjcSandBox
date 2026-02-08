import ctypes

from pyrubicon.objc.api import ObjCInstance

from .constants import Metal


def MTLCreateSystemDefaultDevice() -> ObjCInstance:
  _function = Metal.MTLCreateSystemDefaultDevice
  _function.restype = ctypes.c_void_p
  return ObjCInstance(_function())


import ctypes

from pyrubicon.objc.api import ObjCInstance
from pyrubicon.objc.runtime import Foundation, Class


def NSStringFromClass(cls: Class) -> ObjCInstance:
  '''
  ref: [NSObjCRuntime.rs - source](https://docs.rs/objc2-foundation/latest/src/objc2_foundation/generated/NSObjCRuntime.rs.html#382-389)
  '''
  _NSStringFromClass = Foundation.NSStringFromClass
  _NSStringFromClass.restype = ctypes.c_void_p
  _NSStringFromClass.argtypes = [Class]
  return ObjCInstance(_NSStringFromClass(cls))


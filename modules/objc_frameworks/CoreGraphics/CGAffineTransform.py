import ctypes

from pyrubicon.objc.api import ObjCInstance
from pyrubicon.objc.types import CGFloat

from .constants import CoreGraphics


def CGAffineTransformMakeScale(sx: CGFloat, sy: CGFloat) -> ObjCInstance:
  _function = CoreGraphics.CGAffineTransformMakeScale
  _function.restype = ctypes.c_void_p
  _function.argtypes = [
    CGFloat,
    CGFloat,
  ]
  return ObjCInstance(_function(sx, sy))

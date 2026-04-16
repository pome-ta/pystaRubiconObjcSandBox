import ctypes

from pyrubicon.objc.types import CGPoint, CGRect
from .constants import framework as CoreGraphics

CGPointZero = CGPoint.in_dll(CoreGraphics, 'CGPointZero')
CGRectZero = CGRect.in_dll(CoreGraphics, 'CGRectZero')


def CGRectIntersectsRect(rect1: CGRect, rect2: CGRect) -> bool:
  try:
    _func = CGRectIntersectsRect._cfunc
  except AttributeError:
    _func = CoreGraphics.CGRectIntersectsRect
    _func.restype = ctypes.c_bool
    _func.argtypes = [
      CGRect,
      CGRect,
    ]
    CGRectIntersectsRect._cfunc = _func

  return _func(rect1, rect2)


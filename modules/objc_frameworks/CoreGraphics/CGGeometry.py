import ctypes

from pyrubicon.objc.types import CGPoint, CGRect
from .constants import framework as CoreGraphics

CGPointZero = CGPoint.in_dll(CoreGraphics, 'CGPointZero')
CGRectZero = CGRect.in_dll(CoreGraphics, 'CGRectZero')


def CGRectGetMinX(rect: CGRect) -> float:
  try:
    _func = CGRectGetMinX._cfunc
  except AttributeError:
    _func = CoreGraphics.CGRectGetMinX
    _func.restype = ctypes.c_float
    _func.argtypes = [
      CGRect,
    ]
    CGRectGetMinX._cfunc = _func

  return float(_func(rect))


def CGRectGetMidX(rect: CGRect) -> float:
  try:
    _func = CGRectGetMinX._cfunc
  except AttributeError:
    _func = CoreGraphics.CGRectGetMidX
    _func.restype = ctypes.c_float
    _func.argtypes = [
      CGRect,
    ]
    CGRectGetMidX._cfunc = _func

  return float(_func(rect))


def CGRectGetMaxX(rect: CGRect) -> float:
  try:
    _func = CGRectGetMaxX._cfunc
  except AttributeError:
    _func = CoreGraphics.CGRectGetMaxX
    _func.restype = ctypes.c_float
    _func.argtypes = [
      CGRect,
    ]
    CGRectGetMaxX._cfunc = _func

  return float(_func(rect))


def CGRectGetMinY(rect: CGRect) -> float:
  try:
    _func = CGRectGetMinY._cfunc
  except AttributeError:
    _func = CoreGraphics.CGRectGetMinY
    _func.restype = ctypes.c_float
    _func.argtypes = [
      CGRect,
    ]
    CGRectGetMinY._cfunc = _func

  return float(_func(rect))


def CGRectGetMidY(rect: CGRect) -> float:
  try:
    _func = CGRectGetMinY._cfunc
  except AttributeError:
    _func = CoreGraphics.CGRectGetMidY
    _func.restype = ctypes.c_float
    _func.argtypes = [
      CGRect,
    ]
    CGRectGetMidY._cfunc = _func

  return float(_func(rect))


def CGRectGetMaxY(rect: CGRect) -> float:
  try:
    _func = CGRectGetMaxY._cfunc
  except AttributeError:
    _func = CoreGraphics.CGRectGetMaxY
    _func.restype = ctypes.c_float
    _func.argtypes = [
      CGRect,
    ]
    CGRectGetMaxY._cfunc = _func

  return float(_func(rect))


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


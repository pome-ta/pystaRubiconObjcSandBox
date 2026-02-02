import ctypes

from pyrubicon.objc.types import CGFloat
from pyrubicon.objc.types import __LP64__, with_preferred_encoding

from .constants import CoreGraphics

if __LP64__:
  _CGAffineTransformEncoding = b'{CGAffineTransform=dddddd}'
else:
  _CGAffineTransformEncoding = b'{CGAffineTransform=ffffff}'


@with_preferred_encoding(_CGAffineTransformEncoding)
class CGAffineTransform(ctypes.Structure):

  _fields_ = [
    ('a', CGFloat),
    ('b', CGFloat),
    ('c', CGFloat),
    ('d', CGFloat),
    ('tx', CGFloat),
    ('ty', CGFloat),
  ]

  def __repr__(self):
    return f'<CGAffineTransform({self.a}, {self.b}, {self.c}, {self.d}, {self.tx}, {self.ty})>'

  def __str__(self):
    return f'a={self.a}, b={self.b}, c={self.c}, d={self.d}, tx={self.tx}, ty={self.ty}'


CGAffineTransformIdentity = CGAffineTransform.in_dll(
  CoreGraphics, 'CGAffineTransformIdentity')


def CGAffineTransformMakeScale(sx: CGFloat, sy: CGFloat) -> CGAffineTransform:
  _function = CoreGraphics.CGAffineTransformMakeScale
  _function.restype = CGAffineTransform
  _function.argtypes = [
    CGFloat,
    CGFloat,
  ]
  return _function(sx, sy)


def CGAffineTransformTranslate(t: CGAffineTransform, sx: CGFloat,
                           sy: CGFloat) -> CGAffineTransform:
  _function = CoreGraphics.CGAffineTransformTranslate
  _function.restype = CGAffineTransform
  _function.argtypes = [
    CGAffineTransform,
    CGFloat,
    CGFloat,
  ]
  return _function(t, sx, sy)


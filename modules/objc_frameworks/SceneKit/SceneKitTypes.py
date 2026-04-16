import ctypes

from pyrubicon.objc.types import CGFloat
from pyrubicon.objc.types import __LP64__, with_preferred_encoding

if __LP64__:
  _SCNVector3Encoding = b'{SCNVector3=ddd}'
else:
  _SCNVector3Encoding = b'{SCNVector3=fff}'


@with_preferred_encoding(_SCNVector3Encoding)
class SCNVector3(ctypes.Structure):
  _fields_ = [
    ('x', CGFloat),
    ('y', CGFloat),
    ('z', CGFloat),
  ]


import ctypes
'''
from pyrubicon.objc.types import with_preferred_encoding

_MTLClearColorEncoding = b'{MTLClearColor=dddd}'


@with_preferred_encoding(_MTLClearColorEncoding)
class MTLClearColor(ctypes.Structure):

  _fields_ = [
    ('red', ctypes.c_double),
    ('green', ctypes.c_double),
    ('blue', ctypes.c_double),
    ('alpha', ctypes.c_double),
  ]

  def __repr__(self):
    return f'<MTLClearColor({self.red}, {self.green}, {self.blue}, {self.alpha})>'

  def __str__(self):
    return f'red={self.red}, green={self.green}, blue={self.blue}, alpha={self.alpha}'


def MTLClearColorMake(red: ctypes.c_double, green: ctypes.c_double,
                      blue: ctypes.c_double,
                      alpha: ctypes.c_double) -> MTLClearColor:
  return MTLClearColor(red, green, blue, alpha)
'''


def MTLClearColorMake(red: ctypes.c_double, green: ctypes.c_double,
                      blue: ctypes.c_double, alpha: ctypes.c_double) -> tuple:
  return (red, green, blue, alpha)


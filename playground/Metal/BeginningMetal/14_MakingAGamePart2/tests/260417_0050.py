"""
CGRectZero
CGRectIntersectsRect
"""

_TOP_DIR_NAME = 'pystaRubiconObjcSandBox'
_MODULES_DIR_NAME = 'modules'

# todo: `./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME}` にあるpackage のimport 準備
if __name__ == '__main__' and not __file__[:__file__.rfind('/')].endswith(
    _TOP_DIR_NAME):
  import pathlib
  import sys
  __parents = pathlib.Path(__file__).resolve().parents
  for __dir_path in __parents:
    if __dir_path.name == _TOP_DIR_NAME and (__modules_path := __dir_path /
                                             _MODULES_DIR_NAME).exists():
      sys.path.insert(0, str(__modules_path))
      break
  else:
    import warnings
    with warnings.catch_warnings():
      warnings.simplefilter('always', ImportWarning)
      __warning_message = f'./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME} not found in parent directories'
      warnings.warn(__warning_message, ImportWarning)

  sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'final'))
  #sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'challenge'))

import ctypes
from pyrubicon.objc.types import CGFloat, CGRect, CGRectMake

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from rbedge import pdbr

from objc_frameworks.CoreGraphics import CGRectZero, CGRectIntersectsRect

zero1 = CGRectMake(1,0,-1,1)
zero2 = CGRectZero
#pdbr.state(zero)
print(CGRectIntersectsRect(zero1, zero2))

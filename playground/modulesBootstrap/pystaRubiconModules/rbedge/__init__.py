__version__ = '0.0.0'

import sys
import os
import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCProtocol, ObjCInstance
from pyrubicon.objc.runtime import Foundation

ObjCClass.auto_rename = True
ObjCProtocol.auto_rename = True

#######################################################
# --- exception
#######################################################
# ref: from objc_util.py of Pythonista3 module
ExceptionHandlerFuncType = ctypes.CFUNCTYPE(None, ctypes.c_void_p)


def NSSetUncaughtExceptionHandler(_exc: ExceptionHandlerFuncType) -> None:
  _NSSetUncaughtExceptionHandler = Foundation.NSSetUncaughtExceptionHandler
  _NSSetUncaughtExceptionHandler.restype = None
  _NSSetUncaughtExceptionHandler.argtypes = [
    ExceptionHandlerFuncType,
  ]
  _NSSetUncaughtExceptionHandler(_exc)


def _objc_exception_handler(_exc):
  exc = ObjCInstance(_exc)
  _path_str = '~/Documents/_rubicon_objc_exception.txt'
  with open(os.path.expanduser(_path_str), 'w') as f:
    from datetime import datetime
    f.write(
      'The app was terminated due to an Objective-C exception. Details below:\n\n%s\n%s\n'
      % (datetime.now(), exc))


_handler = ExceptionHandlerFuncType(_objc_exception_handler)
NSSetUncaughtExceptionHandler(_handler)
#######################################################


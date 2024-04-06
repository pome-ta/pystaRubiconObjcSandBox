import sys
import ctypes


_tracefunc = None

def settrace(func):
  # used for on_main_thread()
  global _tracefunc
  _tracefunc = func



IMPTYPE = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)

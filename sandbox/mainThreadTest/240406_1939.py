import sys
from pyrubicon.objc.api import ObjCClass
import pdbr

PY3 = sys.version_info[0] >= 3

OMMainThreadDispatcher_name = b'OMMainThreadDispatcher_3' if PY3 else 'OMMainThreadDispatcher'

try:
  OMMainThreadDispatcher = ObjCClass(OMMainThreadDispatcher_name)
except ValueError:
  IMPTYPE = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)
  imp = IMPTYPE(OMMainThreadDispatcher_invoke_imp)
  retain_global(imp)
  NSObject = ObjCClass('NSObject')
  class_ptr = objc_allocateClassPair(NSObject.ptr, OMMainThreadDispatcher_name,
                                     0)
  class_addMethod(class_ptr, sel('invoke'), imp, b'v16@0:0')
  objc_registerClassPair(class_ptr)
  OMMainThreadDispatcher = ObjCClass(OMMainThreadDispatcher_name)

pdbr.state(OMMainThreadDispatcher.new())


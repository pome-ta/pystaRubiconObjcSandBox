import ctypes
#from ctypes import cdll, c_void_p, c_uint, byref

from rubicon.objc import ObjCClass, objc_method
from rubicon.objc.runtime import send_super

from dispatchSync import dispatch_sync

import pdbr

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
NSString = ObjCClass('NSString')



class TopViewController(UIViewController, auto_rename=True):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.view.backgroundColor = UIColor.systemDarkRedColor()


NSObject = ObjCClass('NSObject')
#print(dir(NSObject))
#print(NSObject.ptr.value)

c = ctypes.cdll.LoadLibrary(None)

object_getClass = c.object_getClass
object_getClass.argtypes = [ctypes.c_void_p]
object_getClass.restype = ctypes.c_void_p

class_copyMethodList = c.class_copyMethodList
class_copyMethodList.restype = ctypes.POINTER(ctypes.c_void_p)
class_copyMethodList.argtypes = [
  ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)
]

method_getName = c.method_getName
method_getName.restype = ctypes.c_void_p
method_getName.argtypes = [ctypes.c_void_p]

sel_getName = c.sel_getName
sel_getName.restype = ctypes.c_char_p
sel_getName.argtypes = [ctypes.c_void_p]

class_getSuperclass = c.class_getSuperclass
class_getSuperclass.restype = ctypes.c_void_p
class_getSuperclass.argtypes = [ctypes.c_void_p]

free = c.free
free.argtypes = [ctypes.c_void_p]
free.restype = None

NSObject_instance_methods = [
  'init',
  'copy',
  'mutableCopy',
  'dealloc',
  'performSelector_withObject_afterDelay_',
  'performSelectorOnMainThread_withObject_waitUntilDone_',
  'performSelectorInBackground_withObject_',
]

vc = TopViewController.new()
#print(vc._cached_objects)
#print(object_getClass(vc.ptr.value))


def pr_dir(ins):
  objc_class_ptr = object_getClass(ins.ptr.value)
  py_methods = []

  while objc_class_ptr is not None:
    num_methods = ctypes.c_uint(0)
    method_list_ptr = class_copyMethodList(objc_class_ptr,
                                           ctypes.byref(num_methods))
    print(num_methods)
    print(dir())
    for i in range(num_methods.value):
      selector = method_getName(method_list_ptr[i])

      sel_name = sel_getName(selector).decode('ascii')
      #sel_name = sel_name.decode('ascii')
      py_method_name = sel_name.replace(':', '_')

      if '.' not in py_method_name:
        py_methods.append(py_method_name)

    free(method_list_ptr)
    objc_class_ptr = class_getSuperclass(objc_class_ptr)
    print(objc_class_ptr)
    if objc_class_ptr == NSObject.ptr.value:
      py_methods += NSObject_instance_methods
      break
    return sorted(set(py_methods))


a = pr_dir(NSString)
from pprint import pprint
#pprint(a)

'''
def __dir__(self):
		objc_class_ptr = object_getClass(self.ptr)
		py_methods = []
		while objc_class_ptr is not None:
			num_methods = c_uint(0)
			method_list_ptr = class_copyMethodList(objc_class_ptr, byref(num_methods))
			for i in xrange(num_methods.value):
				selector = method_getName(method_list_ptr[i])
				sel_name = sel_getName(selector)
				if PY3:
					sel_name = sel_name.decode('ascii')
				py_method_name = sel_name.replace(':', '_')
				if '.' not in py_method_name:
					py_methods.append(py_method_name)
			free(method_list_ptr)
			# Walk up the class hierarchy to add methods from superclasses:
			objc_class_ptr = class_getSuperclass(objc_class_ptr)
			if objc_class_ptr == NSObject.ptr:
				# Don't list all NSObject methods (too much cruft from categories...)
				py_methods += NSObject_instance_methods
				break
		return sorted(set(py_methods))

	
'''


import ctypes
from pyrubicon.objc import ObjCClass, NSObject, ObjCInstance
from pyrubicon.objc.runtime import libobjc

from pprint import pprint

NSObject_instance_methods = [
  'init',
  'copy',
  'mutableCopy',
  'dealloc',
  'performSelector_withObject_afterDelay_',
  'performSelectorOnMainThread_withObject_waitUntilDone_',
  'performSelectorInBackground_withObject_',
]


def objc_dir(obj):
  objct_class = libobjc.object_getClass(obj)
  py_methods = []

  while objct_class is not None:
    num_methods = ctypes.c_uint(0)
    method_list_ptr = libobjc.class_copyMethodList(objct_class,
                                                   ctypes.byref(num_methods))
    for i in range(num_methods.value):
      selector = libobjc.method_getName(method_list_ptr[i])
      sel_name = libobjc.sel_getName(selector).decode('ascii')
      py_method_name = sel_name.replace(':', '_')

      if '.' not in py_method_name:
        py_methods.append(py_method_name)
    libobjc.free(method_list_ptr)
    objct_class = libobjc.class_getSuperclass(objct_class)
    #print(ObjCInstance(objct_class.value))

    if objct_class.value == NSObject.ptr.value:
      py_methods += NSObject_instance_methods
      break
  return sorted(set(py_methods))


from pyrubicon.objc import ObjCClass, objc_method

UIViewController = ObjCClass('UIViewController')


class TopViewController(UIViewController, auto_rename=True):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.view.backgroundColor = UIColor.systemDarkRedColor()


vc = TopViewController  #.new()
#vc = UIViewController#.new()
a = objc_dir(vc)
#pprint(a)


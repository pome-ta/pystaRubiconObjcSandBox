import ctypes
import json
from pprint import pprint

from pyrubicon.objc.api import ObjCInstance, NSObject
from pyrubicon.objc.runtime import libobjc

__all__ = [
  'state',
]

NSObject_instance_methods = [
  'init',
  'copy',
  'mutableCopy',
  'dealloc',
  'performSelector_withObject_afterDelay_',
  'performSelectorOnMainThread_withObject_waitUntilDone_',
  'performSelectorInBackground_withObject_',
]


def _get_className_methods(rubicon_object, is_revers: bool = True):
  objct_class = libobjc.object_getClass(rubicon_object)
  py_className_methods = {}

  while objct_class is not None:
    py_methods = []
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

    py_className_methods[str(ObjCInstance(objct_class.value))] = sorted(
      set(py_methods))

    objct_class = libobjc.class_getSuperclass(objct_class)

    if objct_class.value == NSObject.ptr.value:
      py_className_methods[str(NSObject)] = NSObject_instance_methods
      break

  _items = py_className_methods.items()
  _list_items = list(reversed(_items) if is_revers else _items)
  return dict(_list_items)


def state(rubicon_obj, indent: int = 2, is_reverse: bool = True):
  _dic = _get_className_methods(rubicon_obj, is_reverse)
  data = json.dumps(_dic, indent=indent)
  print(data)
  pprint(rubicon_obj)


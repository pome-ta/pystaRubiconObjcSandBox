import ctypes
from rubicon.objc import ObjCClass, NSObject
from rubicon.objc.runtime import libobjc

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


def objins(obj):
  objct_class = libobjc.object_getClass(obj)
  print(objct_class)
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

    if objct_class.value == NSObject.ptr.value:
      py_methods += NSObject_instance_methods
      break
    return sorted(set(py_methods))


from rubicon.objc import ObjCClass, objc_method

UIViewController = ObjCClass('UIViewController')


class TopViewController(UIViewController, auto_rename=True):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.view.backgroundColor = UIColor.systemDarkRedColor()


#vc = TopViewController.new()
vc = UIViewController  #.new()
a = objins(vc)

pprint(a)

#print(dir(NSObject))
'''
<CDLL '/usr/lib/libobjc.dylib', handle 36244e708 at 0x11023f1f0>
['_FuncPtr',
 '__class__',
 '__delattr__',
 '__dict__',
 '__dir__',
 '__doc__',
 '__eq__',
 '__format__',
 '__ge__',
 '__getattr__',
 '__getattribute__',
 '__getitem__',
 '__gt__',
 '__hash__',
 '__init__',
 '__init_subclass__',
 '__le__',
 '__lt__',
 '__module__',
 '__ne__',
 '__new__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__setattr__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 '__weakref__',
 '_func_flags_',
 '_func_restype_',
 '_handle',
 '_name',
 'class_addIvar',
 'class_addMethod',
 'class_addProperty',
 'class_addProtocol',
 'class_conformsToProtocol',
 'class_copyIvarList',
 'class_copyMethodList',
 'class_copyPropertyList',
 'class_copyProtocolList',
 'class_getClassMethod',
 'class_getClassVariable',
 'class_getInstanceMethod',
 'class_getInstanceSize',
 'class_getInstanceVariable',
 'class_getIvarLayout',
 'class_getMethodImplementation',
 'class_getName',
 'class_getProperty',
 'class_getSuperclass',
 'class_getVersion',
 'class_getWeakIvarLayout',
 'class_isMetaClass',
 'class_replaceMethod',
 'class_respondsToSelector',
 'class_setIvarLayout',
 'class_setVersion',
 'class_setWeakIvarLayout',
 'ivar_getName',
 'ivar_getOffset',
 'ivar_getTypeEncoding',
 'method_exchangeImplementations',
 'method_getImplementation',
 'method_getName',
 'method_getTypeEncoding',
 'method_setImplementation',
 'objc_allocateClassPair',
 'objc_allocateProtocol',
 'objc_autoreleasePoolPop',
 'objc_autoreleasePoolPush',
 'objc_autoreleaseReturnValue',
 'objc_copyProtocolList',
 'objc_getAssociatedObject',
 'objc_getClass',
 'objc_getMetaClass',
 'objc_getProtocol',
 'objc_loadWeakRetained',
 'objc_registerClassPair',
 'objc_registerProtocol',
 'objc_removeAssociatedObjects',
 'objc_setAssociatedObject',
 'objc_storeWeak',
 'object_getClass',
 'object_getClassName',
 'object_getIvar',
 'object_isClass',
 'object_setIvar',
 'property_copyAttributeList',
 'property_getAttributes',
 'property_getName',
 'protocol_addMethodDescription',
 'protocol_addProperty',
 'protocol_addProtocol',
 'protocol_conformsToProtocol',
 'protocol_copyMethodDescriptionList',
 'protocol_copyPropertyList',
 'protocol_copyProtocolList',
 'protocol_getMethodDescription',
 'protocol_getName',
 'sel_getName',
 'sel_isEqual',
 'sel_registerName']


'''


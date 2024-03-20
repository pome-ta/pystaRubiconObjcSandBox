from rubicon.objc import ObjCClass, ObjCProtocol, objc_method
from rubicon.objc import Block
from rubicon.objc.runtime import libobjc,SEL, send_super

from dispatchSync import dispatch_sync

import pdbr

UINavigationController = ObjCClass('UINavigationController')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')
UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')


class TopViewController(UIViewController, auto_rename=True):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.view.backgroundColor = UIColor.systemDarkRedColor()


class WrapNavigationController(UINavigationController,
                               protocols=[UINavigationControllerDelegate],
                               auto_rename=True):

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated):
    appearance = UINavigationBarAppearance.alloc()
    appearance.configureWithDefaultBackground()

    navigationBar = navigationController.navigationBar
    navigationBar.standardAppearance = appearance
    navigationBar.scrollEdgeAppearance = appearance
    navigationBar.compactAppearance = appearance
    navigationBar.compactScrollEdgeAppearance = appearance

    viewController.setEdgesForExtendedLayout_(0)

    done_btn = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, navigationController,
                                                 SEL('doneButtonTapped:'))
    visibleViewController = navigationController.visibleViewController

    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = done_btn


vc = TopViewController.new()
print(vc._cached_objects)

def pr_dir(ins):
  pass



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

def main():
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  root_vc = window.rootViewController

  while root_vc.presentedViewController:
    root_vc = root_vc.presentedViewController

  #vc = TopViewController.new()
  #pdbr.state(vc)
  #print(vc._ivarDescription)
  #print(vc.objc_class)
  #print(dir(vc.objc_class))
  #vc.view.setBackgroundColor_(UIColor.systemDarkRedColor())
  #print(dir(vc))
  #print(vars(vc))
  #print(vc.__repr__())
  #print(vc)

  @Block
  def processing() -> None:
    nv = WrapNavigationController.alloc().initWithRootViewController_(vc)
    nv.delegate = nv
    nv.setModalPresentationStyle_(0)

    root_vc.presentViewController_animated_completion_(nv, True, None)

  #dispatch_sync(processing)


if __name__ == "__main__":
  main()


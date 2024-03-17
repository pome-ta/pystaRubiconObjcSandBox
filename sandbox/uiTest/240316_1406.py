from ctypes import byref, cast, Structure, c_void_p
import functools

from rubicon.objc import ObjCClass, ObjCProtocol, objc_method
from rubicon.objc import ObjCInstance, Block
from rubicon.objc.runtime import objc_id, load_library

import pdbr

libSystem = load_library('System')
libdispatch = libSystem

dispatch_sync = libdispatch.dispatch_sync
dispatch_sync.restype = c_void_p
dispatch_sync.argtypes = [c_void_p, c_void_p]


class struct_dispatch_queue_s(Structure):
  pass  # No _fields_, because this is an opaque structure.


_dispatch_main_q = struct_dispatch_queue_s.in_dll(libdispatch,
                                                  '_dispatch_main_q')


def dispatch_get_main_queue():
  return ObjCInstance(cast(byref(_dispatch_main_q), objc_id))


UINavigationController = ObjCClass('UINavigationController')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')
UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')


class NavigationController(UINavigationController,
                            protocols=[UINavigationControllerDelegate],
                            auto_rename=True):

  
  '''
  @objc_method
  def initWithRootViewController_(self, rootViewController):

    return self
  
    
  '''
  @objc_method
  def navigationController_willShowViewController_animated_(self, _navigationController, _viewController, _animated):
    print('h')



#nv.autorelease


def main() -> None:
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  root_vc = window.rootViewController

  while root_vc.presentedViewController:
    root_vc = root_vc.presentedViewController

  vc = UIViewController.new()
  vc.view.setBackgroundColor_(UIColor.systemDarkRedColor())
  vc.setModalPresentationStyle_(1)
  #nv = NavigationController.alloc().initWithRootViewController_(vc)
  #pdbr.state(UINavigationController.alloc())

  @Block
  def processing() -> None:
    nv = NavigationController.alloc().initWithRootViewController_(vc)
    root_vc.presentViewController_animated_completion_(nv, True, None)

  dispatch_sync(dispatch_get_main_queue(), processing)


main()
#del ANavigationController


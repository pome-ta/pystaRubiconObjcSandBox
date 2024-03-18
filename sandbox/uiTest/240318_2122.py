from ctypes import byref, cast, Structure, c_void_p
import functools

#from objc_util import on_main_thread

from rubicon.objc import ObjCClass, ObjCProtocol, objc_method
from rubicon.objc import ObjCInstance, Block
from rubicon.objc.runtime import objc_id, load_library, send_super, SEL

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


class MainNavigationController(UINavigationController,
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


def on_mainthread(func):
  @functools.wraps
  def _wrapper(*args, **kwargs):
    func(*args, **kwargs)
  return dispatch_sync(dispatch_get_main_queue(), Block(func))

'''
def main() -> None:
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  root_vc = window.rootViewController

  while root_vc.presentedViewController:
    root_vc = root_vc.presentedViewController

  vc = UIViewController.new()
  vc.view.setBackgroundColor_(UIColor.systemDarkRedColor())

  #@Block
  def processing() -> None:
    nv = MainNavigationController.alloc().initWithRootViewController_(vc)
    nv.delegate = nv
    nv.setModalPresentationStyle_(0)

    root_vc.presentViewController_animated_completion_(nv, True, None)

  #processing_block = Block(processing)
  #dispatch_sync(dispatch_get_main_queue(), processing)
  #dispatch_sync(dispatch_get_main_queue(), processing_block)
  dispatch_sync(dispatch_get_main_queue(), Block(processing))
'''
@on_mainthread
def main(v) -> None:
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  root_vc = window.rootViewController

  while root_vc.presentedViewController:
    root_vc = root_vc.presentedViewController

  vc = UIViewController.new()
  vc.view.setBackgroundColor_(UIColor.systemDarkRedColor())
  nv = MainNavigationController.alloc().initWithRootViewController_(vc)
  nv.delegate = nv
  nv.setModalPresentationStyle_(v)

  root_vc.presentViewController_animated_completion_(nv, True, None)

if __name__ == "__main__":
  main(0)


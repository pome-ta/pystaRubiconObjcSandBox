import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import objc_id, send_super, SEL

from rbedge import pdbr

ObjCClass.auto_rename = True

#############################################################
# --- lifeCycle
#############################################################

import asyncio

from pyrubicon.objc.eventloop import EventLoopPolicy

asyncio.set_event_loop_policy(EventLoopPolicy())
loop = asyncio.new_event_loop()

#############################################################
# --- mainThread
#############################################################
import functools
from pyrubicon.objc.runtime import libobjc, objc_block

NSThread = ObjCClass('NSThread')


class struct_dispatch_queue_s(ctypes.Structure):
  pass  # No _fields_, because this is an opaque structure.


_dispatch_main_q = struct_dispatch_queue_s.in_dll(libobjc, '_dispatch_main_q')


def dispatch_get_main_queue():
  return ObjCInstance(ctypes.cast(ctypes.byref(_dispatch_main_q), objc_id))


libobjc.dispatch_async.restype = None
libobjc.dispatch_async.argtypes = [
  objc_id,
  objc_block,
]


def onMainThread(func):

  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    if NSThread.isMainThread:
      func(*args, **kwargs)
    block = Block(functools.partial(func, *args, **kwargs), None)
    libobjc.dispatch_async(dispatch_get_main_queue(), block)

  return wrapper


#############################################################
# --- UINavigationController
#############################################################
UINavigationController = ObjCClass('UINavigationController')
UIBarButtonItem = ObjCClass('UIBarButtonItem')


class RootNavigationController(UINavigationController):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    loop.stop()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.delegate = self

  @objc_method
  def doneButtonTapped_(self, sender):
    self.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated: bool):
    viewController.setEdgesForExtendedLayout_(0)
    _UIBarButtonSystemItem_close = 24
    closeButtonItem = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(24, navigationController,
                                                 SEL('doneButtonTapped:'))
    visibleViewController = navigationController.visibleViewController

    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = closeButtonItem


#############################################################
# --- UIViewController
#############################################################
UIViewController = ObjCClass('UIViewController')


class MainViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = 'title'
    # todo: 処理を書く


#############################################################
# --- app present
#############################################################
UIApplication = ObjCClass('UIApplication')


class App:

  sharedApplication = UIApplication.sharedApplication
  __objectEnumerator = sharedApplication.connectedScenes.objectEnumerator()
  while (__windowScene := __objectEnumerator.nextObject()):
    if __windowScene.activationState == 0:
      break
  rootViewController = __windowScene.keyWindow.rootViewController

  def __init__(self, viewController, modalPresentationStyle=1):
    self.viewController = viewController
    self.modalPresentationStyle = modalPresentationStyle

  def present(self):

    @onMainThread
    def present_viewController(viewController: UIViewController,
                               style: int) -> None:

      presentViewController = RootNavigationController.alloc(
      ).initWithRootViewController_(viewController)

      presentViewController.setModalPresentationStyle_(style)

      self.rootViewController.presentViewController_animated_completion_(
        presentViewController, True, None)

    present_viewController(self.viewController, self.modalPresentationStyle)
    self.main_loop()

  def main_loop(self):
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
  main_vc = MainViewController.new()
  presentation_style = 1

  app = App(main_vc, presentation_style)
  app.present()


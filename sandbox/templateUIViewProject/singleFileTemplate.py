import sys
import os
import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import objc_id, send_super, SEL
# todo: utils ###############################################
from pyrubicon.objc.runtime import Class, Foundation
# todo: lifeCycle ###########################################
import asyncio
import logging
from pyrubicon.objc.eventloop import EventLoopPolicy
# todo: mainThread ##########################################
import functools
from pyrubicon.objc.runtime import libobjc, objc_block

ObjCClass.auto_rename = True


#############################################################
# --- utils
#############################################################
def NSStringFromClass(cls: Class) -> ObjCInstance:
  _NSStringFromClass = Foundation.NSStringFromClass
  _NSStringFromClass.restype = ctypes.c_void_p
  _NSStringFromClass.argtypes = [Class]
  return ObjCInstance(_NSStringFromClass(cls))


#############################################################
# --- exception
#############################################################
# todo: from objc_util.py of Pythonista3
ExceptionHandlerFuncType = ctypes.CFUNCTYPE(None, ctypes.c_void_p)


def NSSetUncaughtExceptionHandler(_exc: ExceptionHandlerFuncType) -> None:
  _NSSetUncaughtExceptionHandler = Foundation.NSSetUncaughtExceptionHandler
  _NSSetUncaughtExceptionHandler.restype = None
  _NSSetUncaughtExceptionHandler.argtypes = [
    ExceptionHandlerFuncType,
  ]
  _NSSetUncaughtExceptionHandler(_exc)


def _objc_exception_handler(_exc):
  exc = ObjCInstance(_exc)
  with open(os.path.expanduser('~/Documents/_rubicon_objc_exception.txt'),
            'w') as f:
    import datetime
    f.write(
      'The app was terminated due to an Objective-C exception. Details below:\n\n%s\n%s\n'
      % (datetime.datetime.now(), exc))


_handler = ExceptionHandlerFuncType(_objc_exception_handler)
NSSetUncaughtExceptionHandler(_handler)

#############################################################
# --- lifeCycle
#############################################################
#logging.basicConfig(level=logging.DEBUG)
asyncio.set_event_loop_policy(EventLoopPolicy())
loop = asyncio.new_event_loop()
#loop.set_debug(True)

#############################################################
# --- mainThread
#############################################################
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
    print(f'- {NSStringFromClass(__class__)}: dealloc')
    loop.stop()

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    print(f'{NSStringFromClass(__class__)}: loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    print(f'{NSStringFromClass(__class__)}: viewDidLoad')
    self.delegate = self

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'{NSStringFromClass(__class__)}: viewDidAppear_')
    print('↓ ---')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    print('↑ ---')
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'{NSStringFromClass(__class__)}: viewWillDisappear_')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'{NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  @objc_method
  def doneButtonTapped_(self, sender):
    print(f'{NSStringFromClass(__class__)}: doneButtonTapped:')

    self.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated: bool):
    #closeButtonItem = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(24, navigationController, SEL('doneButtonTapped:'))
    closeButtonItem = UIBarButtonItem.alloc().initWithBarButtonSystemItem(
      24, target=navigationController, action=SEL('doneButtonTapped:'))

    visibleViewController = navigationController.visibleViewController
    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = closeButtonItem


#############################################################
# --- UIViewController
#############################################################
UIViewController = ObjCClass('UIViewController')


class MainViewController(UIViewController):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t - {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    print(f'\t{NSStringFromClass(__class__)}: loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    print(f'\t{NSStringFromClass(__class__)}: viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__)

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'\t{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'\t{NSStringFromClass(__class__)}: viewDidAppear_')
    print('\t↓ ---')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    print('\t↑ ---')
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'\t{NSStringFromClass(__class__)}: viewWillDisappear_')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'\t{NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')


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
    def present_viewController(viewController: UIViewController, style: int):

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
  print('--- run ---')
  main_vc = MainViewController.new()
  presentation_style = 1

  app = App(main_vc, presentation_style)
  app.present()

  print('--- end ---')


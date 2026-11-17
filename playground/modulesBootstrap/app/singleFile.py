if __name__ == '__main__':
  try:
    import bootstrap

  except ModuleNotFoundError:
    import pathlib, runpy

    _SCRIPT_NAME = 'bootstrap.py'
    try:
      next(_script_path for _dir in pathlib.Path(__file__).resolve().parents
           if (_script_path := _dir / _SCRIPT_NAME).is_file())
    except StopIteration:
      raise FileNotFoundError(f'{_SCRIPT_NAME} not found')

    runpy.run_path(_script_path)

import ctypes

from pyrubicon.objc import (
  Block,
  ObjCClass,
  ObjCInstance,
  objc_method,
)  # api
from pyrubicon.objc import (
  SEL,
  objc_id,
  send_super,
)  # runtime
# todo: utils ###############################################
from pyrubicon.objc.runtime import Class, Foundation
# todo: lifeCycle ###########################################
import asyncio
import logging
from pyrubicon.objc.eventloop import RubiconEventLoop, iOSLifecycle, CFLifecycle
# todo: exception ###########################################
import sys
import os
# todo: mainThread ##########################################
import functools
from pyrubicon.objc import objc_block  # runtime
from pyrubicon.objc.runtime import load_library, libobjc
from rbedge import pdbr

ObjCClass.auto_rename = True

UIApplication = ObjCClass("UIApplication")
UIViewController = ObjCClass("UIViewController")
UIColor = ObjCClass("UIColor")
NSObject = ObjCClass("NSObject")

loop = RubiconEventLoop()

#############################################################
# --- mainThread
#############################################################
#libSystem = load_library('System')
NSThread = ObjCClass('NSThread')


class struct_dispatch_queue_s(ctypes.Structure):
  pass  # No _fields_, because this is an opaque structure.


_dispatch_main_q = struct_dispatch_queue_s.in_dll(libobjc, '_dispatch_main_q')
#_dispatch_main_q = struct_dispatch_queue_s.in_dll(libSystem, '_dispatch_main_q')

def dispatch_get_main_queue():
  return ObjCInstance(ctypes.cast(ctypes.byref(_dispatch_main_q), objc_id))




def dispatch_async(queue, block_obj:objc_block):
  try:
    _func = dispatch_async._cfunc
  except AttributeError:
    _func = libobjc.dispatch_async
    #_func = libSystem.dispatch_async
    _func.restype = None
    _func.argtypes = [
      objc_id,
      objc_block,
    ]
    dispatch_async._cfunc = _func
  
  _func(queue, block_obj)
  
def onMainThread(func):

  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    if NSThread.isMainThread:
      #print('NSThread')
      func(*args, **kwargs)
    #print('block')
    block = Block(functools.partial(func, *args, **kwargs), None)
    dispatch_async(dispatch_get_main_queue(), block)

  return wrapper


# auto_rename=True を付けておくと a-shell で何度実行してもエラーにならない
class MyViewController(UIViewController):

  @objc_method
  def viewDidLoad(self) -> None:
    send_super(
      __class__,
      self,
      'viewDidLoad',
      restype=None,
    )
    #self.view.backgroundColor = UIColor.systemTealColor

  @objc_method
  def viewDidDisappear_(self, animated: bool) -> None:
    send_super(
      __class__,
      self,
      'viewDidDisappear:',
      animated,
      restype=None,
      argtypes=[
        ctypes.c_bool,
      ],
    )

    if self.isBeingDismissed:
      loop.stop()


class ModalPresenter(NSObject):

  @objc_method
  def presentVC_(self, vc) -> None:

    sharedApplication = UIApplication.sharedApplication
    objectEnumerator = sharedApplication.connectedScenes.objectEnumerator()

    windowScene = next(_scene
                       for _scene in iter(objectEnumerator.nextObject, None)
                       if _scene.activationState == 0)

    rootViewController = windowScene.keyWindow.rootViewController

    vc.modalPresentationStyle = 1

    rootViewController.presentViewController(vc,
                                             animated=True,
                                             completion=None)
    '''

    app = UIApplication.sharedApplication
    rootVC = app.keyWindow.rootViewController
    while childVC := rootVC.presentedViewController:
      rootVC = childVC
    #mainVC = MyViewController.new().autorelease()

    rootVC.presentViewController_animated_completion_(vc, True, None)
    '''


class App:

  def __init__(
    self,
    viewController: UIViewController,
    modalPresentationStyle=1,
  ):
    self.viewController = viewController
    self.modalPresentationStyle = modalPresentationStyle

    self.set_rootViewController()

  def set_rootViewController(self) -> None:
    # >>> (1) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    sharedApplication = UIApplication.sharedApplication
    objectEnumerator = sharedApplication.connectedScenes.objectEnumerator()

    windowScene = next(_scene
                       for _scene in iter(objectEnumerator.nextObject, None)
                       if _scene.activationState == 0)

    rootViewController = windowScene.keyWindow.rootViewController
    self.rootViewController = rootViewController

  def present(self) -> None:

    # >>> (2) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    @onMainThread  #(sync=False)
    def present_viewController(
      viewController: UIViewController,
      style: int,
    ) -> None:

      viewController.setModalPresentationStyle_(style)

      self.rootViewController.presentViewController_animated_completion_(
        viewController,
        True,
        None,
      )

    # >>> (3) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    present_viewController(
      self.viewController,
      self.modalPresentationStyle,
    )
    loop.run_forever()
    #loop.run_forever_cooperatively(lifecycle=iOSLifecycle())
    #self.main_loop()
    #loop.run_forever_cooperatively(lifecycle=iOSLifecycle())

  def main_loop(self) -> None:
    # >>> (4) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    try:
      #print(f'try')
      loop.run_forever()
      #loop.run_forever_cooperatively(lifecycle=CFLifecycle())
    except Exception as e:
      print(f'stop: {e}')
      #loop.stop()
    finally:
      print(f'finally')
      #loop.close()


'''
if __name__ == '__main__':
  print('--- run ---')
  main_vc = MainViewController.new()
  presentation_style = 0

  app = App(main_vc, presentation_style)
  app.present()
  print('--- end ---')
  # >>> (6) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  #loop.close()
'''
'''
if __name__ == '__main__':
  print('--- run ---')
  my_vc = MyViewController.new()
  presenter = ModalPresenter.alloc().init()
  presenter.performSelectorOnMainThread(
    SEL("presentVC:"),
    withObject=my_vc,
    waitUntilDone=False,
  )
  loop.run_forever()
'''
if __name__ == '__main__':
  print('--- run ---')
  main_vc = MyViewController.new()
  presentation_style = 1
  app = App(main_vc, presentation_style)
  app.present()


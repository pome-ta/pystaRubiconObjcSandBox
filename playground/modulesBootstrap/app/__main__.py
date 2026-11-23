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

# todo: main ###############################################
from pyrubicon.objc import (
  NSObject,
  ObjCClass,
  ObjCInstance,
  objc_method,
  objc_property,
)  # api
from pyrubicon.objc import (
  SEL,
  objc_id,
  send_super,
)  # runtime
from pyrubicon.objc.runtime import autoreleasepool
# todo: utils ###############################################
from pyrubicon.objc.runtime import Class, Foundation
# todo: lifeCycle ###########################################
from pyrubicon.objc.eventloop import RubiconEventLoop
# todo: exception ###########################################
import sys
import os
# todo: mainThread ##########################################
import functools
from pyrubicon.objc import Block  # api
from pyrubicon.objc import objc_block  # runtime
from pyrubicon.objc.runtime import load_library

from rbedge import pdbr

ObjCClass.auto_rename = True


#############################################################
# --- utils
def NSStringFromClass(cls: Class) -> ObjCInstance:
  try:
    _func = NSStringFromClass._cfunc
  except AttributeError:
    _func = Foundation.NSStringFromClass
    _func.restype = objc_id
    _func.argtypes = [Class]
    NSStringFromClass._cfunc = _func

  return ObjCInstance(_func(cls))


#############################################################
# --- exception
#############################################################

import faulthandler

_fh_file = open(
  os.path.expanduser('~/Documents/_rubicon_objc_faulthandler.txt'), 'w')
faulthandler.enable(_fh_file)

# todo: from objc_util.py of Pythonista3
#  呼び出し方法と出力先を調整
#    - `~/Documents/_objc_exception.txt`
#    - `~/Documents/_rubicon_objc_exception.txt`
# Set a handler for uncaught ObjC exceptions that writes to a log file:
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
  _path_str = '~/Documents/_rubicon_objc_exception.txt'
  with open(os.path.expanduser(_path_str), 'w') as f:
    from datetime import datetime
    f.write(
      'The app was terminated due to an Objective-C exception. Details below:\n\n%s\n%s\n'
      % (datetime.now(), exc))


_handler = ExceptionHandlerFuncType(_objc_exception_handler)
NSSetUncaughtExceptionHandler(_handler)

#############################################################
# --- lifeCycle
#############################################################
loop = RubiconEventLoop()

#############################################################
# --- mainThread
#############################################################
libSystem = load_library('System')
NSThread = ObjCClass('NSThread')


class struct_dispatch_queue_s(ctypes.Structure):
  pass  # No _fields_, because this is an opaque structure.


_dispatch_main_q = struct_dispatch_queue_s.in_dll(
  libSystem,
  '_dispatch_main_q',
)


def dispatch_get_main_queue():
  return ObjCInstance(ctypes.cast(
    ctypes.byref(_dispatch_main_q),
    objc_id,
  ))


def dispatch_async(queue, block_obj: objc_block):
  try:
    _func = dispatch_async._cfunc
  except AttributeError:
    _func = libSystem.dispatch_async
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
      func(*args, **kwargs)
      return
    block = Block(functools.partial(func, *args, **kwargs), None)
    dispatch_async(dispatch_get_main_queue(), block)

  return wrapper


#############################################################
# --- UINavigationController
#############################################################
UINavigationController = ObjCClass('UINavigationController')
UIBarButtonItem = ObjCClass('UIBarButtonItem')


class RootNavigationController(UINavigationController):

  @objc_method
  def dealloc(self) -> None:
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def loadView(self) -> None:
    send_super(
      __class__,
      self,
      'loadView',
      restype=None,
    )
    print(f'{NSStringFromClass(__class__)}: loadView')

  @objc_method
  def viewDidLoad(self) -> None:
    send_super(
      __class__,
      self,
      'viewDidLoad',
      restype=None,
    )
    print(f'{NSStringFromClass(__class__)}: viewDidLoad')
    self.delegate = self

  @objc_method
  def viewWillAppear_(self, animated: bool) -> None:
    send_super(
      __class__,
      self,
      'viewWillAppear:',
      animated,
      restype=None,
      argtypes=[
        ctypes.c_bool,
      ],
    )
    print(f'{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool) -> None:
    send_super(
      __class__,
      self,
      'viewDidAppear:',
      animated,
      restype=None,
      argtypes=[
        ctypes.c_bool,
      ],
    )
    print(f'{NSStringFromClass(__class__)}: viewDidAppear_')
    print('↓ ---')

  @objc_method
  def viewWillDisappear_(self, animated: bool) -> None:
    print('↑ ---')
    send_super(
      __class__,
      self,
      'viewWillDisappear:',
      animated,
      restype=None,
      argtypes=[
        ctypes.c_bool,
      ],
    )
    print(f'{NSStringFromClass(__class__)}: viewWillDisappear_')

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
    print(f'{NSStringFromClass(__class__)}: viewDidDisappear_')
    if self.isBeingDismissed:
      # >>> (5) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      print('stop Call')
      loop.call_later(0.2, loop.stop)

  @objc_method
  def closeButtonTapped_(self, sender) -> None:
    print(f'{NSStringFromClass(__class__)}: doneButtonTapped:')
    self.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
    self,
    navigationController,
    viewController,
    animated: bool,
  ) -> None:
    closeButtonItem = UIBarButtonItem.alloc().initWithBarButtonSystemItem(
      24,
      target=navigationController,
      action=SEL('closeButtonTapped:'),
    )

    visibleViewController = navigationController.visibleViewController
    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = closeButtonItem


#############################################################
# --- UIViewController
#############################################################
UIViewController = ObjCClass('UIViewController')


class MainViewController(UIViewController):

  @objc_method
  def dealloc(self) -> None:
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self) -> None:
    send_super(
      __class__,
      self,
      'loadView',
      restype=None,
    )
    print(f'\t{NSStringFromClass(__class__)}: loadView')

  @objc_method
  def viewDidLoad(self) -> None:
    send_super(
      __class__,
      self,
      'viewDidLoad',
      restype=None,
    )
    print(f'\t{NSStringFromClass(__class__)}: viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__)

  @objc_method
  def viewWillAppear_(self, animated: bool) -> None:
    send_super(
      __class__,
      self,
      'viewWillAppear:',
      animated,
      restype=None,
      argtypes=[
        ctypes.c_bool,
      ],
    )
    print(f'\t{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool) -> None:
    send_super(
      __class__,
      self,
      'viewDidAppear:',
      animated,
      restype=None,
      argtypes=[
        ctypes.c_bool,
      ],
    )
    print(f'\t{NSStringFromClass(__class__)}: viewDidAppear_')
    print('\t↓ ---')

  @objc_method
  def viewWillDisappear_(self, animated: bool) -> None:
    print('\t↑ ---')
    send_super(
      __class__,
      self,
      'viewWillDisappear:',
      animated,
      restype=None,
      argtypes=[
        ctypes.c_bool,
      ],
    )
    print(f'\t{NSStringFromClass(__class__)}: viewWillDisappear_')

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
    print(f'\t{NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self) -> None:
    send_super(
      __class__,
      self,
      'didReceiveMemoryWarning',
      restype=None,
    )
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')


#############################################################
# --- app present
#############################################################
UIApplication = ObjCClass('UIApplication')


class Application(NSObject):

  viewController = objc_property(ObjCInstance)
  navigationClass = objc_property(ObjCClass)
  # # keyWindowViewController = objc_property(ObjCInstance, weak=True)
  # keyWindowViewController = objc_property(object)

  @objc_method
  def dealloc(self) -> None:
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def initSetupWithViewController_navigationClass_(
    self,
    viewController: ObjCInstance,
    navigationClass: ObjCClass,
  ) -> ObjCInstance:
    self = ObjCInstance(
      send_super(__class__, self, 'init', restype=objc_id, argtypes=[]))
    if self is None:
      return None

    self.viewController = viewController
    self.navigationClass = navigationClass
    '''
    sharedApplication = UIApplication.sharedApplication
    objectEnumerator = sharedApplication.connectedScenes.objectEnumerator()
    windowScene = next(_scene
                       for _scene in iter(objectEnumerator.nextObject, None)
                       if _scene.activationState == 0)
    keyWindowViewController = windowScene.keyWindow.rootViewController
    self.keyWindowViewController = keyWindowViewController
    '''

    return self

  @objc_method
  def initWithViewController_(
    self,
    viewController: ObjCInstance,
  ) -> ObjCInstance:
    return self.initSetupWithViewController_navigationClass_(
      viewController,
      RootNavigationController,
    )

  @objc_method
  def initWithViewController_navigationClass_(
    self,
    viewController: ObjCInstance,
    navigationClass: ObjCClass,
  ) -> ObjCInstance:
    return self.initSetupWithViewController_navigationClass_(
      viewController,
      navigationClass,
    )

  @objc_method
  def presentWithStyle_(self, style: int) -> None:
    # >>> (2) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    @onMainThread
    def _main_thread_present() -> None:
      # >>> (1) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      sharedApplication = UIApplication.sharedApplication
      objectEnumerator = sharedApplication.connectedScenes.objectEnumerator()
      windowScene = next(_scene
                         for _scene in iter(objectEnumerator.nextObject, None)
                         if _scene.activationState == 0)
      keyWindowViewController = windowScene.keyWindow.rootViewController

      presentController = self.navigationClass.alloc(
      ).initWithRootViewController_(self.viewController)
      presentController.setModalPresentationStyle_(style)
      '''
      self.keyWindowViewController.presentViewController_animated_completion_(
        presentController,
        True,
        None,
      )
      '''

      keyWindowViewController.presentViewController_animated_completion_(
        presentController,
        True,
        None,
      )

    # >>> (3) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    _main_thread_present()
    print('s: --- main_loop')
    # >>> (4) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    loop.run_forever()
    print('e: --- main_loop')


@autoreleasepool()
def main_call():
  import gc
  print('--- run ---')
  main_vc = MainViewController.new()
  presentation_style = 1
  app = Application.alloc().initWithViewController_(main_vc)
  app.presentWithStyle_(presentation_style)
  print('--- end ---')
  del app, main_vc
  # gc.collect()
  '''
  with autoreleasepool():
    print('--- run ---')
    main_vc = MainViewController.new()
    presentation_style = 1
    app = Application.alloc().initWithViewController_(main_vc)
    app.presentWithStyle_(presentation_style)
    print('--- end ---')
    del app, main_vc
    print('--- del ---')
  '''


if __name__ == '__main__':
  import gc
  '''
  print('--- run ---')
  main_vc = MainViewController.new()
  presentation_style = 1
  app = Application.alloc().initWithViewController_(main_vc)
  app.presentWithStyle_(presentation_style)
  print('--- end ---')
  '''

  with autoreleasepool():
    print('--- run ---')
    main_vc = MainViewController.new()
    presentation_style = 1
    app = Application.alloc().initWithViewController_(main_vc)
    app.presentWithStyle_(presentation_style)
    print('--- end ---')
    del main_vc, app
    print('--- del ---')

  # main_call()
  print('try --- collect')
  try:
    gc.collect()
    print('--- collect: done')
  except Exception as e:
    print('--- collect: error')
    print(f'{e}')


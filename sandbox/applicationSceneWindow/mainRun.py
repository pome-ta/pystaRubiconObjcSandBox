'''
  note: sharedApplication` で何が覗けるか調査
'''
import ctypes
from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import objc_id, send_super, SEL

from rbedge import pdbr

ObjCClass.auto_rename = True

#############################################################
# --- utils
#############################################################
from pyrubicon.objc.runtime import Class, Foundation


def NSStringFromClass(cls: Class) -> ObjCInstance:
  _NSStringFromClass = Foundation.NSStringFromClass
  _NSStringFromClass.restype = ctypes.c_void_p
  _NSStringFromClass.argtypes = [Class]
  return ObjCInstance(_NSStringFromClass(cls))


#############################################################
# --- exception
#######################################################
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
#######################################################

#############################################################

UIApplication = ObjCClass('UIApplication')
UIWindow = ObjCClass('UIWindow')
UIWindowScene = ObjCClass('UIWindowScene')

NSOperation = ObjCClass("NSOperation")
NSOperationQueue = ObjCClass("NSOperationQueue")

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')


class UISceneActivationState:
  unattached = -1
  foregroundActive = 0
  foregroundInactive = 1
  background = 2


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
    viewController.setEdgesForExtendedLayout_(0)
    _UIBarButtonSystemItem_close = 24
    closeButtonItem = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(_UIBarButtonSystemItem_close,
                                                 navigationController,
                                                 SEL('doneButtonTapped:'))
    visibleViewController = navigationController.visibleViewController

    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = closeButtonItem


#############################################################
# --- UIViewController
#############################################################
UIViewController = ObjCClass('UIViewController')


class RootViewController(UIViewController):

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
    self.view.backgroundColor = UIColor.systemDarkTealColor()

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


#initWithSession_connectionOptions_


class NewUIWindowScene(UIWindowScene):

  @objc_method
  def dealloc(self):
    print(f'- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def initWithSession_connectionOptions_(self, scene, connectionOptions):
    send_super(__class__,
               self,
               'initWithSession:connectionOptions:',
               scene,
               connectionOptions,
               argtypes=[
                 objc_id,
                 objc_id,
               ])
    return self


#############################################################
# --- mainThread ?
#############################################################
class MainOperation(NSOperation):

  @objc_method
  def dealloc(self):
    print(f'- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def main(self):
    send_super(__class__, self, 'main')
    print(f'{NSStringFromClass(__class__)}: main')

    sharedApplication = UIApplication.sharedApplication
    connectedScenes = sharedApplication.connectedScenes
    objectEnumerator = connectedScenes.objectEnumerator()

    while (windowScene := objectEnumerator.nextObject()):
      if windowScene.activationState == UISceneActivationState.foregroundActive:
        break
    
    keyWindow = windowScene.keyWindow
    base_rootViewController = keyWindow.rootViewController
    
    window = UIWindow.alloc().initWithWindowScene_(windowScene)
    window.makeKeyAndVisible()
    window.rootViewController = base_rootViewController
    window.resignKeyWindow()
    pdbr.state(windowScene.keyWindow)
    
    
    
    
    #pdbr.state(base_rootViewController)
    #session
    #print(windowScene.keyWindow)
    #pdbr.state(UIWindowScene.new())


if __name__ == '__main__':
  print('--- run')
  operation = MainOperation.new()
  mainQueue = NSOperationQueue.mainQueue
  mainQueue.addOperation(operation)
  print('--- addOperation')
  mainQueue.waitUntilAllOperationsAreFinished()
  print('--- waitUntilAllOperationsAreFinished')
  print('--- end')


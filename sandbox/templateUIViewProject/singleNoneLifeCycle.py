import ctypes
import functools

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import objc_id, send_super, objc_block, libobjc, Class, Foundation, SEL

ObjCClass.auto_rename = True

NSThread = ObjCClass('NSThread')


class struct_dispatch_queue_s(ctypes.Structure):
  pass  # No _fields_, because this is an opaque structure.


_dispatch_main_q = struct_dispatch_queue_s.in_dll(libobjc, '_dispatch_main_q')


def dispatch_get_main_queue():
  return ObjCInstance(ctypes.cast(ctypes.byref(_dispatch_main_q), objc_id))


libobjc.dispatch_async.restype = None
libobjc.dispatch_async.argtypes = [objc_id, objc_block]


def onMainThread(func):

  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    if NSThread.isMainThread:
      func(*args, **kwargs)
    block = Block(functools.partial(func, *args, **kwargs), None)
    libobjc.dispatch_async(dispatch_get_main_queue(), block)

  return wrapper


@onMainThread
def present_viewController(viewController: ObjCInstance,
                           modalPresentationStyle: int = 0,
                           navigationController_enabled: bool = True):
  sharedApplication = ObjCClass('UIApplication').sharedApplication
  keyWindow = sharedApplication.keyWindow if sharedApplication.keyWindow else sharedApplication.windows[
    0]
  rootViewController = keyWindow.rootViewController

  while _presentedViewController := rootViewController.presentedViewController:
    rootViewController = _presentedViewController

  if navigationController_enabled:

    presentViewController = RootNavigationController.alloc(
    ).initWithRootViewController_(viewController)
  else:
    presentViewController = viewController

  # xxx: style 指定を力技で確認
  automatic = -2  # UIModalPresentationStyle.automatic
  blurOverFullScreen = 8  # UIModalPresentationStyle.blurOverFullScreen
  pageSheet = 1  # UIModalPresentationStyle.pageSheet

  style = modalPresentationStyle if isinstance(
    modalPresentationStyle, int
  ) and automatic <= modalPresentationStyle <= blurOverFullScreen else pageSheet

  presentViewController.setModalPresentationStyle_(style)
  print('pre: presentViewController')
  @Block
  def completion()->None:
    print('block')

  rootViewController.presentViewController_animated_completion_(
    presentViewController, True, completion)
  print('modern: presentViewController')


def NSStringFromClass(cls: Class) -> ObjCInstance:
  _NSStringFromClass = Foundation.NSStringFromClass
  _NSStringFromClass.restype = ctypes.c_void_p
  _NSStringFromClass.argtypes = [Class]
  return ObjCInstance(_NSStringFromClass(cls))


# --- UINavigationController
UINavigationController = ObjCClass('UINavigationController')
UIBarButtonItem = ObjCClass('UIBarButtonItem')


class RootNavigationController(UINavigationController):

  @objc_method
  def viewDidLoad(self):
    print('RootNavigationController: viewDidLoad')
    self.delegate = self

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print('RootNavigationController: viewDidDisappear')

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated: bool):

    _UIBarButtonSystemItem_close = 24
    closeButtonItem = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(_UIBarButtonSystemItem_close,
                                                 navigationController,
                                                 SEL('doneButtonTapped:'))
    # todo: view 遷移でのButton 重複を判別
    closeButtonItem.setTag_(_UIBarButtonSystemItem_close)

    visibleViewController = navigationController.visibleViewController

    navigationItem = visibleViewController.navigationItem
    if (rightBarButtonItems := navigationItem.rightBarButtonItems):
      # todo: `UIViewController` で、`rightBarButtonItem` が存在していた場合、`closeButtonItem` を右端に設置
      setRightBarButtonItems = [
        closeButtonItem,
        *[
          item for item in rightBarButtonItems
          if item.tag != _UIBarButtonSystemItem_close
        ],
      ]
      navigationItem.setRightBarButtonItems_animated_(setRightBarButtonItems,
                                                      True)
    else:
      navigationItem.rightBarButtonItem = closeButtonItem


# --- MainViewController
UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')


class MainViewController(UIViewController):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print('\tdealloc')
    pass

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print('viewWillAppear')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print('viewDidAppear')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print('viewWillDisappear')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print('viewDidDisappear')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'{__class__}: didReceiveMemoryWarning')


if __name__ == '__main__':
  main_vc = MainViewController.new()

  _title = NSStringFromClass(MainViewController)
  main_vc.navigationItem.title = _title

  presentation_style = 1  #UIModalPresentationStyle.fullScreen
  present_viewController(main_vc, presentation_style)


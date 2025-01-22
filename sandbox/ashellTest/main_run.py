import sys
import asyncio
from pyrubicon.objc.eventloop import EventLoopPolicy, iOSLifecycle

from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method
from pyrubicon.objc.runtime import SEL, send_super

import pdbr

ObjCClass.auto_rename = True

#from ctypes import byref, cast, Structure
import ctypes
import functools

### --- onMainThread --- ###
from pyrubicon.objc.api import Block, ObjCClass, ObjCInstance
from pyrubicon.objc.runtime import libobjc, objc_block, objc_id


asyncio.set_event_loop_policy(EventLoopPolicy())
loop = asyncio.new_event_loop()

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


### --- ###

# --- UINavigationController
UINavigationController = ObjCClass('UINavigationController')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

# --- UIViewController
UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
UIButtonConfiguration = ObjCClass('UIButtonConfiguration')
UIButton = ObjCClass('UIButton')

NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
# ref: [UIRectEdge | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uirectedge?language=objc)
'''
UIRectEdgeNone = 0
'''
edgeNone = 0

# ref: [UIControlEvents | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uicontrolevents?language=objc)
'''
UIControlEventTouchUpInside = 1 <<  6
'''
touchUpInside = 1 << 6

# ref: [UIBarButtonSystemItem | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uibarbuttonsystemitem?language=objc)
'''
UIBarButtonSystemItemDone
'''
done = 0


# --- NavigationController
class RootNavigationController(UINavigationController,
                               protocols=[UINavigationControllerDelegate]):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    appearance = UINavigationBarAppearance.new()
    appearance.configureWithDefaultBackground()

    navigationBar = self.navigationBar
    navigationBar.standardAppearance = appearance
    navigationBar.scrollEdgeAppearance = appearance
    navigationBar.compactAppearance = appearance
    navigationBar.compactScrollEdgeAppearance = appearance

    self.delegate = self

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewDidDisappear:')
    #loop.stop()
    #loop.shutdown_asyncgens()
    print('RootNavigationController: viewDidDisappear')

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController

    visibleViewController.dismissViewControllerAnimated_completion_(True, None)

    #sys.exit()
    #loop.stop()
    #loop.close()
    #del loop

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated: bool):
    viewController.setEdgesForExtendedLayout_(edgeNone)
    doneButton = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(done, navigationController,
                                                 SEL('doneButtonTapped:'))
    visibleViewController = navigationController.visibleViewController

    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = doneButton


# --- ViewController
class FirstViewController(UIViewController):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print('\tdealloc')
    pass

  @objc_method
  def onTap_(self, sender):
    svc = SecondViewController.new()
    navigationController = self.navigationController
    navigationController.pushViewController_animated_(svc, True)

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    self.navigationItem.title = 'FirstView'

    # --- View
    self.view.backgroundColor = UIColor.systemBlueColor()
    config = UIButtonConfiguration.tintedButtonConfiguration()
    config.title = 'Tap'
    config.baseBackgroundColor = UIColor.systemPinkColor()
    config.baseForegroundColor = UIColor.systemGreenColor()

    tapButton = UIButton.new()
    tapButton.configuration = config
    tapButton.addTarget_action_forControlEvents_(self, SEL('onTap:'),
                                                 touchUpInside)

    self.view.addSubview_(tapButton)
    # --- Layout
    tapButton.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      tapButton.centerXAnchor.constraintEqualToAnchor_(
        self.view.centerXAnchor),
      tapButton.centerYAnchor.constraintEqualToAnchor_(
        self.view.centerYAnchor),
      tapButton.widthAnchor.constraintEqualToAnchor_multiplier_(
        self.view.widthAnchor, 0.4),
      tapButton.heightAnchor.constraintEqualToAnchor_multiplier_(
        self.view.heightAnchor, 0.1),
    ])

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


class SecondViewController(UIViewController):

  @objc_method
  def onTap_(self, sender):
    navigationController = self.navigationController
    navigationController.popViewControllerAnimated_(True)

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    self.navigationItem.title = 'SecondView'

    # --- View
    self.view.backgroundColor = UIColor.systemGreenColor()
    config = UIButtonConfiguration.tintedButtonConfiguration()
    config.title = 'Tap'
    config.baseBackgroundColor = UIColor.systemPinkColor()
    config.baseForegroundColor = UIColor.systemBlueColor()

    tapButton = UIButton.new()
    tapButton.configuration = config
    tapButton.addTarget_action_forControlEvents_(self, SEL('onTap:'),
                                                 touchUpInside)

    self.view.addSubview_(tapButton)
    # --- Layout
    tapButton.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      tapButton.centerXAnchor.constraintEqualToAnchor_(
        self.view.centerXAnchor),
      tapButton.centerYAnchor.constraintEqualToAnchor_(
        self.view.centerYAnchor),
      tapButton.widthAnchor.constraintEqualToAnchor_multiplier_(
        self.view.widthAnchor, 0.4),
      tapButton.heightAnchor.constraintEqualToAnchor_multiplier_(
        self.view.heightAnchor, 0.1),
    ])


# --- main
@onMainThread
def present_viewController(myVC: UIViewController):
  
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  rootVC = window.rootViewController

  while _presentedVC := rootVC.presentedViewController:
    rootVC = _presentedVC

  myNC = RootNavigationController.alloc().initWithRootViewController_(myVC)

  presentVC = myNC

  # ref: [UIModalPresentationStyle | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uimodalpresentationstyle?language=objc)
  '''
  UIModalPresentationFullScreen = 0
  UIModalPresentationPageSheet = 1
  '''
  presentVC.setModalPresentationStyle_(1)

  rootVC.presentViewController_animated_completion_(presentVC, True, None)
  loop.stop()


if __name__ == "__main__":
  vc = FirstViewController.new()
  present_viewController(vc)
  
  #loop.stop()
  #print(dir(loop))
  loop.run_forever(lifecycle=iOSLifecycle())
  print('hogeeeeee')
  #loop.stop()



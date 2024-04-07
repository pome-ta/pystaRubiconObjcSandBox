import ctypes

from pyrubicon.objc.api import at, ObjCInstance, ObjCClass, ObjCProtocol, objc_property, objc_method
from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import Block
from pyrubicon.objc.runtime import SEL, send_super

from mainThread import onMainThread
from objc_util import on_main_thread

import pdbr


ObjCClass.auto_rename = True

UINavigationController = ObjCClass('UINavigationController')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')

UIButtonConfiguration = ObjCClass('UIButtonConfiguration')
UIButton = ObjCClass('UIButton')
UIControlEventTouchUpInside = 1 << 6

NSLayoutConstraint = ObjCClass('NSLayoutConstraint')


#@onMainThread
#@on_main_thread
@onMainThread
def present_ViewController(myViewController):
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  rootViewController = window.rootViewController

  while presentedViewController := rootViewController.presentedViewController:
    rootViewController = presentedViewController

  #navigationController = UINavigationController.new()
  navigationController = UINavigationController.alloc(
  ).initWithRootViewController_(myViewController).autorelease()
  delegate = RootNavigationControllerDelegate.new()
  pdbr.state(delegate)
  navigationController.delegate = delegate
  
  #navigationController = WrapNavigationController.new(myViewController)

  controller = navigationController
  controller.setModalPresentationStyle_(1)

  rootViewController.presentViewController_animated_completion_(
    controller, True, None)



#pdbr.state(UINavigationControllerDelegate)

'''
class RootNavigationController(UINavigationController):
  delegate = objc_property()
'''

class RootNavigationControllerDelegate(NSObject, protocols=[UINavigationControllerDelegate]):

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated):
    appearance = UINavigationBarAppearance.new()
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
    topViewController = navigationController.topViewController
    
    #pdbr.state(navigationController)
    #topViewController

    navigationItem = visibleViewController.navigationItem
    #navigationItem = navigationController.navigationItem
    #navigationItem = topViewController.navigationItem
    
    navigationItem.rightBarButtonItem = done_btn


# --- ViewController


class FirstViewController(UIViewController):

  @objc_method
  def onTap_(self, sender):
    navigationController = self.navigationController
    svc = SecondViewController.new()#.autorelease()
    navigationController.pushViewController_animated_(svc, True)
    

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')

    self.navigationItem.title = 'FirstViewController'
    self.view.backgroundColor = UIColor.systemBlueColor()

    config = UIButtonConfiguration.tintedButtonConfiguration()
    config.title = 'Tap'
    config.baseBackgroundColor = UIColor.systemPinkColor()
    config.baseForegroundColor = UIColor.systemGreenColor()

    tapButton = UIButton.new()
    tapButton.configuration = config
    #btn.addTarget_action_(self, SEL('onTap:'))
    tapButton.addTarget_action_forControlEvents_(self, SEL('onTap:'),
                                                 UIControlEventTouchUpInside)
    #btn.addAction_forControlEvents_(None, UIControlEventTouchUpInside)
    #pdbr.state(btn)

    self.view.addSubview_(tapButton)

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


class SecondViewController(UIViewController):

  @objc_method
  def onTap_(self, sender):
    navigationController = self.navigationController
    pdbr.state(navigationController)

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')

    self.navigationItem.title = 'SecondViewController'
    self.view.backgroundColor = UIColor.systemGreenColor()

    config = UIButtonConfiguration.tintedButtonConfiguration()
    config.title = 'Tap'
    config.baseBackgroundColor = UIColor.systemPinkColor()
    config.baseForegroundColor = UIColor.systemBlueColor()

    btn = UIButton.new()
    btn.configuration = config
    btn.addTarget_action_(self, SEL('onTap:'))

    self.view.addSubview_(btn)

    btn.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      btn.centerXAnchor.constraintEqualToAnchor_(self.view.centerXAnchor),
      btn.centerYAnchor.constraintEqualToAnchor_(self.view.centerYAnchor),
      btn.widthAnchor.constraintEqualToAnchor_multiplier_(
        self.view.widthAnchor, 0.5),
      btn.heightAnchor.constraintEqualToAnchor_multiplier_(
        self.view.heightAnchor, 0.3),
    ])


if __name__ == "__main__":
  _vc = FirstViewController.new()
  #navigationController = WrapNavigationController.new(_vc)
  present_ViewController(_vc)
  #print(navigationController)
  #pdbr.state(navigationController)


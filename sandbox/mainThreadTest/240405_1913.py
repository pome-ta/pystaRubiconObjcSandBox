import ctypes

from pyrubicon.objc.api import ObjCInstance, ObjCClass, ObjCProtocol, objc_property, objc_method
#from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import Block
from pyrubicon.objc.runtime import SEL, send_super

from mainThread import onMainThread

import pdbr

ObjCClass.auto_rename = True


@onMainThread
def present_ViewController(viewController_instance):
  vc = viewController_instance
  vc.autorelease()
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  root_vc = window.rootViewController

  while child_vc := root_vc.presentedViewController:
    root_vc = child_vc

  vc.setModalPresentationStyle_(1)
  root_vc.presentViewController_animated_completion_(vc, True, None)


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


class RootNavigationController(UINavigationController,
                               protocols=[UINavigationControllerDelegate]):

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated):
    appearance = UINavigationBarAppearance.new().autorelease()
    appearance.configureWithDefaultBackground()

    navigationBar = navigationController.navigationBar
    navigationBar.standardAppearance = appearance
    navigationBar.scrollEdgeAppearance = appearance
    navigationBar.compactAppearance = appearance
    navigationBar.compactScrollEdgeAppearance = appearance

    viewController.setEdgesForExtendedLayout_(0)
    '''

    done_btn = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, navigationController,
                                                 SEL('doneButtonTapped:'))
    visibleViewController = navigationController.visibleViewController

    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = done_btn
    '''





# --- ViewController


class FirstViewController(UIViewController):

  @objc_method
  def onTap_(self, sender):
    navigationController = self.navigationController

    selector = SEL('pushViewController:animated:')
    #_ptr = navigationController.ptr
    #print(_ptr)
    #_class = Class(navigationController.ptr)
    #_c =
    #pdbr.state(navigationController.__class__)
    #print(navigationController)
    #pdbr.state(WrapNavigationController)
    #pdbr.state(navigationController.zone)
    #print(navigationController.class)
    #signature = navigationController.instanceMethodSignatureForSelector_(selector)

    #self.performSelectorOnMainThread_withObject_waitUntilDone_(selector, None, True)
    #pdbr.state(navigationController)
    #print(dir(svc))
    svc = SecondViewController.new()
    svc.autorelease()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')

    self.navigationItem.title = 'FirstViewController'
    self.view.backgroundColor = UIColor.systemBlueColor()

    config = UIButtonConfiguration.tintedButtonConfiguration()
    config.title = 'Tap'
    config.baseBackgroundColor = UIColor.systemPinkColor()
    config.baseForegroundColor = UIColor.systemGreenColor()

    btn = UIButton.new()
    btn.configuration = config
    #btn.addTarget_action_(self, SEL('onTap:'))
    btn.addTarget_action_forControlEvents_(self, SEL('onTap:'),
                                           UIControlEventTouchUpInside)
    #btn.addAction_forControlEvents_(None, UIControlEventTouchUpInside)
    #pdbr.state(btn)

    self.view.addSubview_(btn)

    btn.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      btn.centerXAnchor.constraintEqualToAnchor_(self.view.centerXAnchor),
      btn.centerYAnchor.constraintEqualToAnchor_(self.view.centerYAnchor),
      btn.widthAnchor.constraintEqualToAnchor_multiplier_(
        self.view.widthAnchor, 0.4),
      btn.heightAnchor.constraintEqualToAnchor_multiplier_(
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
  present_ViewController(_vc)


import ctypes

from pyrubicon.objc.api import at, ObjCInstance, ObjCClass, ObjCProtocol, objc_property, objc_method
#from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import Block
from pyrubicon.objc.runtime import SEL, send_super

from mainThread import onMainThread

import pdbr

NSInvocation = ObjCClass('NSInvocation')
ObjCClass.auto_rename = True


@onMainThread
def present_ViewController(myViewController):
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  rootViewController = window.rootViewController

  while presentedViewController := rootViewController.presentedViewController:
    rootViewController = presentedViewController

  navigationController = RootNavigationController.alloc(
  ).initWithRootViewController_(myViewController).autorelease()
  navigationController.delegate = navigationController

  controller = navigationController
  controller.setModalPresentationStyle_(1)

  rootViewController.presentViewController_animated_completion_(
    controller, True, None)


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

    #navigationItem = visibleViewController.navigationItem
    #navigationItem = navigationController.navigationItem
    navigationItem = topViewController.navigationItem
    
    navigationItem.rightBarButtonItem = done_btn


# --- ViewController


class FirstViewController(UIViewController):

  @objc_method
  def onTap_(self, sender):
    navigationController = self.navigationController
    svc = SecondViewController.new()#.autorelease()
    '''
    @onMainThread
    def run():
      
      selector = SEL('pushViewController:animated:')
      signature = navigationController.methodSignatureForSelector_(selector)
  
      invocation = NSInvocation.invocationWithMethodSignature_(signature)
      invocation.setSelector_(selector)
      invocation.setTarget_(navigationController)
      invocation.setArgument_atIndex_(svc, 2)
      invocation.setArgument_atIndex_('', 3)
      invocation.invoke()
      #pdbr.state(invocation)

    run()
    '''
    '''
    selector = SEL('pushViewController:animated:')
    signature = navigationController.methodSignatureForSelector_(selector)

    invocation = NSInvocation.invocationWithMethodSignature_(signature)
    invocation.setSelector_(selector)
    invocation.setTarget_(navigationController)
    invocation.setArgument_atIndex_(svc, 2)
    invocation.setArgument_atIndex_(True, 3)
    invocation.invoke()
    #pdbr.state(invocation)
    #print(invocation)
    #pdbr.state(invocation)
    print(at(True))
    '''
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
  present_ViewController(_vc)


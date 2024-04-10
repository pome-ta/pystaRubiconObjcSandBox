from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method
from pyrubicon.objc.runtime import SEL, send_super

from mainThread import onMainThread
import pdbr

ObjCClass.auto_rename = True
#ObjCProtocol.auto_rename = True

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
touchUpInside = 1 << 6

NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

pageSheet = 1  # xxx: あとでちゃんと定義する


# --- NavigationController
class RootNavigationController(UINavigationController):

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

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)


# --- ViewController
class FirstViewController(UIViewController):

  @objc_method
  def onTap_(self, sender):
    svc = SecondViewController.new()
    navigationController = self.navigationController
    navigationController.pushViewController_animated_(svc, True)

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')

    # --- Navigation
    doneButton = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, self.navigationController,
                                                 SEL('doneButtonTapped:'))

    navigationItem = self.navigationItem
    navigationItem.rightBarButtonItem = doneButton
    navigationItem.title = 'FirstView'

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
    self.setEdgesForExtendedLayout_(0)
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
    navigationController.popViewControllerAnimated_(True)

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')

    # --- Navigation
    doneButton = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, self.navigationController,
                                                 SEL('doneButtonTapped:'))

    navigationItem = self.navigationItem
    navigationItem.rightBarButtonItem = doneButton
    navigationItem.title = 'SecondView'

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
    self.setEdgesForExtendedLayout_(0)
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
  presentVC.setModalPresentationStyle_(0)

  rootVC.presentViewController_animated_completion_(presentVC, True, None)


if __name__ == "__main__":
  vc = FirstViewController.new()
  present_viewController(vc)


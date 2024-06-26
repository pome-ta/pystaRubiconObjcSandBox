from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method
from pyrubicon.objc.runtime import SEL, send_super

from mainThread import onMainThread
from objc_util import on_main_thread
import pdbr

ObjCClass.auto_rename = True
ObjCProtocol.auto_rename = True

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

is_print = True
_dp = lambda _s: print(_s) if is_print else None


# --- NavigationController
class RootNavigationController(UINavigationController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    _dp('--- viewDidLoad\t -> NavigationController')
    appearance = UINavigationBarAppearance.new()
    appearance.configureWithDefaultBackground()

    navigationBar = self.navigationBar
    navigationBar.standardAppearance = appearance
    navigationBar.scrollEdgeAppearance = appearance
    navigationBar.compactAppearance = appearance
    navigationBar.compactScrollEdgeAppearance = appearance

    #pdbr.state(self)
    #print(self.navigationItem)
    #pdbr.state(self.navigationItem)
    '''
    
    doneButton = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, self,SEL('doneButtonTapped:'))
    #self.navigationItem.rightBarButtonItem = doneButton
    self.navigationItem.setRightBarButtonItem_(doneButton)
    '''

  @objc_method
  def viewDidAppear_(self, animated: bool):
    # xxx: 引数不要?
    send_super(__class__, self, 'viewDidAppear:')
    _dp('--- viewDidAppear:\t -> NavigationController')
    '''
    doneButton = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, self,
                                                 SEL('doneButtonTapped:'))
    #self.navigationItem.rightBarButtonItem = doneButton
    self.navigationItem.setRightBarButtonItem_(doneButton)
    '''
    #pdbr.state(self.visibleViewController)
    #self.visibleViewController.setEdgesForExtendedLayout_(0)

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewWillDisappear:')
    _dp('--- viewWillDisappear:\t -> NavigationController')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewDidDisappear:')
    _dp('--- viewDidDisappear:\t -> NavigationController')

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)


# --- ViewController
class FirstViewController(UIViewController):

  @objc_method
  def onTap_(self, sender):
    navigationController = self.navigationController
    svc = SecondViewController.new()
    navigationController.pushViewController_animated_(svc, True)

  @objc_method
  def doneButtonTapped_(self, sender):
    self.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    _dp('--- viewDidLoad\t -> ViewController')

    self.view.backgroundColor = UIColor.systemBlueColor()
    self.setEdgesForExtendedLayout_(0)
    doneButton = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, self,
                                                 SEL('doneButtonTapped:'))

    self.navigationItem.rightBarButtonItem = doneButton
    self.navigationItem.title = 'FirstView'

    config = UIButtonConfiguration.tintedButtonConfiguration()
    config.title = 'Tap'
    config.baseBackgroundColor = UIColor.systemPinkColor()
    config.baseForegroundColor = UIColor.systemGreenColor()

    tapButton = UIButton.new()
    tapButton.configuration = config
    tapButton.addTarget_action_forControlEvents_(self, SEL('onTap:'),
                                                 touchUpInside)

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

  @objc_method
  def viewDidAppear_(self, animated: bool):
    # xxx: 引数不要？
    send_super(__class__, self, 'viewDidAppear:')
    _dp('--- viewDidAppear:\t -> ViewController')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewWillDisappear:')
    _dp('--- viewWillDisappear:\t -> ViewController')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewDidDisappear:')
    _dp('--- viewDidDisappear:\t -> ViewController')


class SecondViewController(UIViewController):

  @objc_method
  def onTap_(self, sender):
    navigationController = self.navigationController
    navigationController.popViewControllerAnimated_(True)
    #pdbr.state(navigationController)

  @objc_method
  def doneButtonTapped_(self, sender):
    self.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    _dp('--- viewDidLoad\t -> ViewController')

    self.view.backgroundColor = UIColor.systemGreenColor()
    self.setEdgesForExtendedLayout_(0)
    doneButton = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, self,
                                                 SEL('doneButtonTapped:'))

    self.navigationItem.rightBarButtonItem = doneButton
    self.navigationItem.title = 'Second'

    config = UIButtonConfiguration.tintedButtonConfiguration()
    config.title = 'Tap'
    config.baseBackgroundColor = UIColor.systemPinkColor()
    config.baseForegroundColor = UIColor.systemBlueColor()

    tapButton = UIButton.new()
    tapButton.configuration = config
    tapButton.addTarget_action_forControlEvents_(self, SEL('onTap:'),
                                                 touchUpInside)

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

  @objc_method
  def viewDidAppear_(self, animated: bool):
    # xxx: 引数不要?
    send_super(__class__, self, 'viewDidAppear:')
    _dp('--- viewDidAppear:\t -> ViewController')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewWillDisappear:')
    _dp('--- viewWillDisappear:\t -> ViewController')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewDidDisappear:')
    _dp('--- viewDidDisappear:\t -> ViewController')


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
  presentVC.setModalPresentationStyle_(pageSheet)

  rootVC.presentViewController_animated_completion_(presentVC, True, None)


if __name__ == "__main__":
  is_print = False
  vc = FirstViewController.new()
  present_viewController(vc)


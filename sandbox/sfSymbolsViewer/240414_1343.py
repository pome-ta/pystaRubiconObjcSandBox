from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method, objc_property
from pyrubicon.objc.runtime import SEL, send_super

from mainThread import onMainThread
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

NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

edgeNone = 0  # UIRectEdgeNone
touchUpInside = 1 << 6  # UIControlEventTouchUpInside
done = 0  # UIBarButtonSystemItemDone


# --- present
@onMainThread
def present_viewController(myVC: UIViewController):
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  rootVC = window.rootViewController

  while _presentedVC := rootVC.presentedViewController:
    rootVC = _presentedVC

  myNC = RootNavigationController.alloc().initWithRootViewController_(myVC)

  presentVC = myNC
  '''
  UIModalPresentationFullScreen = 0
  UIModalPresentationPageSheet = 1
  '''
  presentVC.setModalPresentationStyle_(1)

  rootVC.presentViewController_animated_completion_(presentVC, True, None)


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
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)

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
class MainViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    #self.navigationItem.title = 'main'

    # --- View
    self.view.backgroundColor = UIColor.systemBlueColor()
    self.SfSymbolsVC = SfSymbolsViewController.new()
    self.SfSymbolsView = self.SfSymbolsVC.view
    self.view.addSubview_(self.SfSymbolsView)


# --- SF Symbols

# --- UITableView
UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')

UITableViewDataSource = ObjCProtocol('UITableViewDataSource')
UITableViewDelegate = ObjCProtocol('UITableViewDelegate')

UITableViewStylePlain = 0
UITableViewStyleGrouped =1
UITableViewStyleInsetGrouped = 2

# --- TableView
class SfSymbolsViewController(
    UIViewController, protocols=[UITableViewDataSource, UITableViewDelegate]):

  #tableView: UITableView = objc_property()

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    self.tableView = UITableView.new()
    # xxx: `initWithFrame_style_` readonly ?
    self.tableView.style = UITableViewStyleGrouped
    #pdbr.state(self.tableView)
    
    
    return self

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    #self.navigationItem.title = 'main'

    # --- View
    self.view.backgroundColor = UIColor.systemGreenColor()

  @objc_method
  def setup(self):
    pass


if __name__ == "__main__":
  mainVC = SfSymbolsViewController.new()
  present_viewController(mainVC)


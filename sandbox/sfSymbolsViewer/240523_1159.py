from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method, objc_property
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
  presentVC.setModalPresentationStyle_(0)

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


# --- SF Symbols
import ctypes
from pathlib import Path
import plistlib
from pyrubicon.objc.types import NSInteger, CGRectMake

UIImage = ObjCClass('UIImage')
# --- UITableView
UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')

# --- TableView
UITableViewDataSource = ObjCProtocol('UITableViewDataSource')
UITableViewDelegate = ObjCProtocol('UITableViewDelegate')

UITableViewStylePlain = 0
UITableViewStyleGrouped = 1
UITableViewStyleInsetGrouped = 2


def get_order_list():
  CoreGlyphs_path = '/System/Library/CoreServices/CoreGlyphs.bundle/'

  symbol_order_path = 'symbol_order.plist'
  symbol_order_bundle = Path(CoreGlyphs_path, symbol_order_path)

  order_list = plistlib.loads(symbol_order_bundle.read_bytes())
  return order_list


# --- ViewController
class SfSymbolsViewController(
    UIViewController, protocols=[UITableViewDataSource, UITableViewDelegate]):

  tableView: UITableView = objc_property()

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')

    self.all_items: list = get_order_list()
    self.cell_identifier = 'customCell'

    self.tableView = UITableView.alloc().initWithFrame_style_(
      CGRectMake(0.0, 0.0, 0.0, 0.0), UITableViewStyleGrouped)
    self.tableView.translatesAutoresizingMaskIntoConstraints = False

    self.tableView.registerClass_forCellReuseIdentifier_(
      UITableViewCell, self.cell_identifier)

    return self

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    self.navigationItem.title = 'SF Symbols tableList 😤'

    # --- View
    self.view.backgroundColor = UIColor.systemGreenColor()
    self.tableSetup()

  @objc_method
  def tableSetup(self):
    self.tableView.delegate = self
    self.tableView.dataSource = self

    self.view.addSubview_(self.tableView)

    NSLayoutConstraint.activateConstraints_([
      self.tableView.centerXAnchor.constraintEqualToAnchor_(
        self.view.centerXAnchor),
      self.tableView.centerYAnchor.constraintEqualToAnchor_(
        self.view.centerYAnchor),
      self.tableView.widthAnchor.constraintEqualToAnchor_multiplier_(
        self.view.widthAnchor, 1.0),
      self.tableView.heightAnchor.constraintEqualToAnchor_multiplier_(
        self.view.heightAnchor, 1.0),
    ])

  # --- UITableViewDataSource
  @objc_method
  def tableView_numberOfRowsInSection_(self, tableView,
                                       section: NSInteger) -> NSInteger:

    return len(self.all_items)

  @objc_method
  def tableView_cellForRowAtIndexPath_(self, tableView,
                                       indexPath) -> ctypes.c_void_p:
    cell = tableView.dequeueReusableCellWithIdentifier_forIndexPath_(
      self.cell_identifier, indexPath)

    symbol_name = self.all_items[indexPath.row]

    content = cell.defaultContentConfiguration()
    content.text = symbol_name
    content.image = UIImage.systemImageNamed_(symbol_name)
    content.textProperties.numberOfLines = 1

    cell.contentConfiguration = content

    return cell.ptr

  # --- UITableViewDelegate
  @objc_method
  def tableView_didSelectRowAtIndexPath_(self, tableView, indexPath):
    #tableView.deselectRowAtIndexPath_animated_(indexPath, True)
    print(self.all_items[indexPath.row])


if __name__ == '__main__':
  mainVC = SfSymbolsViewController.new()
  present_viewController(mainVC)



import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method, objc_property
from pyrubicon.objc.runtime import send_super, SEL
from pyrubicon.objc.types import NSInteger, CGRectMake

from rbedge.functions import NSStringFromClass
#from rbedge.enumerations import UITableViewStyle
#from rbedge import present_viewController
from rbedge import pdbr

from ctypes import byref, cast, Structure
import functools

from pyrubicon.objc.api import Block, ObjCClass, ObjCInstance
from pyrubicon.objc.runtime import libobjc, objc_block, objc_id

NSThread = ObjCClass('NSThread')


class struct_dispatch_queue_s(Structure):
  pass  # No _fields_, because this is an opaque structure.


_dispatch_main_q = struct_dispatch_queue_s.in_dll(libobjc, '_dispatch_main_q')


def dispatch_get_main_queue():
  return ObjCInstance(cast(byref(_dispatch_main_q), objc_id))


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





# --- test modules
#from storyboard.buttonViewController import prototypes

#ObjCClass.auto_rename = True
#ObjCProtocol.auto_rename = True # xxx: `__init__.py` にやるかも

UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UITableViewController = ObjCClass('UITableViewController')
UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')

UITableViewDataSource = ObjCProtocol('UITableViewDataSource')
UITableViewDelegate = ObjCProtocol('UITableViewDelegate')


class TableViewControllerTest(UITableViewController,
                              protocols=[
                                UITableViewDataSource,UITableViewDelegate,
                              ]):

  tableView: UITableView = objc_property()
  

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')

    self.cell_identifier = 'customCell'

    self.tableView = UITableView.alloc().initWithFrame_style_(
      CGRectMake(0.0, 0.0, 0.0, 0.0), 0)
    self.tableView.translatesAutoresizingMaskIntoConstraints = False

    self.tableView.registerClass_forCellReuseIdentifier_(
      UITableViewCell, self.cell_identifier)

    return self

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

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

    return 1

  @objc_method
  def tableView_cellForRowAtIndexPath_(self, tableView,
                                       indexPath) -> ctypes.c_void_p:
    cell = tableView.dequeueReusableCellWithIdentifier_forIndexPath_(
      self.cell_identifier, indexPath)
    '''

    content = cell.defaultContentConfiguration()
    content.text = 'symbol_name'
    content.textProperties.numberOfLines = 1

    cell.contentConfiguration = content
    '''

    return cell.ptr


if __name__ == '__main__':
  vc = TableViewControllerTest.new()
  present_viewController(vc)



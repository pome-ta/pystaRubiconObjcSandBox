import sys
import pathlib

parent_level = 3
sys.path.append(str(pathlib.Path(__file__, '../' * parent_level).resolve()))

try:
  import ctypes
  from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method, objc_property
  from pyrubicon.objc.runtime import send_super
  from pyrubicon.objc.types import NSInteger, CGRectMake

  from rbedge.functions import NSStringFromClass
  from rbedge.enumerations import UITableViewStyle
  from rbedge import present_viewController
  from rbedge import pdbr
except Exception as e:
  # xxx: `(ModuleNotFoundError, LookupError)`
  print(f'{e}: error')

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
#UITableViewDelegate = ObjCProtocol('UITableViewDelegate')


class TableViewControllerTest(UITableViewController,
                              protocols=[
                                UITableViewDataSource,
                              ]):

  tableView: UITableView = objc_property()
  

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')

    self.cell_identifier = 'customCell'

    self.tableView = UITableView.alloc().initWithFrame_style_(
      CGRectMake(0.0, 0.0, 0.0, 0.0), UITableViewStyle.plain)
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
    #self.tableView.delegate = self
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

    content = cell.defaultContentConfiguration()
    content.text = 'symbol_name'
    content.textProperties.numberOfLines = 1

    cell.contentConfiguration = content

    return cell.ptr


if __name__ == '__main__':
  vc = TableViewControllerTest.new()
  present_viewController(vc)


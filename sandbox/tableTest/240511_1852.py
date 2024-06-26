import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, objc_method
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import NSInteger

from rbedge.enumerations import UITableViewStyle
from rbedge.functions import NSStringFromClass
from rbedge import present_viewController
from rbedge import pdbr

UITableViewController = ObjCClass('UITableViewController')
UITableViewCell = ObjCClass('UITableViewCell')

UITableView = ObjCClass('UITableView')  # todo: 型ヒント

UIColor = ObjCClass('UIColor')


class TableViewControllerTest(UITableViewController):
  '''
  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    self.cell_identifier = 'customCell'
    return self

  '''

  @objc_method
  def initWithStyle_(self, style: ctypes.c_void_p):
    self = send_super(__class__, self, 'initWithStyle:')
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
    self.tableView.registerClass_forCellReuseIdentifier_(
      UITableViewCell, self.cell_identifier)

  # --- UITableViewDataSource
  @objc_method
  def tableView_numberOfRowsInSection_(self, tableView,
                                       section: NSInteger) -> NSInteger:
    return 1

  @objc_method
  def tableView_cellForRowAtIndexPath_(self, tableView,
                                       indexPath) -> ctypes.c_void_p:

    #print(indexPath)
    cell = tableView.dequeueReusableCellWithIdentifier_forIndexPath_(
      self.cell_identifier, indexPath)

    content = cell.defaultContentConfiguration()
    content.text = self.cell_identifier
    content.textProperties.numberOfLines = 1

    cell.contentConfiguration = content
    #pdbr.state(tableView)
    #print(tableView.style)
    return cell.ptr


if __name__ == '__main__':
  vc = TableViewControllerTest.new()
  present_viewController(vc)


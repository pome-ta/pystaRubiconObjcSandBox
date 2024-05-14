import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, objc_method
from pyrubicon.objc.runtime import send_super, libobjc, objc_super, SEL
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

  @objc_method
  def initWithStyle_(self, style: NSInteger):
    #send_super(__class__, self, 'init')
    self.cell_identifier = 'customCell'

    super_sel = SEL('initWithStyle:')
    '''

    super_ptr = libobjc.class_getSuperclass(__class__._as_parameter_)

    super_struct = objc_super(self._as_parameter_, super_ptr)

    send = libobjc.objc_msgSendSuper
    send.restype = ctypes.c_void_p
    send.argtypes = [
      ctypes.POINTER(objc_super),
      SEL,
      NSInteger,
    ]
    _args = [
      ctypes.byref(super_struct),
      super_sel,
      style,
    ]
    _this = send(*_args)
    return ObjCInstance(_this)
    '''
    self_ptr = send_super(__class__,
                          self,
                          'initWithStyle:',
                          style,
                          argtypes=[NSInteger])
    return ObjCInstance(self_ptr)

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
    return 3

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
  #vc = TableViewControllerTest.new()
  vc = TableViewControllerTest.alloc().initWithStyle_(2)
  present_viewController(vc)


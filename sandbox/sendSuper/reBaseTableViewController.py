import ctypes
from pyrubicon.objc.api import ObjCClass, objc_method, objc_property, ObjCInstance, NSMutableArray
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import NSInteger

from rbedge.enumerations import UIListContentTextAlignment

from caseElement import CaseElement  # todo: 型呼び出し

UITableViewController = ObjCClass('UITableViewController')
UITableViewHeaderFooterView = ObjCClass('UITableViewHeaderFooterView')
UIListContentConfiguration = ObjCClass('UIListContentConfiguration')


class BaseTableViewController(UITableViewController):
  #testCells = objc_property(ctypes.py_object)
  #headerFooterView_identifier = objc_property()

  @objc_method
  def initWithStyle_(self, style: NSInteger) -> ObjCInstance:
    _this = send_super(__class__,
                       self,
                       'initWithStyle:',
                       style,
                       restype=objc_id,
                       argtypes=[
                         NSInteger,
                       ])
    this = ObjCInstance(_this)
    #print('initWithStyle: base')
    this.testCells: list[CaseElement] = []
    this.headerFooterView_identifier = 'customHeaderFooterView'
    return this

  '''
  @objc_method
  def dealloc(self):
    #send_super(__class__, self, 'dealloc')
    #print('\tdealloc: base')
    pass
  '''

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    self.tableView.registerClass_forHeaderFooterViewReuseIdentifier_(
      UITableViewHeaderFooterView, self.headerFooterView_identifier)

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewDidDisappear: base')
    self.testCells = None
    self.headerFooterView_identifier = None

  @objc_method
  def centeredHeaderView_(self, title):
    headerView = self.tableView.dequeueReusableHeaderFooterViewWithIdentifier_(
      self.headerFooterView_identifier)

    content = UIListContentConfiguration.groupedHeaderConfiguration()
    content.text = title
    content.textProperties.alignment = UIListContentTextAlignment.center
    headerView.contentConfiguration = content

    return headerView

  # MARK: - UITableViewDataSource
  @objc_method
  def tableView_viewForHeaderInSection_(self, tableView,
                                        section: NSInteger) -> objc_id:
    return self.centeredHeaderView_(self.testCells[section].title)

  @objc_method
  def tableView_titleForHeaderInSection_(self, tableView, section: NSInteger):
    return self.testCells[section].title

  @objc_method
  def tableView_numberOfRowsInSection_(self, tableView,
                                       section: NSInteger) -> NSInteger:
    return 1

  @objc_method
  def numberOfSectionsInTableView_(self, tableView) -> NSInteger:
    return len(self.testCells)

  @objc_method
  def tableView_cellForRowAtIndexPath_(self, tableView, indexPath) -> objc_id:
    cellTest = self.testCells[indexPath.section]
    cell = tableView.dequeueReusableCellWithIdentifier_forIndexPath_(
      cellTest.cellID, indexPath)

    if (view := cellTest.targetView(cell)):
      cellTest.configHandler(view)

    return cell


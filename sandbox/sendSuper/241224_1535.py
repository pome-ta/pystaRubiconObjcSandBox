'''
note: 素の継承は`dealloc` 呼べてる
  - 同ファイル上でsubClass 作る
'''

import ctypes
from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import NSInteger

from rbedge.enumerations import (
  UITableViewStyle, )
from rbedge import pdbr

UITableViewController = ObjCClass('UITableViewController')
UITableViewHeaderFooterView = ObjCClass('UITableViewHeaderFooterView')
UIListContentConfiguration = ObjCClass('UIListContentConfiguration')


class BaseTableViewController(UITableViewController):

  #testCells: list = []

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    self.tableView.registerClass_forHeaderFooterViewReuseIdentifier_(
      UITableViewHeaderFooterView, 'customHeaderFooterView')

  @objc_method
  def centeredHeaderView_(self, title):
    # todo: let headerView: UITableViewHeaderFooterView = UITableViewHeaderFooterView()
    headerView = self.tableView.dequeueReusableHeaderFooterViewWithIdentifier_(
      'customHeaderFooterView')

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


class TableViewController(BaseTableViewController):

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
    print('initWithStyle')
    return this

  @objc_method
  def dealloc(self):
    #send_super(__class__, self, 'dealloc')
    print('\tdealloc')

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    #pdbr.state(self, 1)
    print('viewDidLoad')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print('viewDidAppear')
    #pdbr.state(self, 1)

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print('viewDidDisappear')
    #print(self.retainCount())

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print('didReceiveMemoryWarning')


if __name__ == '__main__':
  from rbedge.functions import NSStringFromClass
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController

  _style = UITableViewStyle.grouped
  main_vc = TableViewController.alloc().initWithStyle_(_style)
  _title = NSStringFromClass(TableViewController)
  main_vc.navigationItem.title = _title

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  #style = UIModalPresentationStyle.popover

  present_viewController(main_vc, style)


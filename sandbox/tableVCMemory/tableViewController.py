'''
  note: 空の`UITableViewController` を出す
'''

import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.api import NSString
from pyrubicon.objc.runtime import objc_id, send_super
from pyrubicon.objc.types import NSInteger

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UITableViewController = ObjCClass('UITableViewController')
UITableViewHeaderFooterView = ObjCClass('UITableViewHeaderFooterView')
UIListContentConfiguration = ObjCClass('UIListContentConfiguration')

UITableViewController = ObjCClass('UITableViewController')
UITableViewCell = ObjCClass('UITableViewCell')


items = ['ほげ', 'ふが',]  # yapf: disable


class TableViewController(UITableViewController):

  cellItems = NSString = objc_property()
  cellIdentifier: NSString = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t\t- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    print(f'\t\t{NSStringFromClass(__class__)}: loadView')

  @objc_method
  def initWithStyle_(self, style: NSInteger) -> ObjCClass:
    send_super(__class__,
               self,
               'initWithStyle:',
               style,
               restype=objc_id,
               argtypes=[
                 NSInteger,
               ])
    print(f'\t\t{NSStringFromClass(__class__)}: initWithStyle:')
    self.cellItems = items
    #self.cellItems=['ほげ', 'ふが',]  # yapf: disable
    self.cellIdentifier = NSString.stringWithString_('customCell')
    self.tableView.registerClass_forCellReuseIdentifier_(
      UITableViewCell, self.cellIdentifier)
    return self

  # MARK: - UITableViewDataSource
  @objc_method
  def tableView_numberOfRowsInSection_(self, tableView,
                                       section: NSInteger) -> NSInteger:
    return 1

  @objc_method
  def numberOfSectionsInTableView_(self, tableView) -> NSInteger:
    return len(self.cellItems)

  @objc_method
  def tableView_cellForRowAtIndexPath_(self, tableView, indexPath) -> objc_id:
    cell = tableView.dequeueReusableCellWithIdentifier_forIndexPath_(
      self.cellIdentifier, indexPath)
    content = cell.defaultContentConfiguration()
    content.text = self.cellItems[indexPath.section]
    #print(indexPath)
    #pdbr.state(indexPath)
    content.textProperties.numberOfLines = 1

    cell.contentConfiguration = content

    return cell


if __name__ == '__main__':
  from rbedge.app import App

  from rbedge.enumerations import (
    UITableViewStyle,
    UIModalPresentationStyle,
  )

  table_style = UITableViewStyle.plain
  main_vc = TableViewController.alloc().initWithStyle_(table_style)
  _title = NSStringFromClass(TableViewController)
  main_vc.navigationItem.title = _title

  presentation_style = UIModalPresentationStyle.fullScreen
  app = App(main_vc)
  app.main_loop(presentation_style)


from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, objc_id

from rbedge.enumerations import (
  UITableViewStyle, )
from rbedge import pdbr

UITableViewController = ObjCClass('UITableViewController')


class TableViewController(UITableViewController):
  # MARK: - View Life Cycle

  @objc_method
  def dealloc(self):
    send_super(__class__, self, 'dealloc')
    print('dealloc')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    #pdbr.state(self, 1)

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


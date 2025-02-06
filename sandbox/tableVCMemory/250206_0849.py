'''
  note: 空の`UITableViewController` を出す
'''

import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import objc_id, send_super
from pyrubicon.objc.types import NSInteger

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UITableViewController = ObjCClass('UITableViewController')
UITableViewHeaderFooterView = ObjCClass('UITableViewHeaderFooterView')
UIListContentConfiguration = ObjCClass('UIListContentConfiguration')


UITableViewController = ObjCClass('UITableViewController')

class TableViewController(UITableViewController):
  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #pdbr.state(self)
    print(f'\t\t- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    print(f'\t\t{NSStringFromClass(__class__)}: loadView')

  @objc_method
  def initWithStyle_(self, style: NSInteger) -> ObjCInstance:
    send_super(__class__,
               self,
               'initWithStyle:',
               style,
               restype=objc_id,
               argtypes=[
                 NSInteger,
               ])
    print(f'\t\t{NSStringFromClass(__class__)}: initWithStyle:')
    return self

if __name__ == '__main__':
  from rbedge.app import App

  from rbedge.enumerations import (
    UITableViewStyle,
    UIModalPresentationStyle,
  )

  table_style = UITableViewStyle.grouped
  main_vc = TableViewController.alloc().initWithStyle_(table_style)
  _title = NSStringFromClass(TableViewController)
  main_vc.navigationItem.title = _title

  presentation_style = UIModalPresentationStyle.fullScreen
  app = App(main_vc)
  app.main_loop(presentation_style)


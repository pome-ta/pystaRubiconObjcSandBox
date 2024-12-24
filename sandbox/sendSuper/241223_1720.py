import ctypes
from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, objc_id

from rbedge.enumerations import (
  UITableViewStyle, )
from rbedge import pdbr

UITableViewController = ObjCClass('UITableViewController')
'''
def send_super(
    cls,
    receiver,
    selector,
    *args,
    restype=c_void_p,
    argtypes=None,
    varargs=None,
    _allow_dealloc=False,
):
'''


class TableViewController(UITableViewController):


  @objc_method
  def init(self):
    send_super(__class__, self, 'init')  # xxx: 不要?
    print('init')
    return self

  @objc_method
  def initWithStyle_(self, style: objc_id) -> ObjCInstance:
    this = send_super(__class__,
                      self,
                      'initWithStyle:',
                      style,
                      restype=objc_id,
                      argtypes=[
                        objc_id,
                      ])
    print('h')
    #return self
    print(this)
    print(ObjCInstance(this))
    print(self)
    return ObjCInstance(this)

  @objc_method
  def dealloc(self):
    #send_super(__class__, self, 'dealloc')
    print('dealloc')

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    #pdbr.state(self, 1)

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
    print(self.retainCount())

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


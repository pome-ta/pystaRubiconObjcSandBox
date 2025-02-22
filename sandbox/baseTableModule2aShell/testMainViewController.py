import ctypes
from enum import Enum

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, objc_id, SEL
from pyrubicon.objc.types import NSInteger

from caseElement import CaseElement

from baseTableViewController import BaseTableViewController
from storyboard.testMainViewController import prototypes

from rbedge.enumerations import (
  UIControlState,
  UIControlEvents,
  UIButtonConfigurationCornerStyle,
  UIImageRenderingMode,
  NSUnderlineStyle,
  UIImageSymbolScale,
  NSDirectionalRectEdge,
  UIButtonConfigurationSize,
)

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIColor = ObjCClass('UIColor')


class testKind(Enum):
  hoge = 'hoge'
  fuga = 'fuga'


class TestMainViewController(BaseTableViewController):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t- {NSStringFromClass(__class__)}: dealloc')

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
    #print(f'\t{NSStringFromClass(__class__)}: initWithStyle_')
    return self

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    #print(f'\t{NSStringFromClass(__class__)}: loadView')
    [
      self.tableView.registerClass_forCellReuseIdentifier_(
        prototype['cellClass'], prototype['identifier'])
      for prototype in prototypes
    ]

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    #print(f'\t{NSStringFromClass(__class__)}: viewDidLoad')
    self.navigationItem.title = 'title' if (
      title := self.navigationItem.title) is None else title

    c1 = CaseElement.alloc().initWithTitle_cellID_configHandlerName_(
      'hogehoge', testKind.hoge.value, 'configureHogeView:')

    self.testCells.addObject_(c1)

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewDidAppear_')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    # print('\t↑ ---')
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    # print(f'\t{NSStringFromClass(__class__)}: viewWillDisappear_')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'\t{NSStringFromClass(__class__)}: viewDidDisappear_')
    # xxx: a-shell で動くけど、Pythonista3 の2回目の`dealloc` が呼ばれない
    #self.testCells = None

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  # MARK: - Configuration
  @objc_method
  def configureHogeView_(self, button):
    button.addTarget_action_forControlEvents_(self, SEL('buttonClicked:'),UIControlEvents.touchUpInside)
    

  @objc_method
  def configureFugaView_(self, button):
    pass

  # MARK: - Button Actions
  @objc_method
  def buttonClicked_(self, sender):
    print(f'Button was clicked.{sender}')


if __name__ == '__main__':
  from rbedge.app import App

  from rbedge.enumerations import (
    UITableViewStyle,
    UIModalPresentationStyle,
  )

  print('__name__')

  table_style = UITableViewStyle.grouped
  main_vc = TestMainViewController.alloc().initWithStyle_(table_style)
  _title = NSStringFromClass(TestMainViewController)
  main_vc.navigationItem.title = _title

  # presentation_style = UIModalPresentationStyle.fullScreen
  presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc)
  print('---')
  app.main_loop(presentation_style)
  print('--- end ---\n')


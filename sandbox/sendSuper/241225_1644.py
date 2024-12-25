'''
note: 素の継承は`dealloc` 呼べてる
  - 外部モジュールとして呼び出し
  - サンプル要素を追加
    - 要素呼び出しで、`dealloc` が発動しない
    - `self.testCells` 要素を使用後`None` で`dealloc` 出現
    - `property` として、持たせる場合にはどうすれば？
    - `this` じゃなくて`self` でよくね？
'''

import ctypes
from enum import Enum

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import NSInteger

from rbedge.enumerations import (
  UITableViewStyle,
  UIProgressViewStyle,
)
from rbedge import pdbr

from caseElement import CaseElement
from pyLocalizedString import localizedString

from reBaseTableViewController import BaseTableViewController
from storyboard.progressViewController import prototypes

UIColor = ObjCClass('UIColor')


# Cell identifier for each progress view table view cell.
class ProgressViewKind(Enum):
  defaultProgress = 'defaultProgress'
  barProgress = 'barProgress'
  tintedProgress = 'tintedProgress'


class TableViewController(BaseTableViewController):

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

    print('initWithStyle')
    '''
    [
      this.tableView.registerClass_forCellReuseIdentifier_(
        prototype['cellClass'], prototype['identifier'])
      for prototype in prototypes
    ]
    '''
    self.initPrototype()
    return self

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #pdbr.state(self)
    print('\tdealloc')

  @objc_method
  def initPrototype(self):
    [
      self.tableView.registerClass_forCellReuseIdentifier_(
        prototype['cellClass'], prototype['identifier'])
      for prototype in prototypes
    ]

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    print('viewDidLoad')
    self.navigationItem.title = localizedString('SymbolsTitle') if (
      title := self.navigationItem.title) is None else title

    self.testCells.extend([
      CaseElement(localizedString('ProgressDefaultTitle'),
                  ProgressViewKind.defaultProgress.value,
                  self.configureDefaultStyleProgressView_),
      CaseElement(localizedString('ProgressBarTitle'),
                  ProgressViewKind.barProgress.value,
                  self.configureBarStyleProgressView_),
    ])
    if True:  # wip: `traitCollection.userInterfaceIdiom != .mac`
      # Tinted progress views available only on iOS.
      self.testCells.extend([
        CaseElement(localizedString('ProgressTintedTitle'),
                    ProgressViewKind.tintedProgress.value,
                    self.configureTintedProgressView_),
      ])

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

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewDidDisappear')
    self.testCells = None
    #pdbr.state(self)

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print('didReceiveMemoryWarning')


# MARK: - Configuration

  @objc_method
  def configureDefaultStyleProgressView_(self, progressView):
    progressView.progressViewStyle = UIProgressViewStyle.default
    # Reset the completed progress of the `UIProgressView`s.
    progressView.setProgress_animated_(0.0, False)

  @objc_method
  def configureBarStyleProgressView_(self, progressView):
    progressView.progressViewStyle = UIProgressViewStyle.bar
    # Reset the completed progress of the `UIProgressView`s.
    progressView.setProgress_animated_(0.0, False)

  @objc_method
  def configureTintedProgressView_(self, progressView):
    progressView.progressViewStyle = UIProgressViewStyle.default
    progressView.trackTintColor = UIColor.systemBlueColor()
    progressView.progressTintColor = UIColor.systemPurpleColor()

    # Reset the completed progress of the `UIProgressView`s.
    progressView.setProgress_animated_(0.0, False)

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


if __name__ == '__main__':
  try:
    import bootstrap
  except ModuleNotFoundError as e:
    _TARGET_NAME = 'bootstrap'
    if e.name != _TARGET_NAME:
      raise
    import pathlib as _pathlib, runpy as _runpy

    _runpy.run_path(
      next(
        filter(
          _pathlib.Path.is_file,
          (_dir / f'{_TARGET_NAME}.py'
           for _dir in _pathlib.Path(__file__).resolve().parents),
        ),
        f'{_TARGET_NAME} not found',
      ))

import ctypes

from pyrubicon.objc import (
  ObjCClass,
  ObjCInstance,
  objc_method,
  objc_property,
)  # api
from pyrubicon.objc import send_super, objc_id  # runtime
from pyrubicon.objc import NSInteger  # types

from objc_frameworks.Foundation import NSStringFromClass

from rbedge import pdbr

from storyboard_buttonViewController import prototypes

test_prototypes = prototypes if isinstance(prototypes, list) else [prototypes]

UITableViewController = ObjCClass('UITableViewController')
UITableViewCell = ObjCClass('UITableViewCell')
UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')


class ButtonViewControllerTest(UITableViewController):

  @objc_method
  def dealloc(self) -> None:
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t- {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def initWithStyle_(self, style: NSInteger) -> ObjCInstance:
    self = ObjCInstance(
      send_super(
        __class__,
        self,
        'initWithStyle:',
        style,
        restype=objc_id,
        argtypes=[
          NSInteger,
        ],
      ))
    if self is None:
      return None
    #print(f'\t{NSStringFromClass(__class__)}: initWithStyle_')
    return self

  @objc_method
  def loadView(self) -> None:
    send_super(
      __class__,
      self,
      'loadView',
      restype=None,
    )
    #print(f'{NSStringFromClass(__class__)}: loadView')
    [
      self.tableView.registerClass_forCellReuseIdentifier_(
        prototype['cellClass'], prototype['identifier'])
      for prototype in test_prototypes
    ]

  @objc_method
  def viewDidLoad(self) -> None:
    send_super(
      __class__,
      self,
      'viewDidLoad',
      restype=None,
    )
    # --- Navigation
    self.navigationItem.title = NSStringFromClass(__class__) if (
      title := self.navigationItem.title) is None else title
    # --- View
    self.view.backgroundColor = UIColor.systemDarkGreenColor()

  @objc_method
  def viewWillAppear_(self, animated: bool) -> None:
    send_super(
      __class__,
      self,
      'viewWillAppear:',
      animated,
      restype=None,
      argtypes=[
        ctypes.c_bool,
      ],
    )
    #print(f'\t{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool) -> None:
    send_super(
      __class__,
      self,
      'viewDidAppear:',
      animated,
      restype=None,
      argtypes=[
        ctypes.c_bool,
      ],
    )
    #print(f'\t{NSStringFromClass(__class__)}: viewDidAppear_')

  @objc_method
  def viewWillDisappear_(self, animated: bool) -> None:
    send_super(
      __class__,
      self,
      'viewWillDisappear:',
      animated,
      restype=None,
      argtypes=[
        ctypes.c_bool,
      ],
    )
    # print(f'\t{NSStringFromClass(__class__)}: viewWillDisappear_')

  @objc_method
  def viewDidDisappear_(self, animated: bool) -> None:
    send_super(
      __class__,
      self,
      'viewDidDisappear:',
      animated,
      restype=None,
      argtypes=[
        ctypes.c_bool,
      ],
    )
    #print(f'\t{NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self) -> None:
    send_super(
      __class__,
      self,
      'didReceiveMemoryWarning',
      restype=None,
    )
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')



  # --- UITableViewDataSource
  @objc_method
  def tableView_numberOfRowsInSection_(
    self,
    tableView,
    section: NSInteger,
  ) -> NSInteger:

    return len(test_prototypes)

  @objc_method
  def tableView_cellForRowAtIndexPath_(
    self,
    tableView,
    indexPath,
  ) -> ObjCInstance:

    identifier = test_prototypes[indexPath.row]['identifier']

    cell = tableView.dequeueReusableCellWithIdentifier_forIndexPath_(
      identifier,
      indexPath,
    )

    return cell


if __name__ == '__main__':

  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle, UITableViewStyle

  table_style = UITableViewStyle.grouped

  main_vc = ButtonViewControllerTest.alloc().initWithStyle_(table_style)
  _title = NSStringFromClass(ButtonViewControllerTest)
  main_vc.navigationItem.title = _title

  #presentation_style = UIModalPresentationStyle.fullScreen
  presentation_style = UIModalPresentationStyle.pageSheet

  app = App.alloc().initWithViewController_(main_vc)
  app.presentWithStyle_(presentation_style)

  try:
    import gc
    gc.collect()
  except Exception as e:
    print('--- collect: error')
    print(f'{e}')


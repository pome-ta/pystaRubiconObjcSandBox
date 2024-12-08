'''
  note: 
    - [【Swift】世界一わかりやすいTableViewのアコーディオンの実装方法 #Xode - Qiita](https://qiita.com/tosh_3/items/c254429f4f68c7eab39d)
'''

import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCProtocol, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property, objc_const
from pyrubicon.objc.runtime import send_super, objc_id, load_library

from rbedge.enumerations import (
  UITableViewStyle, )
from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- TableView
UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')
UITableViewDataSource = ObjCProtocol('UITableViewDataSource')
UITableViewDelegate = ObjCProtocol('UITableViewDelegate')

# --- others
UIColor = ObjCClass('UIColor')


class ViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    # --- Navigation
    send_super(__class__, self, 'viewDidLoad')
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    # --- View
    self.view.backgroundColor = UIColor.systemBrownColor()  # todo: 確認用

    # --- Table set
    self.cell_identifier = 'customCell'

    tableView = UITableView.alloc().initWithFrame_style_(
      self.view.bounds, UITableViewStyle.plain)
    tableView.registerClass_forCellReuseIdentifier_(UITableViewCell,
                                                    self.cell_identifier)

    tableView.delegate = self
    tableView.dataSource = self

    # --- Layout
    self.view.addSubview_(tableView)
    tableView.translatesAutoresizingMaskIntoConstraints = False
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide
    NSLayoutConstraint.activateConstraints_([
      tableView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      tableView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      tableView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 1.0),
      tableView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 1.0),
    ])

  # --- UITableViewDataSource
  @objc_method
  def tableView_numberOfRowsInSection_(self, tableView, section) -> int:

    return 1

  @objc_method
  def tableView_cellForRowAtIndexPath_(self, tableView, indexPath) -> objc_id:
    cell = tableView.dequeueReusableCellWithIdentifier_forIndexPath_(
      self.cell_identifier, indexPath)

    content = cell.defaultContentConfiguration()
    content.text = 'h'

    cell.contentConfiguration = content

    return cell

  # --- UITableViewDelegate
  @objc_method
  def tableView_didSelectRowAtIndexPath_(self, tableView, indexPath):
    pass


if __name__ == '__main__':
  from rbedge import present_viewController
  from rbedge.enumerations import UIModalPresentationStyle

  vc = ViewController.new()

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)


'''
  note: 
    - [【Swift】世界一わかりやすいTableViewのアコーディオンの実装方法 #Xode - Qiita](https://qiita.com/tosh_3/items/c254429f4f68c7eab39d)
    - 開閉
'''

import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id, SEL
from pyrubicon.objc.types import NSInteger

from rbedge.enumerations import (
  UITableViewStyle,
  UITableViewRowAnimation,
)
from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- TableView
UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')
UITableViewHeaderFooterView = ObjCClass('UITableViewHeaderFooterView')
UITableViewDataSource = ObjCProtocol('UITableViewDataSource')
UITableViewDelegate = ObjCProtocol('UITableViewDelegate')

UITapGestureRecognizer = ObjCClass('UITapGestureRecognizer')
NSIndexSet = ObjCClass('NSIndexSet')

# --- others
UIColor = ObjCClass('UIColor')


class Rail:

  def __init__(self, railName: str, stationArray: list, isShown: bool = True):
    self.isShown = isShown
    self.railName = railName
    self.stationArray = stationArray



headerArray = ['山手線', '東横線', '田園都市線', '常磐線',] # yapf: disable
yamanoteArray = ['渋谷', '新宿', '池袋',] # yapf: disable
toyokoArray = ['自由ヶ丘', '日吉',] # yapf: disable
dentoArray = ['溝の口', '二子玉川',] # yapf: disable
jobanArray = ['上野',] # yapf: disable


courseArray = [
  Rail(rail, stations) for rail, stations in zip(headerArray, [
    yamanoteArray,
    toyokoArray,
    dentoArray,
    jobanArray,
  ])
]


class ViewController(UIViewController):

  tableView: UITableView = objc_property()

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
    self.headerFooterView_identifier = 'customHeaderFooterView'

    tableView = UITableView.alloc().initWithFrame_style_(
      self.view.bounds, UITableViewStyle.plain)
    tableView.registerClass_forCellReuseIdentifier_(UITableViewCell,
                                                    self.cell_identifier)

    tableView.registerClass_forHeaderFooterViewReuseIdentifier_(
      UITableViewHeaderFooterView, self.headerFooterView_identifier)

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
    self.tableView = tableView

  # --- UITableViewDataSource
  @objc_method
  def tableView_numberOfRowsInSection_(self, tableView, section: int) -> int:
    return len(rail.stationArray) if (rail :=
                                      courseArray[section]).isShown else 0

  @objc_method
  def tableView_cellForRowAtIndexPath_(self, tableView, indexPath):
    cell = tableView.dequeueReusableCellWithIdentifier_forIndexPath_(
      self.cell_identifier, indexPath)

    content = cell.defaultContentConfiguration()
    content.text = courseArray[indexPath.section].stationArray[indexPath.row]

    cell.contentConfiguration = content

    return cell

  @objc_method
  def numberOfSectionsInTableView_(self, tableView) -> int:
    return len(courseArray)

  @objc_method
  def tableView_titleForHeaderInSection_(self, tableView, section: int):

    return courseArray[section].railName

  # --- UITableViewDelegate
  @objc_method
  def tableView_viewForHeaderInSection_(self, tableView, section: int):
    headerView = tableView.dequeueReusableHeaderFooterViewWithIdentifier_(
      self.headerFooterView_identifier)

    gesture = UITapGestureRecognizer.alloc().initWithTarget_action_(
      self, SEL('headertapped:'))
    headerView.addGestureRecognizer_(gesture)
    headerView.tag = section
    return headerView

  @objc_method
  def headertapped_(self, sender):

    if (section := sender.view.tag) is None:
      return
    courseArray[section].isShown = not courseArray[section].isShown

    self.tableView.beginUpdates()
    self.tableView.reloadSections_withRowAnimation_(
      NSIndexSet.indexSetWithIndex_(section),
      UITableViewRowAnimation.automatic)
    self.tableView.endUpdates()


if __name__ == '__main__':
  from rbedge import present_viewController
  from rbedge.enumerations import UIModalPresentationStyle

  vc = ViewController.new()

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)


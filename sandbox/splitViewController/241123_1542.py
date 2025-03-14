'''
  note:
    `UISplitViewController` と、`UITableView`
'''
import ctypes
from pathlib import Path
import plistlib

from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGRectMake

from rbedge.enumerations import (
  UISplitViewControllerStyle,
  UISplitViewControllerColumn,
  UITableViewStyle,
)
from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- SplitView
UISplitViewController = ObjCClass('UISplitViewController')
UISplitViewControllerDelegate = ObjCProtocol('UISplitViewControllerDelegate')
UITableViewCell = ObjCClass('UITableViewCell')

# --- TableView
UITableView = ObjCClass('UITableView')
UITableViewDataSource = ObjCProtocol('UITableViewDataSource')
UITableViewDelegate = ObjCProtocol('UITableViewDelegate')

# --- others
UIColor = ObjCClass('UIColor')
UILabel = ObjCClass('UILabel')
UIFont = ObjCClass('UIFont')
UIImage = ObjCClass('UIImage')


def get_order_list():
  CoreGlyphs_path = '/System/Library/CoreServices/CoreGlyphs.bundle/'

  symbol_order_path = 'symbol_order.plist'
  symbol_order_bundle = Path(CoreGlyphs_path, symbol_order_path)

  order_list = plistlib.loads(symbol_order_bundle.read_bytes())
  return order_list


class PrimaryTableViewController(UIViewController,
                                 protocols=[
                                   UITableViewDataSource,
                                   UITableViewDelegate,
                                 ]):

  tableView: UITableView = objc_property()

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    self.tableView = UITableView.alloc().initWithFrame_style_(
      CGRectMake(0.0, 0.0, 0.0, 0.0), UITableViewStyle.plain)

    self.all_items: list = get_order_list()

    self.cell_identifier = 'customCell'
    self.tableView.registerClass_forCellReuseIdentifier_(
      UITableViewCell, self.cell_identifier)

    return self

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')

    # --- View
    self.view.backgroundColor = UIColor.systemGreenColor()  # todo: 確認用
    self.view.addSubview_(self.tableView)

    # --- Table set
    self.tableView.delegate = self
    self.tableView.dataSource = self

    # --- Layout
    self.tableView.translatesAutoresizingMaskIntoConstraints = False
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide
    NSLayoutConstraint.activateConstraints_([
      self.tableView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      self.tableView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      self.tableView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 1.0),
      self.tableView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 1.0),
    ])

  # --- UITableViewDataSource
  @objc_method
  def tableView_numberOfRowsInSection_(self, tableView, section) -> int:

    return len(self.all_items)

  @objc_method
  def tableView_cellForRowAtIndexPath_(self, tableView, indexPath) -> objc_id:
    cell = tableView.dequeueReusableCellWithIdentifier_forIndexPath_(
      self.cell_identifier, indexPath)

    symbol_name = self.all_items[indexPath.row]

    content = cell.defaultContentConfiguration()
    content.text = symbol_name
    content.image = UIImage.systemImageNamed_(symbol_name)
    content.textProperties.numberOfLines = 1

    cell.contentConfiguration = content

    return cell

  # --- UITableViewDelegate
  @objc_method
  def tableView_didSelectRowAtIndexPath_(self, tableView, indexPath):
    #tableView.deselectRowAtIndexPath_animated_(indexPath, True)
    print(self.all_items[indexPath.row])


class PrimaryViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    # --- View
    self.view.backgroundColor = UIColor.systemDarkTealColor()

    self.label = UILabel.new()
    self.label.text = 'Primary'
    self.label.font = UIFont.systemFontOfSize_(26.0)
    self.label.sizeToFit()

    self.view.addSubview_(self.label)

    # --- Layout
    self.label.translatesAutoresizingMaskIntoConstraints = False

    NSLayoutConstraint.activateConstraints_([
      self.label.centerXAnchor.constraintEqualToAnchor_(
        self.view.centerXAnchor),
      self.label.centerYAnchor.constraintEqualToAnchor_(
        self.view.centerYAnchor),
    ])


class SecondaryViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    # --- View
    self.view.backgroundColor = UIColor.systemDarkRedColor()

    self.label = UILabel.new()
    self.label.text = 'Primary'
    self.label.font = UIFont.systemFontOfSize_(26.0)
    self.label.sizeToFit()

    self.view.addSubview_(self.label)

    # --- Layout
    self.label.translatesAutoresizingMaskIntoConstraints = False

    NSLayoutConstraint.activateConstraints_([
      self.label.centerXAnchor.constraintEqualToAnchor_(
        self.view.centerXAnchor),
      self.label.centerYAnchor.constraintEqualToAnchor_(
        self.view.centerYAnchor),
    ])


class SplitViewController(UISplitViewController,
                          protocols=[
                            UISplitViewControllerDelegate,
                          ]):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.delegate = self

    #primary_vc = PrimaryViewController.new()
    primary_vc = PrimaryTableViewController.new()
    primary_vc.title = primary_vc.className()

    secondary_vc = SecondaryViewController.new()

    primary = UISplitViewControllerColumn.primary
    secondary = UISplitViewControllerColumn.secondary

    self.setViewController_forColumn_(primary_vc, primary)
    self.setViewController_forColumn_(secondary_vc, secondary)


class ViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    # --- Navigation
    send_super(__class__, self, 'viewDidLoad')
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    # --- View
    split = SplitViewController.alloc().initWithStyle_(
      UISplitViewControllerStyle.doubleColumn)
    self.addChildViewController_(split)
    self.view.addSubview_(split.view)
    split.didMoveToParentViewController_(self)

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #pdbr.state(self,1)
    #pdbr.state(self.childViewControllers[0])


if __name__ == '__main__':
  from rbedge import present_viewController
  from rbedge.enumerations import UIModalPresentationStyle

  vc = ViewController.new()
  #vc = PrimaryTableViewController.new()

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)


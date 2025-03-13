from pathlib import Path
import plistlib

from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super

from rbedge.enumerations import UITableViewStyle
from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')
UIImage = ObjCClass('UIImage')

NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')


def get_order_list():
  CoreGlyphs_path = '/System/Library/CoreServices/CoreGlyphs.bundle/'

  symbol_order_path = 'symbol_order.plist'
  symbol_order_bundle = Path(CoreGlyphs_path, symbol_order_path)

  order_list = plistlib.loads(symbol_order_bundle.read_bytes())
  return order_list


class SFSymbolsViewController(UIViewController):

  cell_identifier: str = objc_property()
  all_items: list = objc_property()

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    self.cell_identifier = 'customCell'
    self.all_items = get_order_list()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')

    # --- Navigation
    self.navigationItem.title = NSStringFromClass(__class__) if (
      title := self.navigationItem.title) is None else title
    self.view.backgroundColor = UIColor.systemBackgroundColor()

    # --- Table
    sf_tableView = UITableView.alloc().initWithFrame_style_(
      self.view.bounds, UITableViewStyle.plain)
    sf_tableView.registerClass_forCellReuseIdentifier_(UITableViewCell,
                                                       self.cell_identifier)
    sf_tableView.dataSource = self
    sf_tableView.delegate = self

    # --- Layout
    self.view.addSubview_(sf_tableView)
    sf_tableView.translatesAutoresizingMaskIntoConstraints = False
    areaLayoutGuide = self.view.safeAreaLayoutGuide

    NSLayoutConstraint.activateConstraints_([
      sf_tableView.centerXAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerXAnchor),
      sf_tableView.centerYAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerYAnchor),
      sf_tableView.widthAnchor.constraintEqualToAnchor_multiplier_(
        areaLayoutGuide.widthAnchor, 1.0),
      sf_tableView.heightAnchor.constraintEqualToAnchor_multiplier_(
        areaLayoutGuide.heightAnchor, 1.0),
    ])

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  # --- UITableViewDataSource
  @objc_method
  def tableView_numberOfRowsInSection_(self, tableView, section: int) -> int:
    return len(self.all_items)

  @objc_method
  def tableView_cellForRowAtIndexPath_(self, tableView, indexPath):
    cell = tableView.dequeueReusableCellWithIdentifier_forIndexPath_(
      self.cell_identifier, indexPath)

    symbol_name = self.all_items[indexPath.row]

    content = cell.defaultContentConfiguration()
    content.text = symbol_name
    content.textProperties.numberOfLines = 1
    content.image = UIImage.systemImageNamed_(symbol_name)
    cell.contentConfiguration = content

    return cell

  # --- UITableViewDelegate
  @objc_method
  def tableView_didSelectRowAtIndexPath_(self, tableView, indexPath):
    #tableView.deselectRowAtIndexPath_animated_(indexPath, True)
    select_item = self.all_items[indexPath.row]

    print(f'select:\t{select_item}')


if __name__ == '__main__':
  from rbedge.app import App
  from rbedge.enumerations import UIModalPresentationStyle

  main_vc = SFSymbolsViewController.new()
  _title = NSStringFromClass(SFSymbolsViewController)
  main_vc.navigationItem.title = _title

  presentation_style = UIModalPresentationStyle.fullScreen

  app = App(main_vc, presentation_style)
  app.present()


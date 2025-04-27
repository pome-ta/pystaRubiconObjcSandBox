import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super

from rbedge.enumerations import UITableViewStyle

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

# --- UIFontTextStyle
from pyrubicon.objc.runtime import load_library
from pyrubicon.objc.api import objc_const

UIKit = load_library('UIKit')
# xxx: PEP8では非推奨
UIFontTextStyle = lambda const_name: str(objc_const(UIKit, const_name))

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')

UITableViewController = ObjCClass('UITableViewController')
UITableViewHeaderFooterView = ObjCClass('UITableViewHeaderFooterView')
UIListContentConfiguration = ObjCClass('UIListContentConfiguration')

UIFont = ObjCClass('UIFont')

fontTextStyles = [
  'UIFontTextStyleBody',
  'UIFontTextStyleCallout',
  'UIFontTextStyleCaption1',
  'UIFontTextStyleCaption2',
  'UIFontTextStyleFootnote',
  'UIFontTextStyleHeadline',
  'UIFontTextStyleSubheadline',
  'UIFontTextStyleLargeTitle',
  'UIFontTextStyleExtraLargeTitle',
  'UIFontTextStyleExtraLargeTitle2',
  'UIFontTextStyleTitle1',
  'UIFontTextStyleTitle2',
  'UIFontTextStyleTitle3',
]

lipsum = 'あのイーハトーヴォのすきとおった風、夏でも底に冷たさをもつ青いそら、うつくしい森で飾られたモリーオ市、郊外のぎらぎらひかる草の波。'

cells = [[style, [
  style,
  lipsum,
]] for style in fontTextStyles]


class FonTextStylesController(UIViewController):

  cellIdentifier: str = objc_property()
  headerFooterViewIdentifier: str = objc_property()

  @objc_method
  def dealloc(self) -> None:
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'\t\t- {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    #print(f'\t\t{NSStringFromClass(__class__)}: loadView')
    self.cellIdentifier = 'customCell'
    self.headerFooterViewIdentifier = 'customHeaderFooterView'

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    #print(f'\t\t{NSStringFromClass(__class__)}: viewDidLoad')
    # --- Navigation
    self.navigationItem.title = NSStringFromClass(__class__) if (
      title := self.navigationItem.title) is None else title

    # --- Table set
    tableView = UITableView.alloc().initWithFrame_style_(
      self.view.bounds, UITableViewStyle.grouped)

    tableView.registerClass_forCellReuseIdentifier_(UITableViewCell,
                                                    self.cellIdentifier)
    tableView.registerClass_forHeaderFooterViewReuseIdentifier_(
      UITableViewHeaderFooterView, self.headerFooterViewIdentifier)

    tableView.delegate = self
    tableView.dataSource = self

    # --- Layout
    self.view.addSubview_(tableView)
    tableView.translatesAutoresizingMaskIntoConstraints = False
    # areaLayoutGuide = self.view.safeAreaLayoutGuide
    areaLayoutGuide = self.view
    NSLayoutConstraint.activateConstraints_([
      tableView.centerXAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerXAnchor),
      tableView.centerYAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerYAnchor),
      tableView.widthAnchor.constraintEqualToAnchor_multiplier_(
        areaLayoutGuide.widthAnchor, 1.0),
      tableView.heightAnchor.constraintEqualToAnchor_multiplier_(
        areaLayoutGuide.heightAnchor, 1.0),
    ])

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'{__class__}: didReceiveMemoryWarning')

  # --- UITableViewDataSource
  @objc_method
  def numberOfSectionsInTableView_(self, tableView) -> int:
    return len(cells)

  '''
  @objc_method
  def tableView_titleForHeaderInSection_(self, tableView, section: int):
    return cells[section][0]
  '''

  @objc_method
  def tableView_viewForHeaderInSection_(self, tableView, section: int):

    header = tableView.dequeueReusableHeaderFooterViewWithIdentifier_(
      self.headerFooterViewIdentifier)
    #header.textLabel.text = cells[section][0]
    header.text = cells[section][0]
    return header

  @objc_method
  def tableView_numberOfRowsInSection_(self, tableView, section: int) -> int:
    return len(cells[section])

  @objc_method
  def tableView_cellForRowAtIndexPath_(self, tableView, indexPath):
    cell = tableView.dequeueReusableCellWithIdentifier_forIndexPath_(
      self.cellIdentifier, indexPath)

    style = cells[indexPath.section][0]
    text = cells[indexPath.section][1][indexPath.row]

    contentConfiguration = cell.defaultContentConfiguration()
    contentConfiguration.text = text
    contentConfiguration.textProperties.setFont_(
      UIFont.preferredFontForTextStyle_(UIFontTextStyle(style)))

    cell.contentConfiguration = contentConfiguration
    return cell


if __name__ == '__main__':
  from rbedge.app import App
  from rbedge.enumerations import UIModalPresentationStyle

  main_vc = FonTextStylesController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()


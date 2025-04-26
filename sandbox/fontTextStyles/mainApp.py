import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super

from rbedge.enumerations import UITableViewStyle

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')

UITableViewController = ObjCClass('UITableViewController')
UITableViewHeaderFooterView = ObjCClass('UITableViewHeaderFooterView')
UIListContentConfiguration = ObjCClass('UIListContentConfiguration')

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

print(len(cells))


class FonTextStylesTableViewController(UIViewController):

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

    # --- Table set
    tableView = UITableView.alloc().initWithFrame_style_(
      self.view.bounds, UITableViewStyle.grouped)


if __name__ == '__main__':
  from rbedge.app import App
  from rbedge.enumerations import UIModalPresentationStyle

  main_vc = FonTextStylesTableViewController.new()
  _title = NSStringFromClass(FonTextStylesTableViewController)
  main_vc.navigationItem.title = _title

  # presentation_style = UIModalPresentationStyle.fullScreen
  presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()


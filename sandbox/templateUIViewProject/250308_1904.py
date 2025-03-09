from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super

from rbedge.enumerations import UITableViewStyle
from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
UITableView = ObjCClass('UITableView')

NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')


class SFSymbolsViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')

    # --- Navigation
    self.navigationItem.title = NSStringFromClass(__class__) if (
      title := self.navigationItem.title) is None else title

    # --- Table
    sfTableView = UITableView.alloc().initWithFrame_style_(
      self.view.bounds, UITableViewStyle.plain)
    sfTableView.backgroundColor = UIColor.systemCyanColor()
    pdbr.state(UITableView.alloc())

    # --- Layout
    self.view.addSubview_(sfTableView)
    sfTableView.translatesAutoresizingMaskIntoConstraints = False
    areaLayoutGuide = self.view.safeAreaLayoutGuide

    NSLayoutConstraint.activateConstraints_([
      sfTableView.centerXAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerXAnchor),
      sfTableView.centerYAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerYAnchor),
      sfTableView.widthAnchor.constraintEqualToAnchor_multiplier_(
        areaLayoutGuide.widthAnchor, 0.5),
      sfTableView.heightAnchor.constraintEqualToAnchor_multiplier_(
        areaLayoutGuide.heightAnchor, 0.5),
    ])

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')


if __name__ == '__main__':
  from rbedge.app import App
  from rbedge.enumerations import UIModalPresentationStyle

  main_vc = SFSymbolsViewController.new()
  _title = NSStringFromClass(SFSymbolsViewController)
  main_vc.navigationItem.title = _title

  presentation_style = UIModalPresentationStyle.fullScreen

  app = App(main_vc, presentation_style)
  app.present()


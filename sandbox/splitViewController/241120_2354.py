'''
  note:
    `UISplitViewControllerDelegate` 確認
'''

from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super

from rbedge.enumerations import (
  UIViewAutoresizing,
  UISplitViewControllerStyle,
  UISplitViewControllerColumn,
  UISplitViewControllerDisplayMode,
  UIModalPresentationStyle,
)
from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
UISplitViewController = ObjCClass('UISplitViewController')
UISplitViewControllerDelegate = ObjCProtocol('UISplitViewControllerDelegate')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UIColor = ObjCClass('UIColor')
UILabel = ObjCClass('UILabel')
UIFont = ObjCClass('UIFont')

UINavigationController = ObjCClass('UINavigationController')  # todo: 型確認用


class PrimaryViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    # --- Navigation
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title
    #self.navigationItem.title = 'title'

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
    # --- Navigation
    title = NSStringFromClass(__class__)
    #self.navigationItem.title = title

    # --- View
    self.view.backgroundColor = UIColor.systemDarkRedColor()

    self.label = UILabel.new()
    self.label.text = 'Secondary'
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
  
  @objc_method
  def splitViewController_topColumnForCollapsingToProposedTopColumn_(
      self, svc, proposedTopColumn: int):
    return UISplitViewControllerColumn.secondary

  @objc_method
  def splitViewController_displayModeForExpandingToProposedDisplayMode_(
      self, svc, proposedDisplayMode: int):

    if (navController :=
        svc.viewControllers[0]).isMemberOfClass_(UINavigationController):
      navController.popToRootViewControllerAnimated_(False)

    return UISplitViewControllerDisplayMode.automatic


class ViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    title = NSStringFromClass(__class__)

    self.navigationItem.title = title

    # --- View
    split = SplitViewController.alloc().initWithStyle_(
      UISplitViewControllerStyle.doubleColumn)

    self.addChildViewController_(split)
    self.view.addSubview_(split.view)

    split.view.frame = self.view.bounds
    split.view.autoresizingMask = UIViewAutoresizing.flexibleHeight | UIViewAutoresizing.flexibleWidth

    split.didMoveToParentViewController_(self)

    primary_vc = PrimaryViewController.new()
    primary_vc.title = primary_vc.className()

    secondary_vc = SecondaryViewController.new()

    primary = UISplitViewControllerColumn.primary
    secondary = UISplitViewControllerColumn.secondary

    split.setViewController_forColumn_(primary_vc, primary)
    split.setViewController_forColumn_(secondary_vc, secondary)

    #split.viewControllers = [primary, secondary,]


if __name__ == '__main__':
  from rbedge import present_viewController

  vc = ViewController.new()

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)


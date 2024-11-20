'''
  note:
    [Split View Controllers Done Right in iOS 14 - BiTE Interactive](https://www.biteinteractive.com/split-view-controllers-done-right-in-ios-14/)
'''

from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, SEL

from rbedge.rootNavigationController import RootNavigationController
from rbedge.objcMainThread import onMainThread
from rbedge.enumerations import (
  UIViewAutoresizing,
  UIRectEdge,
  UIBarButtonSystemItem,
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

# --- UINavigationController
UINavigationController = ObjCClass('UINavigationController')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')


class PrimaryViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    # --- Navigation
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title
    #self.navigationItem.title = 'title'
    #self.title = 'p'

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
    #pdbr.state(self,1)

    # --- Layout
    self.label.translatesAutoresizingMaskIntoConstraints = False

    NSLayoutConstraint.activateConstraints_([
      self.label.centerXAnchor.constraintEqualToAnchor_(
        self.view.centerXAnchor),
      self.label.centerYAnchor.constraintEqualToAnchor_(
        self.view.centerYAnchor),
    ])


class ViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    title = NSStringFromClass(__class__)

    self.navigationItem.title = title

    # --- View
    split = UISplitViewController.alloc().initWithStyle_(
      UISplitViewControllerStyle.doubleColumn)

    self.addChildViewController_(split)
    self.view.addSubview_(split.view)

    split.view.frame = self.view.bounds
    split.view.autoresizingMask = UIViewAutoresizing.flexibleHeight | UIViewAutoresizing.flexibleWidth

    split.didMoveToParentViewController_(self)

    primary = PrimaryViewController.new()
    #print(dir(primary))
    #print(primary.__class__)
    #pdbr.state(primary,1)
    #print(primary.CalClassName)
    #primary.title = f'{primary.class}'
    primary.title = 'hPrimaryViewController'

    split.setViewController_forColumn_(primary,
                                       UISplitViewControllerColumn.primary)

    secondary = SecondaryViewController.new()
    split.setViewController_forColumn_(secondary,
                                       UISplitViewControllerColumn.secondary)

    #pdbr.state(split)


if __name__ == '__main__':
  from rbedge import present_viewController

  vc = ViewController.new()

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)


'''
  note:
    [How to create UISplitViewController programmatically | by Anurag Ajwani | Medium](https://anuragajwani.medium.com/how-to-create-uisplitviewcontroller-programmatically-b07b15c01ae6)
    - Navigation の取り回し
    - `back` ではなく、title
      - 生成後、設定
'''

from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, SEL

from rbedge.rootNavigationController import RootNavigationController
from rbedge.objcMainThread import onMainThread
from rbedge.enumerations import (
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


class NavigationController(UINavigationController,
                           protocols=[
                             UINavigationControllerDelegate,
                           ]):

  @objc_method
  def viewDidLoad(self):
    appearance = UINavigationBarAppearance.new()
    appearance.configureWithDefaultBackground()

    navigationBar = self.navigationBar
    navigationBar.standardAppearance = appearance
    navigationBar.scrollEdgeAppearance = appearance
    navigationBar.compactAppearance = appearance
    navigationBar.compactScrollEdgeAppearance = appearance

    self.delegate = self

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated: bool):
    extendedLayout = UIRectEdge.none
    viewController.setEdgesForExtendedLayout_(extendedLayout)

    barButtonSystemItem = UIBarButtonSystemItem.done
    doneButton = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(barButtonSystemItem,
                                                 navigationController,
                                                 SEL('doneButtonTapped:'))
    visibleViewController = navigationController.visibleViewController

    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = doneButton


class PrimaryViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    # --- Navigation
    title = NSStringFromClass(__class__)
    #self.navigationItem.title = title
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
    self.navigationItem.title = title

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


class SplitViewController(UISplitViewController,
                          protocols=[
                            UISplitViewControllerDelegate,
                          ]):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.delegate = self
    # --- Navigation
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    # --- View
    self.view.backgroundColor = UIColor.systemIndigoColor()

  @objc_method
  def splitViewController_topColumnForCollapsingToProposedTopColumn_(
      self, svc, proposedTopColumn: int):
    #print('topColumnForCollapsingToProposedTopColumn')
    #pdbr.state(svc.viewControllers[0])
    #pdbr.state(svc.navigationItem)
    return UISplitViewControllerColumn.secondary

  @objc_method
  def splitViewController_displayModeForExpandingToProposedDisplayMode_(
      self, svc, proposedDisplayMode: int):

    if (navController :=
        svc.viewControllers[0]).isMemberOfClass_(UINavigationController):
      navController.popToRootViewControllerAnimated_(False)

    return UISplitViewControllerDisplayMode.automatic


@onMainThread
def present_splitViewController():
  sharedApplication = ObjCClass('UIApplication').sharedApplication
  keyWindow = sharedApplication.keyWindow if sharedApplication.keyWindow else sharedApplication.windows[
    0]
  rootViewController = keyWindow.rootViewController

  while _presentedViewController := rootViewController.presentedViewController:
    rootViewController = _presentedViewController

  p_vc = PrimaryViewController.new()
  p_vc.title = 'hoge'
  s_vc = SecondaryViewController.new()
  nav_vc = NavigationController.alloc().initWithRootViewController_(p_vc)

  splt_vc = SplitViewController.alloc().initWithStyle_(
    UISplitViewControllerStyle.doubleColumn)

  splt_vc.viewControllers = [
    #nav_vc,
    p_vc,
    s_vc,
  ]

  presentViewController = splt_vc
  #presentViewController = NavigationController.alloc().initWithRootViewController_(splt_vc)

  style = UIModalPresentationStyle.fullScreen
  style = UIModalPresentationStyle.pageSheet

  presentViewController.setModalPresentationStyle_(style)

  rootViewController.presentViewController_animated_completion_(
    presentViewController, True, None)


if __name__ == '__main__':
  '''
  splt_vc = SplitViewController.alloc().initWithStyle_(
    UISplitViewControllerStyle.doubleColumn)
  p_vc = PrimaryViewController.new()

  style = UIModalPresentationStyle.fullScreen
  style = UIModalPresentationStyle.pageSheet
  present_splitViewController(p_vc, style, NavigationController)
  '''
  present_splitViewController()


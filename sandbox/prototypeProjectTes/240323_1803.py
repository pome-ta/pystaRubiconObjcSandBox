from pyrubicon.objc import ObjCClass, ObjCProtocol, objc_method
from pyrubicon.objc import Block
from pyrubicon.objc.runtime import SEL, send_super

from dispatchSync import dispatch_sync

import pdbr

UINavigationController = ObjCClass('UINavigationController')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')
UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')


class TopViewController(UIViewController, auto_rename=True):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.view.backgroundColor = UIColor.systemDarkRedColor()


class WrapNavigationController(UINavigationController,
                               protocols=[UINavigationControllerDelegate],
                               auto_rename=True):

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated):
    appearance = UINavigationBarAppearance.alloc()
    appearance.configureWithDefaultBackground()

    navigationBar = navigationController.navigationBar
    navigationBar.standardAppearance = appearance
    navigationBar.scrollEdgeAppearance = appearance
    navigationBar.compactAppearance = appearance
    navigationBar.compactScrollEdgeAppearance = appearance

    viewController.setEdgesForExtendedLayout_(0)

    done_btn = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, navigationController,
                                                 SEL('doneButtonTapped:'))
    visibleViewController = navigationController.visibleViewController

    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = done_btn


def main():
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  root_vc = window.rootViewController

  while root_vc.presentedViewController:
    root_vc = root_vc.presentedViewController

  vc = TopViewController.new()

  @Block
  def processing() -> None:
    nv = WrapNavigationController.alloc().initWithRootViewController_(vc)
    nv.delegate = nv
    nv.setModalPresentationStyle_(0)

    root_vc.presentViewController_animated_completion_(nv, True, None)

  dispatch_sync(processing)


if __name__ == "__main__":
  main()


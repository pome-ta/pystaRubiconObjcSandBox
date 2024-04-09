from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method
from pyrubicon.objc.runtime import SEL, send_super

from mainThread import onMainThread
from objc_util import on_main_thread
import pdbr

ObjCClass.auto_rename = True
ObjCProtocol.auto_rename = True

# --- UINavigationController
UINavigationController = ObjCClass('UINavigationController')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

# --- UIViewController
UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
pageSheet = 1  # xxx: あとでちゃんと定義する


# --- NavigationController
class RootNavigationController(UINavigationController,
                               protocols=[UINavigationControllerDelegate]):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    print('--- viewDidLoad\t -> NavigationController')
    self.delegate = self

  @objc_method
  def viewDidAppear_(self, animated: bool):
    # xxx: 引数不要?
    send_super(__class__, self, 'viewDidAppear:')
    print('--- viewDidAppear:\t -> NavigationController')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewWillDisappear:')
    print('--- viewWillDisappear:\t -> NavigationController')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewDidDisappear:')
    print('--- viewDidDisappear:\t -> NavigationController')

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated):
    print('--- :willShowViewController:animated:\t -> NavigationController')
    appearance = UINavigationBarAppearance.new()
    appearance.configureWithDefaultBackground()

    navigationBar = navigationController.navigationBar
    navigationBar.standardAppearance = appearance
    navigationBar.scrollEdgeAppearance = appearance
    navigationBar.compactAppearance = appearance
    navigationBar.compactScrollEdgeAppearance = appearance

    viewController.setEdgesForExtendedLayout_(0)


# --- ViewController
class FirstViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    print('--- ViewController-> viewDidLoad')
    self.view.backgroundColor = UIColor.systemBlueColor()
    self.navigationItem.title = str(__class__)
    #pdbr.state(self.navigationItem)

  @objc_method
  def viewDidAppear_(self, animated: bool):
    # xxx: 引数不要？
    send_super(__class__, self, 'viewDidAppear:')
    print('--- ViewController-> viewDidAppear:')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewWillDisappear:')
    print('--- ViewController-> viewWillDisappear:')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewDidDisappear:')
    print('--- ViewController-> viewDidDisappear:')


@onMainThread
def present_viewController(myVC: UIViewController):
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  rootVC = window.rootViewController

  while _presentedVC := rootVC.presentedViewController:
    rootVC = _presentedVC

  myNC = RootNavigationController.alloc().initWithRootViewController_(myVC)

  presentVC = myNC
  presentVC.setModalPresentationStyle_(pageSheet)

  rootVC.presentViewController_animated_completion_(presentVC, True, None)


if __name__ == "__main__":
  vc = FirstViewController.new()
  present_viewController(vc)


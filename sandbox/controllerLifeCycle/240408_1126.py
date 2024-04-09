from pyrubicon.objc.api import ObjCClass, objc_method
from pyrubicon.objc.runtime import send_super

from mainThread import onMainThread
from objc_util import on_main_thread
import pdbr

ObjCClass.auto_rename = True

# --- UIViewController
UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
pageSheet = 1  # xxx: あとでちゃんと定義する


class FirstViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.view.backgroundColor = UIColor.systemBlueColor()


@onMainThread
def present_viewController(myVC: UIViewController):
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  rootVC = window.rootViewController

  while _presentedVC := rootVC.presentedViewController:
    rootVC = _presentedVC

  presentVC = myVC
  presentVC.setModalPresentationStyle_(pageSheet)

  rootVC.presentViewController_animated_completion_(presentVC, True, None)


if __name__ == "__main__":
  vc  = FirstViewController.new()
  present_viewController(vc)


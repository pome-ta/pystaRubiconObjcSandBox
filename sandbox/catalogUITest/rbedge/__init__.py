 __version__ = 0.0
from pyrubicon.objc.api import ObjCInstance, ObjCClass, ObjCProtocol, objc_method
from pyrubicon.objc.runtime import SEL, send_super, Foundation, Class

from .rootNavigationController import RootNavigationController
from .mainThread import onMainThread
 
 
@onMainThread
def present_viewController(myVC: UIViewController):
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  rootVC = window.rootViewController

  while _presentedVC := rootVC.presentedViewController:
    rootVC = _presentedVC

  myNC = RootNavigationController.alloc().initWithRootViewController_(myVC)

  presentVC = myNC
  '''
  UIModalPresentationFullScreen = 0
  UIModalPresentationPageSheet = 1
  '''
  presentVC.setModalPresentationStyle_(0)

  rootVC.presentViewController_animated_completion_(presentVC, True, None)



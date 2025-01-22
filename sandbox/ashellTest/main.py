from pyrubicon.objc.api import ObjCClass
import pdbr

UIApplication = ObjCClass('UIApplication')

if __name__ == '__main__':
  app = UIApplication.sharedApplication
  window = app.windows.firstObject()
  rootVC = window.rootViewController
  while _presentedVC := rootVC.presentedViewController:
    rootVC = _presentedVC
  pdbr.state(rootVC)


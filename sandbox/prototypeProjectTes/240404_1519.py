from pyrubicon.objc import objc_method, ObjCClass, send_super,ObjCProtocol,SEL

ObjCClass.auto_rename = True

NSOperation = ObjCClass("NSOperation")
NSOperationQueue = ObjCClass("NSOperationQueue")
UIApplication = ObjCClass('UIApplication')
UIColor = ObjCClass('UIColor')
UIViewController = ObjCClass('UIViewController')

UINavigationController = ObjCClass('UINavigationController')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

class WrapNavigationController(UINavigationController,
                               protocols=[UINavigationControllerDelegate]):

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)
    #loop.stop()

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



class MyViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, "viewDidLoad")
    self.view.backgroundColor = UIColor.blueColor
    print("Viewが読み込まれました")


class MainOperation(NSOperation):

  @objc_method
  def main(self):
    send_super(__class__, self, "main")
    app = UIApplication.sharedApplication
    rootVC = app.keyWindow.rootViewController
    while childVC := rootVC.presentedViewController:
      rootVC = childVC
    
    vc = MyViewController.new().autorelease()
    nv = WrapNavigationController.alloc().initWithRootViewController_(vc)
    nv.delegate = nv
    nv.setModalPresentationStyle_(1)

    rootVC.presentViewController_animated_completion_(nv, True, None)
    
    #rootVC.presentViewController(mainVC, animated=True, completion=None)


if __name__ == "__main__":
  operation = MainOperation.new()
  queue = NSOperationQueue.mainQueue
  queue.addOperation(operation)
  queue.waitUntilAllOperationsAreFinished()


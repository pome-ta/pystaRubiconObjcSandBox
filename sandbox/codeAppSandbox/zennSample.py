from pyrubicon.objc import objc_method, ObjCClass, send_super

ObjCClass.auto_rename = True

NSOperation = ObjCClass("NSOperation")
NSOperationQueue = ObjCClass("NSOperationQueue")
UIApplication = ObjCClass('UIApplication')
UIColor = ObjCClass('UIColor')
UIViewController = ObjCClass('UIViewController')

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
        mainVC = MyViewController.new().autorelease()
        rootVC.presentViewController(mainVC, animated=True, completion=None)

if __name__ == "__main__":
    operation = MainOperation.new()
    queue = NSOperationQueue.mainQueue
    queue.addOperation(operation)
    queue.waitUntilAllOperationsAreFinished()

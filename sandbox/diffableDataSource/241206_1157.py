'''
  note:
    - [モダンなUICollectionViewでシンプルなリストレイアウト その1 〜 概要](https://zenn.dev/samekard_dev/articles/43991e9321b6c9)
    - [PythonistaでRubicon-ObjCを使う](https://zenn.dev/qqfunc/articles/b39a657990c9f0)
'''

import ctypes

from pyrubicon.objc import ObjCClass, ObjCInstance
from pyrubicon.objc import objc_method, send_super

from rbedge import pdbr

ObjCClass.auto_rename = True

NSOperation = ObjCClass('NSOperation')
NSOperationQueue = ObjCClass('NSOperationQueue')
UIApplication = ObjCClass('UIApplication')
UIColor = ObjCClass('UIColor')
UIViewController = ObjCClass('UIViewController')


class ViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.view.backgroundColor = UIColor.blueColor
    #print('Viewが読み込まれました')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewDidAppear_')

  @objc_method
  def createLayout(self) -> ObjCInstance:
    pass

  @objc_method
  def configureHierarchy(self):
    pass

  @objc_method
  def configureDataSource(self):
    pass


class MainOperation(NSOperation):

  @objc_method
  def main(self):
    send_super(__class__, self, 'main')
    app = UIApplication.sharedApplication
    rootVC = app.keyWindow.rootViewController
    while childVC := rootVC.presentedViewController:
      rootVC = childVC
    mainVC = ViewController.new().autorelease()
    rootVC.presentViewController(mainVC, animated=True, completion=None)


if __name__ == "__main__":
  operation = MainOperation.new()
  queue = NSOperationQueue.mainQueue
  queue.addOperation(operation)
  queue.waitUntilAllOperationsAreFinished()


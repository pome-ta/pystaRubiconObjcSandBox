from pyrubicon.objc.api import ObjCClass, objc_method
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import SEL, send_super, objc_id

from rbedge.functions import NSStringFromClass

UIViewController = ObjCClass('UIViewController')


class ViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?

    title = NSStringFromClass(__class__)
    self.navigationItem.title = title


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController

  main_vc = ViewController.new()
  #style = UIModalPresentationStyle.pageSheet
  style = UIModalPresentationStyle.fullScreen
  present_viewController(main_vc, style)


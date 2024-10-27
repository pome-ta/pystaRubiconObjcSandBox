"""
todo:
  Pythonista3 以外の環境でもUIView を使える状態に
"""

from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super

from rbedge.functions import NSStringFromClass

UIViewController = ObjCClass('UIViewController')
UIView = ObjCClass('UIView')


class MainViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    # --- Navigation
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = MainViewController.new()
  #style = UIModalPresentationStyle.fullScreen
  style = UIModalPresentationStyle.pageSheet
  present_viewController(main_vc, style)


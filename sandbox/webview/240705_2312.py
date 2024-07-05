from pyrubicon.objc.api import ObjCClass, ObjCInstance, ObjCProtocol, objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import NSInteger

from rbedge.enumerations import (
  UICollectionLayoutListAppearance,
  UICollectionLayoutListHeaderMode,
  UIViewAutoresizing,
)
from rbedge.functions import NSStringFromClass

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- WKWebView
WKWebView = ObjCClass('WKWebView')
WKWebViewConfiguration=ObjCClass('WKWebViewConfiguration')

WKUIDelegate = ObjCProtocol('WKUIDelegate')


class WebView(UIViewController, protocols=[WKUIDelegate]):
  webView: WKWebView = objc_property()

  @objc_method
  def loadView(self):
    pass
    
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    pdbr.state(WKWebViewConfiguration)


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = WebView.new()

  present_viewController(main_vc)


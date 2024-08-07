from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method, objc_property
from pyrubicon.objc.runtime import send_super, load_library
from pyrubicon.objc.types import CGRect

from rbedge.functions import NSStringFromClass

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
CoreGraphics = load_library('CoreGraphics')
CGRectZero = CGRect.in_dll(CoreGraphics, 'CGRectZero')

NSURL = ObjCClass('NSURL')
NSURLRequest = ObjCClass('NSURLRequest')
# --- WKWebView
WKWebView = ObjCClass('WKWebView')
WKWebViewConfiguration = ObjCClass('WKWebViewConfiguration')

WKUIDelegate = ObjCProtocol('WKUIDelegate')
WKNavigationDelegate = ObjCProtocol('WKNavigationDelegate')


class WebView(UIViewController,
              protocols=[
                WKUIDelegate,
                WKNavigationDelegate,
              ]):

  webView: WKWebView = objc_property()

  @objc_method
  def loadView(self):
    print('l')
    webConfiguration = WKWebViewConfiguration.new()
    self.webView = WKWebView.alloc().initWithFrame_configuration_(
      CGRectZero, webConfiguration)
    #self.webView.uiDelegate = self
    #self.webView.navigationDelegate = self
    self.view = self.webView

  @objc_method
  def viewDidLoad(self):
    print('d')
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    self.view.backgroundColor = UIColor.systemDarkRedColor()

    myURL = NSURL.URLWithString_('https://www.apple.com')
    myRequest = NSURLRequest.requestWithURL_(myURL)
    self.webView.loadRequest_(myRequest)

  '''
  @objc_method
  def webView_didFinishNavigation_(self, webView, navigation):
    title = webView.title
    self.navigationItem.title = str(title)
  '''


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = WebView.new()

  present_viewController(main_vc)


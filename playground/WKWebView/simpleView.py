_TOP_DIR_NAME = 'pystaRubiconObjcSandBox'
_MODULES_DIR_NAME = 'modules'

# todo: `./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME}` にあるpackage のimport 準備
if __name__ == '__main__' and not __file__[:__file__.rfind('/')].endswith(
    _TOP_DIR_NAME):
  import pathlib
  import sys
  __parents = pathlib.Path(__file__).resolve().parents
  for __dir_path in __parents:
    if __dir_path.name == _TOP_DIR_NAME and (__modules_path := __dir_path /
                                             _MODULES_DIR_NAME).exists():
      sys.path.insert(0, str(__modules_path))
      break
  else:
    import warnings
    with warnings.catch_warnings():
      warnings.simplefilter('always', ImportWarning)
      __warning_message = f'./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME} not found in parent directories'
      warnings.warn(__warning_message, ImportWarning)

import ctypes
from pathlib import Path

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super

from objc_frameworks.CoreGraphics import CGRectZero
from objc_frameworks.Foundation import NSURLRequestCachePolicy
from objc_frameworks.UIKit import (
  UIViewAutoresizing,
  UIControlEvents,
  UIBarButtonSystemItem,
  UIBarButtonItemStyle,
)

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')

WKWebView = ObjCClass('WKWebView')
WKWebViewConfiguration = ObjCClass('WKWebViewConfiguration')
WKWebsiteDataStore = ObjCClass('WKWebsiteDataStore')
NSURL = ObjCClass('NSURL')

UIColor = ObjCClass('UIColor')


class WebViewController(UIViewController):

  webView: WKWebView = objc_property()
  indexPath: Path = objc_property(object)

  @objc_method
  def initWithIndexPath_(self, indexPath: object):
    send_super(__class__, self, 'init')

    if not (indexPath.exists()):
      raise FileNotFoundError(f'{indexPath}')

    self.indexPath = indexPath
    return self

  @objc_method
  def makeWeblView(self) -> ObjCInstance:
    websiteDataStore = WKWebsiteDataStore.nonPersistentDataStore()

    webConfiguration = WKWebViewConfiguration.new()
    webConfiguration.websiteDataStore = websiteDataStore
    webConfiguration.preferences.setValue_forKey_(
      True, 'allowFileAccessFromFileURLs')

    webView = WKWebView.alloc().initWithFrame_configuration_(
      CGRectZero, webConfiguration)

    return webView

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'	 - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    self.webView = self.makeWeblView()

  @objc_method
  def viewDidLoad(self):
    from objc_frameworks.Foundation import NSStringFromClass

    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__)

    # --- load
    _fileURLWithPath = NSURL.fileURLWithPath_isDirectory_
    _path = str(self.indexPath)
    _parent = str(self.indexPath.parent)
    loadFileURL = _fileURLWithPath(_path, False)
    allowingReadAccessToURL = _fileURLWithPath(_parent, True)

    self.webView.loadFileURL(
      loadFileURL,
      allowingReadAccessToURL=allowingReadAccessToURL,
    )

    self.setupLayoutConstraint()

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    self.webView.reloadFromOrigin()

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'	{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  # --- private
  @objc_method
  def setupLayoutConstraint(self):
    NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

    self.view.addSubview_(self.webView)

    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    self.webView.translatesAutoresizingMaskIntoConstraints = False

    centerXAnchor = self.webView.centerXAnchor.constraintEqualToAnchor_(
      safeAreaLayoutGuide.centerXAnchor)
    centerYAnchor = self.webView.centerYAnchor.constraintEqualToAnchor_(
      safeAreaLayoutGuide.centerYAnchor)

    widthAnchor = self.webView.widthAnchor.constraintEqualToAnchor_multiplier_(
      safeAreaLayoutGuide.widthAnchor,
      0.96,
    )
    heightAnchor = self.webView.heightAnchor.constraintEqualToAnchor_multiplier_(
      safeAreaLayoutGuide.heightAnchor,
      0.96,
    )

    NSLayoutConstraint.activateConstraints_([
      centerXAnchor,
      centerYAnchor,
      widthAnchor,
      heightAnchor,
    ])


if __name__ == '__main__':
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  index_path = Path('./docs/index.html')

  #main_vc = WebViewController.new()
  main_vc = WebViewController.alloc().initWithIndexPath_(index_path)

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()


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

from objc_frameworks.Foundation import NSStringFromClass
from objc_frameworks.Foundation import NSURLRequestCachePolicy
from objc_frameworks.UIKit import UIViewAutoresizing, UIControlEvents

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')

UIView = ObjCClass('UIView')
WKWebView = ObjCClass('WKWebView')

UIColor = ObjCClass('UIColor')

class WebView(UIView):
  
  wkWebView: WKWebView = objc_property()
  
  @objc_method
  def initWithIndexPath_(self, index_path: object):
    pass
  
  

class MainViewController(UIViewController):

  wkWebView: WKWebView = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'	 - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__)
    
    #self.view.backgroundColor = UIColor.secondarySystemBackgroundColor()
    
    wkWebView = WKWebView.new()
    print(self.view.bounds)
    

    self.wkWebView = wkWebView
    self.view.addSubview_(self.wkWebView)
    
    #self.setupLayoutConstraint()

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #self.wkWebView.autoresizingMask = UIViewAutoresizing.flexibleWidth | UIViewAutoresizing.flexibleHeight

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(self.wkWebView)
    print(self.view.bounds)

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

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

    self.view.addSubview_(self.wkWebView)

    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    self.wkWebView.translatesAutoresizingMaskIntoConstraints = False

    centerXAnchor = self.wkWebView.centerXAnchor.constraintEqualToAnchor_(
      safeAreaLayoutGuide.centerXAnchor)
    centerYAnchor = self.wkWebView.centerYAnchor.constraintEqualToAnchor_(
      safeAreaLayoutGuide.centerYAnchor)

    widthAnchor = self.wkWebView.widthAnchor.constraintEqualToAnchor_multiplier_(
      safeAreaLayoutGuide.widthAnchor,
      0.96,
    )
    heightAnchor = self.wkWebView.heightAnchor.constraintEqualToAnchor_multiplier_(
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

  main_vc = MainViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()


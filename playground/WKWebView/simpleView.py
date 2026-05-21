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

from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from pyrubicon.objc.api import ObjCInstance, NSObject
from pyrubicon.objc.api import objc_method, objc_property, at, py_from_ns, ns_from_py
from pyrubicon.objc.runtime import send_super, objc_id, SEL

from pyrubicon.objc.types import CGRect

from objc_frameworks.CoreGraphics import CGRectZero
from objc_frameworks.Foundation import NSURLRequestCachePolicy
from objc_frameworks.UIKit import (
  UIViewAutoresizing,
  UIBarButtonItemStyle,
  NSNotificationName,
  UIKeyboardAnimationDurationUserInfoKey,
  UIKeyboardFrameBeginUserInfoKey,
  UIKeyboardFrameEndUserInfoKey,
)

from rbedge.lifeCycle import loop
from rbedge import pdbr

UINavigationController = ObjCClass('UINavigationController')
UIViewController = ObjCClass('UIViewController')

WKWebView = ObjCClass('WKWebView')
WKWebViewConfiguration = ObjCClass('WKWebViewConfiguration')
WKWebsiteDataStore = ObjCClass('WKWebsiteDataStore')
NSURL = ObjCClass('NSURL')

WKNavigationDelegate = ObjCProtocol('WKNavigationDelegate')
WKUIDelegate = ObjCProtocol('WKUIDelegate')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')

UIBarButtonItem = ObjCClass('UIBarButtonItem')
UIImage = ObjCClass('UIImage')

NSNotificationCenter = ObjCClass('NSNotificationCenter')

UIScreen = ObjCClass('UIScreen')


class NavigationController(UINavigationController):

  @objc_method
  def initWithRootViewController_(self, rootViewController):
    send_super(__class__,
               self,
               'initWithRootViewController:',
               rootViewController,
               argtypes=[
                 objc_id,
               ])
    return self

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'- {NSStringFromClass(__class__)}: dealloc')
    loop.stop()

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    #print(f'{NSStringFromClass(__class__)}: viewDidLoad')

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'{NSStringFromClass(__class__)}: viewDidAppear_')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'{NSStringFromClass(__class__)}: viewWillDisappear_')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'{NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  @objc_method
  def doneButtonTapped_(self, sender):
    self.dismissViewControllerAnimated_completion_(True, None)


class WebDelegate(
    NSObject,
    protocols=[
      WKNavigationDelegate,
      #WKUIDelegate,
    ]):

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    return self

  # --- WKUIDelegate
  # --- WKNavigationDelegate
  @objc_method
  def webView_didCommitNavigation_(self, webView, navigation):
    # 遷移開始時
    pass

  @objc_method
  def webView_didFailNavigation_withError_(self, webView, navigation, error):
    # 遷移中にエラーが発生した時
    # xxx: 未確認
    print('didFailNavigation_withError')
    print(error)

  @objc_method
  def webView_didFailProvisionalNavigation_withError_(self, webView,
                                                      navigation, error):
    # ページ読み込み時にエラーが発生した時
    print('didFailProvisionalNavigation_withError')
    print(error)

  @objc_method
  def webView_didFinishNavigation_(self, webView, navigation):
    # ページ読み込みが完了した時
    title = webView.title

  @objc_method
  def webView_didReceiveServerRedirectForProvisionalNavigation_(
      self, webView, navigation):
    # リダイレクトされた時
    # xxx: 未確認
    print('didReceiveServerRedirectForProvisionalNavigation')

  @objc_method
  def webView_didStartProvisionalNavigation_(self, webView, navigation):
    # ページ読み込みが開始された時
    pass


class WebViewController(UIViewController):

  indexPath: Path = objc_property(object)
  webView: WKWebView = objc_property()
  webDelegate: WebDelegate = objc_property()

  isKeyboardVisible: bool = objc_property(object)

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

    webDelegate = WebDelegate.new()
    webView = self.makeWeblView()
    webView.navigationDelegate = webDelegate
    #webView.uiDelegate = webDelegate  # xxx: ?

    self.webView = webView
    self.webDelegate = webDelegate
    self.isKeyboardVisible = False

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

    closeImage = UIImage.systemImageNamed_('xmark')
    closeButtonItem = UIBarButtonItem.alloc().initWithImage(
      closeImage,
      style=UIBarButtonItemStyle.plain,
      target=self.navigationController,
      action=SEL('doneButtonTapped:'),
    )

    self.navigationItem.setRightBarButtonItem_animated_(closeButtonItem, True)

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

    notificationCenter = NSNotificationCenter.defaultCenter

    notificationCenter.addObserver(
      self,
      selector=SEL('keyboardWillChangeFrame:'),
      name=NSNotificationName.keyboardWillChangeFrameNotification,
      object=None,
    )

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
    notificationCenter = NSNotificationCenter.defaultCenter
    notificationCenter.removeObserver(
      self,
      name=NSNotificationName.keyboardWillChangeFrameNotification,
      object=None,
    )

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'	{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  @objc_method
  def keyboardWillChangeFrame_(self, notification):
    #print('keyboardWillChangeFrame')
    duration = notification.userInfo[UIKeyboardAnimationDurationUserInfoKey]

    if duration.doubleValue == 0:
      return

    self.handleKeyboardFrameChange_(notification)

  @objc_method
  def handleKeyboardFrameChange_(self, notification):
    #print('handleKeyboardFrameChange')

    end = notification.userInfo[UIKeyboardFrameEndUserInfoKey]

    if not ((window := self.view.window())):
      return

    keyboardFrameInWindow = window.convertRect_fromWindow_(
      end.CGRectValue, None)

    #pdbr.state(self.view.window())
    #print(window)
    print(keyboardFrameInWindow)

    screenHeight = UIScreen.mainScreen.bounds.size.height

    nowVisible = end.CGRectValue.origin.y < screenHeight

    if nowVisible and not self.isKeyboardVisible:
      self.isKeyboardVisible = True
      print('show')
    if not nowVisible and self.isKeyboardVisible:
      self.isKeyboardVisible = False
      print('hide')

  @objc_method
  def keyboardWillShow_(self, notification):
    #print('s: keyboardWillShow')
    print(notification)

  @objc_method
  def keyboardWillHide_(self, notification):
    #print('h: keyboardWillHide')
    pass

  # --- private
  @objc_method
  def setupLayoutConstraint(self):
    NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

    self.view.addSubview_(self.webView)

    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide
    #safeAreaLayoutGuide = self.view

    self.webView.translatesAutoresizingMaskIntoConstraints = False

    centerXAnchor = self.webView.centerXAnchor.constraintEqualToAnchor_(
      safeAreaLayoutGuide.centerXAnchor)
    centerYAnchor = self.webView.centerYAnchor.constraintEqualToAnchor_(
      safeAreaLayoutGuide.centerYAnchor)

    widthAnchor = self.webView.widthAnchor.constraintEqualToAnchor_multiplier_(
      safeAreaLayoutGuide.widthAnchor,
      1,
    )
    heightAnchor = self.webView.heightAnchor.constraintEqualToAnchor_multiplier_(
      safeAreaLayoutGuide.heightAnchor,
      1,
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

  ROOT_PATH = Path(__file__).parents[0]

  index_path = ROOT_PATH / 'docs/index.html'
  #main_vc = WebViewController.new()
  main_vc = WebViewController.alloc().initWithIndexPath_(index_path)

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present(NavigationController)


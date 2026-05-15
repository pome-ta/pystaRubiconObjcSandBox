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

from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, SEL

from objc_frameworks.UIKit import UIViewAutoresizing
from objc_frameworks.UIKit import UIBarButtonSystemItem

from rbedge.lifeCycle import loop
from rbedge import pdbr

UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')

UINavigationController = ObjCClass('UINavigationController')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIToolbarAppearance = ObjCClass('UIToolbarAppearance')
UIViewController = ObjCClass('UIViewController')

UIView = ObjCClass('UIView')
UIColor = ObjCClass('UIColor')
UIBarButtonItem = ObjCClass('UIBarButtonItem')


class NavigationController(
    UINavigationController,
    protocols=[
      UINavigationControllerDelegate,
    ],
):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'- {NSStringFromClass(__class__)}: dealloc')
    loop.stop()

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    #print(f'{NSStringFromClass(__class__)}: loadView')
    
    navigationBarAppearance = UINavigationBarAppearance.new()
    navigationBarAppearance.configureWithDefaultBackground()

    self.navigationBar.standardAppearance = navigationBarAppearance
    self.navigationBar.scrollEdgeAppearance = navigationBarAppearance
    self.navigationBar.compactAppearance = navigationBarAppearance
    self.navigationBar.compactScrollEdgeAppearance = navigationBarAppearance
    
    
    '''
    toolbarAppearance = UIToolbarAppearance.new()
    toolbarAppearance.configureWithDefaultBackground()

    self.toolbar.standardAppearance = toolbarAppearance
    self.toolbar.scrollEdgeAppearance = toolbarAppearance
    self.toolbar.compactAppearance = toolbarAppearance
    self.toolbar.compactScrollEdgeAppearance = toolbarAppearance
    '''
    
    #
    #self.setToolbarHidden_animated_(False, True)
    #self.setNavigationBarHidden_animated_(True, True)
    #self.setToolbarHidden_(False)
    #pdbr.state(self)
    #print(self.toolbarHidden)

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    #print(f'{NSStringFromClass(__class__)}: viewDidLoad')
    self.delegate = self

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
    #self.setToolbarHidden_(True)

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
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated: bool):
    # xxx: layout 範囲の制限
    #extendedLayout = UIRectEdge.none
    #viewController.setEdgesForExtendedLayout_(extendedLayout)

    closeButtonItem = UIBarButtonItem.alloc().initWithBarButtonSystemItem(
      UIBarButtonSystemItem.close,
      target=navigationController,
      action=SEL('doneButtonTapped:'),
    )

    # todo: view 遷移でのButton 重複を判別

    visibleViewController = navigationController.visibleViewController

    #pdbr.state(visibleViewController)

    navigationItem = visibleViewController.navigationItem
    navigationItem.leftBarButtonItem = closeButtonItem

    #navigationController.setToolbarItems_animated_([closeButtonItem] ,True)

  @objc_method
  def doneButtonTapped_(self, sender):
    self.dismissViewControllerAnimated_completion_(True, None)


class MainViewController(ObjCClass('UIViewController')):

  subView: UIView = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'\t - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')

  @objc_method
  def viewDidLoad(self):
    from objc_frameworks.Foundation import NSStringFromClass
    send_super(__class__, self, 'viewDidLoad')
    #self.navigationItem.title = NSStringFromClass(__class__)
    self.view.backgroundColor = UIColor.systemDarkPinkColor()

    subView = UIView.new()
    subView.autoresizingMask = UIViewAutoresizing.flexibleWidth | UIViewAutoresizing.flexibleHeight

    subView.backgroundColor = UIColor.systemDarkTealColor()

    self.subView = subView
    #pdbr.state(self)
    closeButtonItem = UIBarButtonItem.alloc().initWithBarButtonSystemItem(
      UIBarButtonSystemItem.close,
      target=self.navigationController,
      action=SEL('doneButtonTapped:'),
    )
    self.toolbarItems = [closeButtonItem]

    self.setupLayoutConstraint()

  @objc_method
  def doneButtonTapped_(self, sender):
    self.navigationController.dismissViewControllerAnimated(
      True,
      completion=None,
    )

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    self.navigationController.setToolbarHidden_animated_(False, animated)

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
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  # --- private
  @objc_method
  def setupLayoutConstraint(self):
    NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

    self.view.addSubview_(self.subView)

    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide
    #safeAreaLayoutGuide = self.view

    self.subView.translatesAutoresizingMaskIntoConstraints = False

    centerXAnchor = self.subView.centerXAnchor.constraintEqualToAnchor_(
      safeAreaLayoutGuide.centerXAnchor)
    centerYAnchor = self.subView.centerYAnchor.constraintEqualToAnchor_(
      safeAreaLayoutGuide.centerYAnchor)

    widthAnchor = self.subView.widthAnchor.constraintEqualToAnchor_multiplier_(
      safeAreaLayoutGuide.widthAnchor,
      0.88,
    )
    heightAnchor = self.subView.heightAnchor.constraintEqualToAnchor_multiplier_(
      safeAreaLayoutGuide.heightAnchor,
      0.88,
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
  app.present(NavigationController)


import ctypes

from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, SEL

from .lifeCycle import loop
from .enumerations import UIBarButtonSystemItem

from .functions import NSStringFromClass

UINavigationController = ObjCClass('UINavigationController')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')


class RootNavigationController(UINavigationController):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'- {NSStringFromClass(__class__)}: dealloc')
    loop.stop()
    #print('--- stop')

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    #print(f'{NSStringFromClass(__class__)}: loadView')
    navigationBarAppearance = UINavigationBarAppearance.new()
    navigationBarAppearance.configureWithDefaultBackground()
    #navigationBarAppearance.configureWithOpaqueBackground()
    #navigationBarAppearance.configureWithTransparentBackground()

    '''
    navigationBar = self.navigationBar
    navigationBar.standardAppearance = navigationBarAppearance
    navigationBar.scrollEdgeAppearance = navigationBarAppearance
    navigationBar.compactAppearance = navigationBarAppearance
    navigationBar.compactScrollEdgeAppearance = navigationBarAppearance
    '''
    

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
  def closeButtonTapped_(self, sender):
    self.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated: bool):
    closeButtonItem = UIBarButtonItem.alloc().initWithBarButtonSystemItem(
      UIBarButtonSystemItem.close,
      target=navigationController,
      action=SEL('closeButtonTapped:'))

    visibleViewController = navigationController.visibleViewController
    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = closeButtonItem


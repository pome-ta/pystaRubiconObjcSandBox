import ctypes
from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import objc_id, send_super, SEL

import pdbr

ObjCClass.auto_rename = True

UIApplication = ObjCClass('UIApplication')
UINavigationController = ObjCClass('UINavigationController')
UIBarButtonItem = ObjCClass('UIBarButtonItem')
UIViewController = ObjCClass('UIViewController')


class RootNavigationController(UINavigationController):

  @objc_method
  def viewDidLoad(self):
    self.delegate = self

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated: bool):

    _UIBarButtonSystemItem_close = 24
    closeButtonItem = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(_UIBarButtonSystemItem_close,
                                                 navigationController,
                                                 SEL('doneButtonTapped:'))
    # todo: view 遷移でのButton 重複を判別
    closeButtonItem.setTag_(_UIBarButtonSystemItem_close)

    visibleViewController = navigationController.visibleViewController

    navigationItem = visibleViewController.navigationItem
    if (rightBarButtonItems := navigationItem.rightBarButtonItems):
      # todo: `UIViewController` で、`rightBarButtonItem` が存在していた場合、`closeButtonItem` を右端に設置
      setRightBarButtonItems = [
        closeButtonItem,
        *[
          item for item in rightBarButtonItems
          if item.tag != _UIBarButtonSystemItem_close
        ],
      ]
      navigationItem.setRightBarButtonItems_animated_(setRightBarButtonItems,
                                                      True)
    else:
      navigationItem.rightBarButtonItem = closeButtonItem


def present_viewController(viewController):
  app = UIApplication.sharedApplication
  window = app.windows.firstObject()
  rootViewController = window.rootViewController
  while _presentedVC := rootViewController.presentedViewController:
    rootViewController = _presentedVC
  presentViewController = RootNavigationController.alloc(
  ).initWithRootViewController_(viewController)
  presentViewController.setModalPresentationStyle_(1)
  rootViewController.presentViewController_animated_completion_(
    presentViewController, True, None)


class MainViewController(UIViewController):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print('\tdealloc')
    pass

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print('viewWillAppear')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print('viewDidAppear')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print('viewWillDisappear')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print('viewDidDisappear')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'{__class__}: didReceiveMemoryWarning')


if __name__ == '__main__':
  main_vc = MainViewController.new()
  present_viewController(main_vc)


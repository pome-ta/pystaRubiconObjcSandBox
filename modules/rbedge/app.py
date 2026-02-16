from typing import Union

from pyrubicon.objc.api import ObjCClass

from objc_frameworks.UIKit import UISceneActivationState, UIModalPresentationStyle

from .lifeCycle import loop
from .objcMainThread import onMainThread
from .rootNavigationController import RootNavigationController

from rbedge import pdbr

UIApplication = ObjCClass('UIApplication')
UIViewController = ObjCClass('UIViewController')  # todo: アノテーション用


class App:

  sharedApplication = UIApplication.sharedApplication
  #rootViewController = sharedApplication.connectedScenes.allObjects()[0].windows[0].rootViewController

  #print(rootViewController)
  '''
  __objectEnumerator = sharedApplication.connectedScenes.objectEnumerator()
  while (__windowScene := __objectEnumerator.nextObject()):
    if __windowScene.activationState == 0:
      break
  rootViewController = __windowScene.keyWindow.rootViewController
  '''

  def __init__(
    self,
    viewController: UIViewController,
    modalPresentationStyle: Union[UIModalPresentationStyle,
                                  int] = UIModalPresentationStyle.pageSheet):

    print('init')

    #@onMainThread

    #pdbr.state(self.rootViewController)

    self.viewController = viewController
    # xxx: style 指定を力技で確認
    _automatic = UIModalPresentationStyle.automatic  # -2
    _blurOverFullScreen = UIModalPresentationStyle.blurOverFullScreen  # 8
    _pageSheet = UIModalPresentationStyle.pageSheet  # 1

    self.modalPresentationStyle = modalPresentationStyle if isinstance(
      modalPresentationStyle, int
    ) and _automatic <= modalPresentationStyle <= _blurOverFullScreen else _pageSheet

    #self.set_rootViewController()

  '''
  def set_rootViewController(self) -> None:
    print('s: set_rootViewController')
    sharedApplication = UIApplication.sharedApplication
    __objectEnumerator = sharedApplication.connectedScenes.objectEnumerator()
    #pdbr.state(__objectEnumerator)
    while (__windowScene := __objectEnumerator.nextObject()):
      print(__windowScene)
      if __windowScene.activationState == 0:
        break
    rootViewController = __windowScene.keyWindow.rootViewController
    self.rootViewController = rootViewController
    print('e: set_rootViewController')
  '''

  def present(self) -> None:
    print('present')
    def get_rootViewController():
      self.rootViewController = self.sharedApplication.connectedScenes.allObjects(
      )[0].windows[0].rootViewController


    @onMainThread
    def present_viewController(viewController: UIViewController,
                               style: int) -> None:

      presentViewController = RootNavigationController.alloc(
      ).initWithRootViewController_(viewController)

      presentViewController.setModalPresentationStyle_(style)
      get_rootViewController()

      self.rootViewController.presentViewController_animated_completion_(
        presentViewController, True, None)

    present_viewController(self.viewController, self.modalPresentationStyle)
    self.main_loop()

  def main_loop(self) -> None:

    try:
      print('app s: run')
      loop.run_forever()
      print('app e: run')

    except Exception as e:
      print(f'Exception: {e}')
    finally:
      print('app s: close')
      loop.close()
      print('app e: close')


from pyrubicon.objc import (
  NSObject,
  ObjCClass,
  ObjCInstance,
  objc_method,
  objc_property,
)  # api
from pyrubicon.objc import (
  objc_id,
  send_super,
)  # runtime

from .lifeCycle import loop
from .enumerations import (
  UISceneActivationState,
  UIModalPresentationStyle,
)
from .objcMainThread import onMainThread
from .rootNavigationController import RootNavigationController
from .functions import NSStringFromClass

UIApplication = ObjCClass('UIApplication')


class App(NSObject):

  viewController = objc_property(ObjCInstance)
  navigationClass = objc_property(ObjCClass)
  sharedViewController = objc_property(ObjCInstance)

  @objc_method
  def dealloc(self) -> None:
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'- {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def configureWithViewController_navigationClass_(
    self,
    viewController: ObjCInstance,
    navigationClass: ObjCClass,
  ) -> ObjCInstance:
    self = ObjCInstance(send_super(
      __class__,
      self,
      'init',
      restype=objc_id,
    ))
    if self is None:
      return None

    self.viewController = viewController
    self.navigationClass = navigationClass

    sharedApplication = UIApplication.sharedApplication
    objectEnumerator = sharedApplication.connectedScenes.objectEnumerator()

    next(sharedScene for _scene in iter(objectEnumerator.nextObject, None)
         if (sharedScene := _scene).activationState == 0)

    sceneWindow = sharedScene.keyWindow if (
      _delegate := sharedScene.delegate) is None else _delegate.window

    self.sharedViewController = sceneWindow.rootViewController

    return self

  @objc_method
  def initWithViewController_(
    self,
    viewController: ObjCInstance,
  ) -> ObjCInstance:
    return self.configureWithViewController_navigationClass_(
      viewController,
      RootNavigationController,
    )

  @objc_method
  def initWithViewController_navigationClass_(
    self,
    viewController: ObjCInstance,
    navigationClass: ObjCClass,
  ) -> ObjCInstance:
    return self.configureWithViewController_navigationClass_(
      viewController,
      navigationClass,
    )

  @objc_method
  def presentWithStyle_(self, style: int) -> None:

    # xxx: style 指定を力技で確認
    _automatic = UIModalPresentationStyle.automatic  # -2
    _blurOverFullScreen = UIModalPresentationStyle.blurOverFullScreen  # 8
    _pageSheet = UIModalPresentationStyle.pageSheet  # 1

    modalPresentationStyle = style if isinstance(
      style, int
    ) and _automatic <= modalPresentationStyle <= _blurOverFullScreen else _pageSheet

    @onMainThread
    def _main_thread_present() -> None:

      presentController = self.navigationClass.alloc(
      ).initWithRootViewController_(self.viewController)
      presentController.setModalPresentationStyle_(modalPresentationStyle)

      self.sharedViewController.presentViewController(
        presentController,
        animated=True,
        completion=None,
      )

    _main_thread_present()
    #print('s: --- main_loop ---')
    loop.run_forever()


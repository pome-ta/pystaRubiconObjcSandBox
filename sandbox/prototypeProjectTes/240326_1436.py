from pyrubicon.objc.api import ObjCInstance, ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_property, objc_method
from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import Block
from pyrubicon.objc.runtime import SEL#, send_super

from dispatchSync import dispatch_sync

import pdbr


def present_ViewController(viewController_instance):
  vc = viewController_instance
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  root_vc = window.rootViewController

  while root_vc.presentedViewController:
    root_vc = root_vc.presentedViewController

  @Block
  def processing() -> None:
    nv = WrapNavigationController.alloc().initWithRootViewController_(vc)
    nv.delegate = nv
    nv.setModalPresentationStyle_(1)

    root_vc.presentViewController_animated_completion_(nv, True, None)

  dispatch_sync(processing)


UINavigationController = ObjCClass('UINavigationController')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')


class WrapNavigationController(UINavigationController,
                               protocols=[UINavigationControllerDelegate],
                               auto_rename=True):

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated):
    appearance = UINavigationBarAppearance.alloc()
    appearance.configureWithDefaultBackground()

    navigationBar = navigationController.navigationBar
    navigationBar.standardAppearance = appearance
    navigationBar.scrollEdgeAppearance = appearance
    navigationBar.compactAppearance = appearance
    navigationBar.compactScrollEdgeAppearance = appearance

    viewController.setEdgesForExtendedLayout_(0)

    done_btn = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, navigationController,
                                                 SEL('doneButtonTapped:'))
    visibleViewController = navigationController.visibleViewController

    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = done_btn


class TopViewController(UIViewController, auto_rename=True):
  generator = objc_property()

  @objc_method
  def viewDidLoad(self):
    #send_super(__class__, self, 'viewDidLoad')
    pass

    #self.generator = AudioEngeneWaveGenerator.alloc().initGenerator()
    #self.generator.start()

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    #self.generator.stop()
    pass


# --- AVAudioEngine

AVAudioEngine = ObjCClass('AVAudioEngine')


class AudioEngeneWaveGenerator(NSObject, auto_rename=True):
  audioEngine: AVAudioEngine = objc_property()
  #audioEngine = AVAudioEngine.new()
  

  @objc_method
  def initAudioEngene(self):
    self.audioEngine = AVAudioEngine.new()
    pdbr.state(self.audioEngine)
    return self


if __name__ == "__main__":
  _vc = TopViewController.new()
  _generator = AudioEngeneWaveGenerator.alloc().initAudioEngene()
  present_ViewController(_vc)


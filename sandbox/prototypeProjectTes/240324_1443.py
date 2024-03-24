import ctypes

from pyrubicon.objc import ObjCInstance, ObjCClass, NSObject, ObjCProtocol, objc_method, objc_property, py_from_ns
from pyrubicon.objc import Block
from pyrubicon.objc.runtime import SEL, send_super

from dispatchSync import dispatch_sync

import pdbr

CHANNEL = 1

OSStatus = ctypes.c_int32

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioSourceNode = ObjCClass('AVAudioSourceNode')
AVAudioFormat = ObjCClass('AVAudioFormat')

#AVAudioMixerNode = ObjCClass('AVAudioMixerNode')  # todo: 定義のみ
#AVAudioOutputNode = ObjCClass('AVAudioOutputNode')  # todo: 定義のみ


class AudioBuffer(ctypes.Structure):
  _fields_ = [
    ('mNumberChannels', ctypes.c_uint32),
    ('mDataByteSize', ctypes.c_uint32),
    ('mData', ctypes.c_void_p),
  ]


class AudioBufferList(ctypes.Structure):
  _fields_ = [
    ('mNumberBuffers', ctypes.c_uint32),
    ('mBuffers', AudioBuffer * CHANNEL),
  ]


class AudioEngeneWaveGenerator(NSObject, auto_rename=True):
  audioEngine: AVAudioEngine = objc_property()
  sampleRate: float = objc_property()  # xxx: わざわざ不要か？
  deltaTime: float = objc_property()
  timex: float = objc_property()

  @objc_method
  def initGenerator(self):
    audioEngine = AVAudioEngine.new()
    
    mainMixer = audioEngine.mainMixerNode
    outputNode = audioEngine.outputNode
    format = outputNode.inputFormatForBus_(0)

    self.sampleRate = format.sampleRate
    self.deltaTime = 1 / py_from_ns(self.sampleRate)
    inputFormat = AVAudioFormat.alloc(
    ).initWithCommonFormat_sampleRate_channels_interleaved_(
      format.commonFormat, py_from_ns(self.sampleRate), CHANNEL,
      format.isInterleaved)

    
    sourceNode = AVAudioSourceNode.alloc()
    
    self.audioEngine = audioEngine
    return self


ag = AudioEngeneWaveGenerator.alloc().initGenerator()

#pdbr.state(AudioEngeneWaveGenerator)

UINavigationController = ObjCClass('UINavigationController')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')
UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')


class TopViewController(UIViewController, auto_rename=True):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.view.backgroundColor = UIColor.systemDarkRedColor()

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    pass


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


def main():
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  root_vc = window.rootViewController

  while root_vc.presentedViewController:
    root_vc = root_vc.presentedViewController

  vc = TopViewController.new()

  @Block
  def processing() -> None:
    nv = WrapNavigationController.alloc().initWithRootViewController_(vc)
    nv.delegate = nv
    nv.setModalPresentationStyle_(1)

    root_vc.presentViewController_animated_completion_(nv, True, None)

  dispatch_sync(processing)


if __name__ == "__main__":
  main()


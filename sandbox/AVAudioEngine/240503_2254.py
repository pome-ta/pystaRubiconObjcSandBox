from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method, objc_property
from pyrubicon.objc.api import NSObject
from pyrubicon.objc.runtime import SEL, send_super

from mainThread import onMainThread
import pdbr

ObjCClass.auto_rename = True

# --- UINavigationController
UINavigationController = ObjCClass('UINavigationController')
UINavigationControllerDelegate = ObjCProtocol('UINavigationControllerDelegate')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

# --- UIViewController
UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
UIButtonConfiguration = ObjCClass('UIButtonConfiguration')
UIButton = ObjCClass('UIButton')
touchUpInside = 1 << 6

NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

pageSheet = 1  # xxx: あとでちゃんと定義する


@onMainThread
def present_viewController(myVC: UIViewController):
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  rootVC = window.rootViewController

  while _presentedVC := rootVC.presentedViewController:
    rootVC = _presentedVC

  myNC = RootNavigationController.alloc().initWithRootViewController_(myVC)

  presentVC = myNC
  presentVC.setModalPresentationStyle_(1)

  rootVC.presentViewController_animated_completion_(presentVC, True, None)


# --- NavigationController
class RootNavigationController(UINavigationController,
                               protocols=[UINavigationControllerDelegate]):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    appearance = UINavigationBarAppearance.new()
    appearance.configureWithDefaultBackground()

    navigationBar = self.navigationBar
    navigationBar.standardAppearance = appearance
    navigationBar.scrollEdgeAppearance = appearance
    navigationBar.compactAppearance = appearance
    navigationBar.compactScrollEdgeAppearance = appearance

    self.delegate = self

  @objc_method
  def doneButtonTapped_(self, sender):
    visibleViewController = self.visibleViewController
    visibleViewController.dismissViewControllerAnimated_completion_(True, None)

  @objc_method
  def navigationController_willShowViewController_animated_(
      self, navigationController, viewController, animated: bool):
    viewController.setEdgesForExtendedLayout_(0)
    doneButton = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, navigationController,
                                                 SEL('doneButtonTapped:'))
    visibleViewController = navigationController.visibleViewController

    navigationItem = visibleViewController.navigationItem
    navigationItem.rightBarButtonItem = doneButton


# --- ViewController
class MainViewController(UIViewController):
  #waveGenerator = objc_property()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = 'sine wave'
    self.waveGenerator = WaveGenerator.new()
    self.waveGenerator.prepare()
    self.waveGenerator.start()

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__, self, 'viewWillDisappear:')
    self.waveGenerator.dispose()


# --- AVAudioEngine
import ctypes
from math import sin, pi

from pyrubicon.objc.runtime import  load_library
from pyrubicon.objc.api import Block

#Core Audio Types

AVFoundation = load_library('CoreAudio')

OSStatus = ctypes.c_int32

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioFormat = ObjCClass('AVAudioFormat')
AVAudioSourceNode = ObjCClass('AVAudioSourceNode')

CHANNEL = 1


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


class WaveGenerator(NSObject):
  #audioEngine = objc_property()
  '''
  sampleRate = objc_property(float)
  time = objc_property(float)
  deltaTime = objc_property(float)
  toneA = objc_property(float)

  sourceNode = objc_property()
  '''

  @objc_method
  def init(self):
    self.audioEngine = AVAudioEngine.new()

    self.sampleRate = 44100.0
    self.time = 0.0
    self.deltaTime = 0.0

    @Block
    def renderBlock(isSilence: ctypes.c_void_p, timestamp: ctypes.c_void_p,
                    frameCount: ctypes.c_int32,
                    outputData: ctypes.c_void_p) -> OSStatus:
      #print('h')
      return 0

    self.sourceNode = AVAudioSourceNode.alloc().initWithRenderBlock_(
      renderBlock)

    return self

  @objc_method
  def initAudioEngene(self):
    self.mainMixer = self.audioEngine.mainMixerNode
    self.outputNode = self.audioEngine.outputNode
    self.format = self.outputNode.inputFormatForBus_(0)

    self.sampleRate = float(self.format.sampleRate)
    self.deltaTime = 1.0 / self.sampleRate

  @objc_method
  def prepare(self):
    self.initAudioEngene()

  @objc_method
  def start(self):
    inputFormat = AVAudioFormat.alloc(
    ).initWithCommonFormat_sampleRate_channels_interleaved_(
      self.format.commonFormat, self.sampleRate, 1, self.format.isInterleaved)
    self.audioEngine.attachNode_(self.sourceNode)
    self.audioEngine.connect_to_format_(self.sourceNode, self.mainMixer,
                                        inputFormat)

    try:
      self.audioEngine.startAndReturnError_(None)

    except Exception as e:
      print(f'{e}: エラー')

  @objc_method
  def stop(self):
    self.audioEngine.stop()

  @objc_method
  def dispose(self):
    self.stop()


if __name__ == "__main__":
  vc = MainViewController.new()
  present_viewController(vc)


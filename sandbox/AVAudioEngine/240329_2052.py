from math import sin, pi
import ctypes

from pyrubicon.objc.api import ObjCInstance, ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_property, objc_method
from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import Block
from pyrubicon.objc.runtime import SEL  #, send_super

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

  @objc_method
  def viewDidLoad(self):
    playSineWave()


AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioPlayerNode = ObjCClass('AVAudioPlayerNode')
AVAudioPCMBuffer = ObjCClass('AVAudioPCMBuffer')

audioEngine = AVAudioEngine.new()
player = AVAudioPlayerNode.new()


def playSineWave():
  audioFormat = player.outputFormatForBus_(0)

  sampleRate = audioFormat.sampleRate
  length = 3.0 * sampleRate

  buffer = AVAudioPCMBuffer.alloc().initWithPCMFormat_frameCapacity_(
    audioFormat, ctypes.c_uint32(int(length)))

  buffer.frameLength = ctypes.c_uint32(int(length))

  channels = int(audioFormat.channelCount)

  for ch in range(channels):
    samples = buffer.floatChannelData[ch]
    for n in range(buffer.frameLength):
      samples[n] = sin(2.0 * pi * 440.0 * float(n) / sampleRate)

  audioEngine.attachNode_(player)
  mixer = audioEngine.mainMixerNode
  audioEngine.connect_to_format_(player, mixer, audioFormat)

  @Block
  def completionHandler() -> ctypes.c_void_p:
    print('Play completed')

  player.scheduleBuffer_completionHandler_(buffer, completionHandler)

  try:
    audioEngine.startAndReturnError_(None)
    player.play()
  except:
    print('error')


if __name__ == "__main__":

  _vc = TopViewController.new()
  present_ViewController(_vc)


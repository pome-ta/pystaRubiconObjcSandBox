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

  #generator = objc_property()

  @objc_method
  def viewDidLoad(self):
    self.generator = AudioEngeneWaveGenerator.alloc().initAudioEngene()
    self.generator.start()

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    self.generator.stop()


# --- AVAudioEngine
from math import sin, pi
from random import random, uniform

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


bufferList_pointer = ctypes.POINTER(AudioBufferList)


class AudioEngeneWaveGenerator(NSObject, auto_rename=True):

  @objc_method
  def callInitialize(self):
    # todo: rubicon -> python としての変数定義的な
    self.audioEngine = AVAudioEngine.new()
    self.sampleRate = 44100.0
    self.deltaTime = 0.0
    self.time = 0.0
    self.toneA = 440.0

    @Block
    def renderBlock(isSilence: ctypes.c_void_p, timestamp: ctypes.c_void_p,
                    frameCount: ctypes.c_int32,
                    outputData: ctypes.c_void_p) -> OSStatus:

      ablPointer = ctypes.cast(outputData, bufferList_pointer).contents

      _time = self.time
      _deltaTime = self.deltaTime
      _toneA = self.toneA

      for frame in range(frameCount):
        sampleVal = sin(_toneA * 2.0 * pi * _time)
        _time += _deltaTime

        for buffer in range(ablPointer.mNumberBuffers):
          _mData = ablPointer.mBuffers[buffer].mData
          _pointer = ctypes.POINTER(ctypes.c_float * frameCount)
          _buf = ctypes.cast(_mData, _pointer).contents
          _buf[frame] = sampleVal

      self.time = _time
      self.deltaTime = _deltaTime
      self.toneA = _toneA
      return 0

    self.sourceNode = AVAudioSourceNode.alloc().initWithRenderBlock_(
      renderBlock)

  @objc_method
  def initAudioEngene(self):
    self.callInitialize()

    self.mainMixer = self.audioEngine.mainMixerNode
    self.outputNode = self.audioEngine.outputNode
    self.format = self.outputNode.inputFormatForBus_(0)

    self.sampleRate = self.format.sampleRate
    self.deltaTime = 1 / self.sampleRate

    return self

  @objc_method
  def start(self):

    inputFormat = AVAudioFormat.alloc(
    ).initWithCommonFormat_sampleRate_channels_interleaved_(
      self.format.commonFormat, self.sampleRate, CHANNEL,
      self.format.isInterleaved)

    self.audioEngine.attachNode_(self.sourceNode)
    self.audioEngine.connect_to_format_(self.sourceNode, self.mainMixer,
                                        inputFormat)

    self.audioEngine.connect_to_format_(self.mainMixer, self.outputNode, None)
    self.mainMixer.outputVolume = 0.5

    self.audioEngine.startAndReturnError_(None)

  @objc_method
  def stop(self):
    self.audioEngine.stop()


if __name__ == "__main__":
  _vc = TopViewController.new()
  present_ViewController(_vc)


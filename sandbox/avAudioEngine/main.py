import ctypes
from math import pi, sin
from random import uniform

from pyrubicon.objc.api import ObjCClass, Block
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.api import NSObject
from pyrubicon.objc.runtime import send_super

from rbedge.functions import NSStringFromClass

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
UISlider = ObjCClass('UISlider')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioFormat = ObjCClass('AVAudioFormat')
AVAudioSourceNode = ObjCClass('AVAudioSourceNode')

OSStatus = ctypes.c_int32
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


# --- OSC
amplitude: float = 1.0
frequency: float = 440.0


def white_noise():
  return uniform(-1.0, 1.0)


def sine(time):
  wave = amplitude * sin(2.0 * pi * frequency * time)
  return wave


class Synth(NSObject):

  audioEngine: AVAudioEngine = objc_property()
  time: float = objc_property(float)
  sampleRate: float = objc_property(float)
  deltaTime: float = objc_property(float)

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t - {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    #print(f'{NSStringFromClass(__class__)}: init')
    audioEngine = AVAudioEngine.new()

    mainMixer = audioEngine.mainMixerNode
    outputNode = audioEngine.outputNode
    format = outputNode.inputFormatForBus_(0)

    sampleRate = format.sampleRate
    deltaTime = 1 / sampleRate

    inputFormat = AVAudioFormat.alloc(
    ).initWithCommonFormat_sampleRate_channels_interleaved_(
      format.commonFormat, sampleRate, CHANNEL, format.isInterleaved())

    sourceNode = AVAudioSourceNode.alloc().initWithRenderBlock_(
      Block(
        self.__renderBlock,
        OSStatus,
        *[
          ctypes.c_bool,  # isSilence
          ctypes.c_void_p,  # timestamp
          ctypes.c_uint,  # frameCount
          ctypes.c_void_p,  # outputData
        ]))
    audioEngine.attachNode_(sourceNode)
    audioEngine.connect_to_format_(sourceNode, mainMixer, inputFormat)
    audioEngine.connect_to_format_(mainMixer, outputNode, None)
    mainMixer.outputVolume = 0.5

    audioEngine.prepare()  # xxx: 不要？

    self.audioEngine = audioEngine
    self.time = 0.0
    self.sampleRate = sampleRate
    self.deltaTime = deltaTime

    return self

  @objc_method
  def __renderBlock(self, isSilence: ctypes.c_bool, timestamp: ctypes.c_void_p,
                    frameCount: ctypes.c_uint,
                    outputData: ctypes.c_void_p) -> OSStatus:
    ablPointer = ctypes.cast(outputData,
                             ctypes.POINTER(AudioBufferList)).contents
    mDataPointer = ctypes.POINTER(ctypes.c_float * frameCount)

    time = self.time  # todo: `self.time` だと、音出ない

    for frame in range(frameCount):
      sampleVal = sin(440.0 * 2.0 * pi * time)
      time += self.deltaTime

      for ch, buffer in enumerate(ablPointer.mBuffers):
        buf = ctypes.cast(buffer.mData, mDataPointer).contents
        buf[frame] = sampleVal

    self.time = time
    return 0

  @objc_method
  def start(self):
    try:
      self.audioEngine.startAndReturnError_(None)

    except Exception as e:
      print(f'{e}: エラー')

  @objc_method
  def stop(self):
    if self.audioEngine.isRunning():
      self.audioEngine.stop()


class MainViewController(UIViewController):

  synth: Synth = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'\t - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    #print(f'\t{NSStringFromClass(__class__)}: loadView')
    self.synth = Synth.new()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    #print(f'\t{NSStringFromClass(__class__)}: viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__) if (
      title := self.navigationItem.title) is None else title

    self.synth.start()

    # あとでボタンにする
    slider = UISlider.new()
    slider.value = 0.5
    slider.minimumValue = 0.0
    slider.maximumValue = 1.0

    # --- layout
    self.view.addSubview_(slider)
    slider.translatesAutoresizingMaskIntoConstraints = False

    areaLayoutGuide = self.view.safeAreaLayoutGuide
    NSLayoutConstraint.activateConstraints_([
      slider.centerXAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerXAnchor),
      slider.centerYAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerYAnchor),
      slider.leadingAnchor.constraintEqualToAnchor_constant_(
        areaLayoutGuide.leadingAnchor, 20.0),
      slider.trailingAnchor.constraintEqualToAnchor_constant_(
        areaLayoutGuide.trailingAnchor, -20.0),
    ])

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewDidAppear_')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewWillDisappear_')

    self.synth.stop()

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')


if __name__ == '__main__':
  from rbedge.app import App
  from rbedge.enumerations import UIModalPresentationStyle

  main_vc = MainViewController.new()

  #presentation_style = UIModalPresentationStyle.fullScreen
  presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()


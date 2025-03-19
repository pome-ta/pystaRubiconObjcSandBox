import ctypes
from math import pi, sin
from random import uniform

from pyrubicon.objc.api import ObjCClass, Block
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.api import NSObject
from pyrubicon.objc.runtime import send_super, SEL

from rbedge.enumerations import (
  UIControlEvents,
  UILayoutConstraintAxis,
  UIStackViewAlignment,
)
from rbedge.functions import NSStringFromClass

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
UIStackView = ObjCClass('UIStackView')
UISegmentedControl = ObjCClass('UISegmentedControl')
UISlider = ObjCClass('UISlider')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioFormat = ObjCClass('AVAudioFormat')
AVAudioSourceNode = ObjCClass('AVAudioSourceNode')

UIColor = ObjCClass('UIColor')

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
# wip: rubicon のオブジェクトとして持たせたくないので、気持ち悪いclass になってる
class Oscillator:

  def __init__(self, frequency: float = 440.0):
    self.frequency: float = frequency
    self.amplitude: float = 1.0
    self.wave_types = [
      self.sine,
      self.triangle,
      self.sawtooth,
      self.square,
      self.white_noise,
    ]

  @classmethod
  def type_value(cls,
                 select_type: int,
                 value: float,
                 frequency: float = 440.0):
    osc = cls(frequency)
    wave_type = osc.wave_types[select_type]
    return wave_type(value)

  @classmethod
  def type_name(cls, select_type: int) -> str:
    osc = cls()
    wave_type = osc.wave_types[select_type]
    return wave_type.__name__

  @classmethod
  def type_names(cls) -> list:
    osc = cls()
    return [wave_type.__name__ for wave_type in osc.wave_types]

  def sine(self, time) -> float:
    wave = self.amplitude * sin(2.0 * pi * self.frequency * time)
    return wave

  def triangle(self, time) -> float:
    period = 1.0 / self.frequency
    currentTime = time % period
    value = currentTime / period
    result = 0.0
    if value < 0.25:
      result = value * 4
    elif value < 0.75:
      result = 2.0 - (value * 4.0)
    else:
      result = value * 4 - 4.0
    wave = self.amplitude * result
    return wave

  def sawtooth(self, time) -> float:
    period = 1.0 / self.frequency
    currentTime = time % period
    wave = self.amplitude * ((currentTime / period) * 2 - 1.0)
    return wave

  def square(self, time) -> float:
    period = 1.0 / self.frequency
    currentTime = time % period
    if (currentTime / period) < 0.5:
      wave = self.amplitude
    else:
      wave = -1.0 * self.amplitude
    return wave

  def white_noise(self, _) -> float:
    return uniform(-1.0, 1.0)


class Synth(NSObject):

  audioEngine: AVAudioEngine = objc_property()
  time: float = objc_property(float)
  sampleRate: float = objc_property(float)
  deltaTime: float = objc_property(float)
  signal: int = objc_property(int)

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
    mainMixer.outputVolume = 0.2

    audioEngine.prepare()  # xxx: 不要？

    self.audioEngine = audioEngine
    self.time = 0.0
    self.sampleRate = sampleRate
    self.deltaTime = deltaTime
    self.signal = 0

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
      sampleVal = Oscillator.type_value(self.signal, time)
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

    # --- vew
    wave_names = Oscillator.type_names()
    segmentedControl = UISegmentedControl.alloc().initWithItems_(wave_names)
    segmentedControl.selectedSegmentIndex = 0
    segmentedControl.addTarget_action_forControlEvents_(
      self, SEL('selectedSegmentDidChange:'), UIControlEvents.valueChanged)

    slider = UISlider.new()
    slider.setContinuous_(False)
    slider.value = 0.0
    slider.minimumValue = 0.0
    slider.maximumValue = 4.0
    slider.addTarget_action_forControlEvents_(self,
                                              SEL('sliderValueDidChange:'),
                                              UIControlEvents.valueChanged)

    # --- layout
    stackView = UIStackView.alloc().initWithArrangedSubviews_([
      segmentedControl,
      slider,
    ])
    stackView.backgroundColor = UIColor.systemBackgroundColor()
    stackView.axis = UILayoutConstraintAxis.vertical
    stackView.alignment = UIStackViewAlignment.center
    stackView.spacing = 32.0

    self.view.addSubview_(stackView)
    stackView.translatesAutoresizingMaskIntoConstraints = False
    segmentedControl.translatesAutoresizingMaskIntoConstraints = False
    slider.translatesAutoresizingMaskIntoConstraints = False

    areaLayoutGuide = self.view.safeAreaLayoutGuide
    # --- stackView
    NSLayoutConstraint.activateConstraints_([
      stackView.centerXAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerXAnchor),
      stackView.centerYAnchor.constraintEqualToAnchor_(
        areaLayoutGuide.centerYAnchor),
      stackView.leadingAnchor.constraintEqualToAnchor_constant_(
        areaLayoutGuide.leadingAnchor, 24.0),
      stackView.trailingAnchor.constraintEqualToAnchor_constant_(
        areaLayoutGuide.trailingAnchor, -24.0),
    ])
    # --- segmentedControl
    NSLayoutConstraint.activateConstraints_([
      segmentedControl.leadingAnchor.constraintEqualToAnchor_(
        stackView.leadingAnchor),
      segmentedControl.trailingAnchor.constraintEqualToAnchor_(
        stackView.trailingAnchor),
    ])
    # --- slider
    NSLayoutConstraint.activateConstraints_([
      slider.leadingAnchor.constraintEqualToAnchor_(stackView.leadingAnchor),
      slider.trailingAnchor.constraintEqualToAnchor_(stackView.trailingAnchor),
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

  @objc_method
  def selectedSegmentDidChange_(self, segmentedControl):
    self.synth.signal = segmentedControl.selectedSegmentIndex
    #print(f'The selected segment: {segmentedControl.selectedSegmentIndex}')

  # MARK: - Actions
  @objc_method
  def sliderValueDidChange_(self, slider):
    int_value = int(slider.value)
    '''
    self.synth.signal = int_value
    slider.value = float(int_value)
    print(f'Slider changed its value: {int_value} to {Oscillator.type_name(int_value)}')
    '''


if __name__ == '__main__':
  from rbedge.app import App
  from rbedge.enumerations import UIModalPresentationStyle

  main_vc = MainViewController.new()

  #presentation_style = UIModalPresentationStyle.fullScreen
  presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()


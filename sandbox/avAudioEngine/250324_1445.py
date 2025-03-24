import ctypes
import struct
from math import pi, sin
from random import uniform

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.api import NSObject
from pyrubicon.objc.runtime import send_super, SEL

from rbedge.enumerations import (
  UIControlEvents,
  UILayoutConstraintAxis,
  UIStackViewAlignment,
)
from rbedge.functions import NSStringFromClass
from rbedge.objcMainThread import onMainThread

from rbedge import pdbr

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioFormat = ObjCClass('AVAudioFormat')
AVAudioSourceNode = ObjCClass('AVAudioSourceNode')

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')

UIStackView = ObjCClass('UIStackView')
UISegmentedControl = ObjCClass('UISegmentedControl')
UISlider = ObjCClass('UISlider')
UILabel = ObjCClass('UILabel')

width_size: int = 40
height_size: int = 24

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
class Oscillator(NSObject):

  frequency: float = objc_property(float)
  amplitude: float = objc_property(float)
  waveTypes: list = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t - {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    self.frequency = 440.0
    self.amplitude = 1.0

    waveForms = [
      'sine',
      'triangle',
      'sawtooth',
      'square',
      'whiteNoise',
    ]
    self.waveTypes = [waveForm for waveForm in waveForms]

    return self

  @objc_method
  def sine(self, time: float, frequency: float, amplitude: float) -> float:
    wave = amplitude * sin(2.0 * pi * frequency * time)
    return wave

  @objc_method
  def triangle(self, time: float, frequency: float, amplitude: float) -> float:
    period = 1.0 / frequency
    currentTime = time % period
    value = currentTime / period
    result = 0.0
    if value < 0.25:
      result = value * 4
    elif value < 0.75:
      result = 2.0 - (value * 4.0)
    else:
      result = value * 4 - 4.0
    wave = amplitude * result
    return wave

  @objc_method
  def sawtooth(self, time: float, frequency: float, amplitude: float) -> float:
    period = 1.0 / frequency
    currentTime = time % period
    wave = amplitude * ((currentTime / period) * 2 - 1.0)
    return wave

  @objc_method
  def square(self, time: float, frequency: float, amplitude: float) -> float:
    period = 1.0 / frequency
    currentTime = time % period
    if (currentTime / period) < 0.5:
      wave = amplitude
    else:
      wave = -1.0 * amplitude
    return wave

  @objc_method
  def whiteNoise(self, time: float, frequency: float,
                 amplitude: float) -> float:
    wave = uniform(-1.0, 1.0)
    return wave


class Synth(Oscillator):

  audioEngine: AVAudioEngine = objc_property()
  time: float = objc_property(float)
  sampleRate: float = objc_property(float)
  deltaTime: float = objc_property(float)

  waveType: int = objc_property(int)
  #tapBufferDatas: list = objc_property(weak=True)
  textView = objc_property()

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
        self._renderBlock,
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

    _bufsize = width_size * height_size  # 取得する情報量
    #17640
    mainMixer.installTapOnBus_bufferSize_format_block_(
      0, _bufsize, inputFormat,
      Block(self._tapBlock, None, *[
        ctypes.c_void_p,
        ctypes.c_void_p,
      ]))

    audioEngine.prepare()  # xxx: 不要?

    self.audioEngine = audioEngine
    self.time = 0.0
    self.sampleRate = sampleRate
    self.deltaTime = deltaTime

    self.waveType = 0
    #self.tapBufferDatas = []

    return self

  @objc_method
  def _renderBlock(self, isSilence: ctypes.c_bool, timestamp: ctypes.c_void_p,
                   frameCount: ctypes.c_uint,
                   outputData: ctypes.c_void_p) -> OSStatus:
    ablPointer = ctypes.cast(outputData,
                             ctypes.POINTER(AudioBufferList)).contents
    mDataPointer = ctypes.POINTER(ctypes.c_float * frameCount)
    # todo: `self.` だと、音出ないので、変数化
    _time = self.time
    _frequency = self.frequency
    _amplitude = self.amplitude
    _waveType = self.waveType

    if _waveType == 0:
      _signal = self.sine
    elif _waveType == 1:
      _signal = self.triangle
    elif _waveType == 2:
      _signal = self.sawtooth
    elif _waveType == 3:
      _signal = self.square
    elif _waveType == 4:
      _signal = self.whiteNoise
    else:
      _signal = self.sine

    for frame in range(frameCount):
      sampleVal = _signal(_time, _frequency, _amplitude)
      _time += self.deltaTime
      for ch, buffer in enumerate(ablPointer.mBuffers):
        buf = ctypes.cast(buffer.mData, mDataPointer).contents
        buf[frame] = sampleVal
    self.time = _time
    return 0

  @objc_method
  def _tapBlock(self, buffer: ctypes.c_void_p, when: ctypes.c_void_p) -> None:
    buff = ObjCInstance(buffer)
    floatChannelDatas = buff.floatChannelData
    floatChannelData = floatChannelDatas[0]
    '''
    self.tapBufferDatas = [
      floatChannelData[i] for i in range(width_size * height_size)
    ]
    '''
    if self.textView is not None:

      @onMainThread
      def mainThread():
        self.textView.text = f'{floatChannelData[0]}'

      #print(floatChannelData[0])
      mainThread()

    #self.tapBufferDatas = float_datas

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
  label: UILabel = objc_property()

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

    # --- view
    wave_names = [waveType for waveType in self.synth.waveTypes]
    segmentedControl = UISegmentedControl.alloc().initWithItems_(wave_names)
    segmentedControl.selectedSegmentIndex = 0
    segmentedControl.addTarget_action_forControlEvents_(
      self, SEL('selectedSegmentDidChange:'), UIControlEvents.valueChanged)

    value = 440.0
    label = UILabel.new()
    label.text = f'frequency: {value:.2f}'

    textView = UILabel.new()
    textView.text = 'hoge'

    slider = UISlider.new()
    #slider.setContinuous_(False)
    slider.minimumValue = 110.0
    slider.maximumValue = 880.0
    slider.value = value
    slider.addTarget(self,
                     action=SEL('sliderValueDidChange:'),
                     forControlEvents=UIControlEvents.valueChanged)
    # --- layout
    stackView = UIStackView.alloc().initWithArrangedSubviews_([
      textView,
      segmentedControl,
      label,
      slider,
    ])
    #stackView.backgroundColor = UIColor.systemBackgroundColor()
    stackView.axis = UILayoutConstraintAxis.vertical
    stackView.alignment = UIStackViewAlignment.center
    stackView.spacing = 32.0

    self.view.addSubview_(stackView)
    stackView.translatesAutoresizingMaskIntoConstraints = False
    label.translatesAutoresizingMaskIntoConstraints = False
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
    # --- label
    NSLayoutConstraint.activateConstraints_([
      label.leadingAnchor.constraintEqualToAnchor_(stackView.leadingAnchor),
      label.trailingAnchor.constraintEqualToAnchor_(stackView.trailingAnchor),
    ])
    # --- slider
    NSLayoutConstraint.activateConstraints_([
      slider.leadingAnchor.constraintEqualToAnchor_(stackView.leadingAnchor),
      slider.trailingAnchor.constraintEqualToAnchor_(stackView.trailingAnchor),
    ])

    self.synth.textView = textView
    self.label = label

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
    #print(self.synth.tapBufferDatas)
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
    index = segmentedControl.selectedSegmentIndex
    self.synth.waveType = index

  # MARK: - Actions
  @objc_method
  def sliderValueDidChange_(self, slider):
    '''
    value = float(int(slider.value))
    self.synth.frequency = value
    slider.value = value
    '''
    value = int(slider.value * 100) / 100
    self.synth.frequency = value
    self.label.text = f'frequency: {value:.2f}'


if __name__ == '__main__':
  from rbedge.app import App
  from rbedge.enumerations import UIModalPresentationStyle

  main_vc = MainViewController.new()

  #presentation_style = UIModalPresentationStyle.fullScreen
  presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()


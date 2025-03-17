"""
[【iOS】Core Audioでシンセサイザーを作る #Swift - Qiita](https://qiita.com/TokyoYoshida/items/df60ea8585a0223e868b)
"""

import ctypes

from pyrubicon.objc.api import ObjCClass, Block
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.api import NSObject
from pyrubicon.objc.runtime import send_super

from rbedge.functions import NSStringFromClass

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')

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


class Synth(NSObject):

  audioEngine: AVAudioEngine = objc_property()
  sampleRate: float = objc_property(float)
  deltaTime: float = objc_property(float)

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t - {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    print(f'{NSStringFromClass(__class__)}: init')
    audioEngine = AVAudioEngine.new()

    mainMixer = audioEngine.mainMixerNode
    outputNode = audioEngine.outputNode
    format = outputNode.inputFormatForBus_(0)

    sampleRate = format.sampleRate
    deltaTime = 1 / sampleRate

    inputFormat = AVAudioFormat.alloc(
    ).initWithCommonFormat_sampleRate_channels_interleaved_(
      format.commonFormat, sampleRate, CHANNEL, format.isInterleaved())

    @Block
    def renderBlock(isSilence: ctypes.c_bool, timestamp: ctypes.c_void_p,
                    frameCount: ctypes.c_uint,
                    outputData: ctypes.c_void_p) -> OSStatus:
      #print(f'{isSilence=}, {timestamp=}, {frameCount=}, {outputData=}')
      ablPointer = ctypes.cast(outputData, ctypes.POINTER(AudioBufferList)).contents
      #print(dir(ablPointer.mNumberBuffers))
      #print(ablPointer.mNumberBuffers)
      #print(ablPointer.mNumberBuffers)
      #print(ablPointer.mBuffers)
      #print(ctypes.cast(ablPointer.mBuffers,ctypes.POINTER(AudioBuffer)))
      
      for buffer in range(ablPointer.mNumberBuffers):
        print(buffer)

      return 0

    sourceNode = AVAudioSourceNode.alloc().initWithRenderBlock_(renderBlock)
    audioEngine.attachNode_(sourceNode)
    audioEngine.connect_to_format_(sourceNode, mainMixer, inputFormat)
    audioEngine.connect_to_format_(mainMixer, outputNode, None)
    mainMixer.outputVolume = 0.5

    # xxx: 不要？
    audioEngine.prepare()

    self.audioEngine = audioEngine
    self.sampleRate = sampleRate
    self.deltaTime = deltaTime

    return self

  @objc_method
  def start(self):
    try:
      self.audioEngine.startAndReturnError_(None)

    except Exception as e:
      print(f'{e}: エラー')

  @objc_method
  def stop(self):
    self.audioEngine.stop()


class MainViewController(UIViewController):

  #synth: Synth = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'\t - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    #print(f'\t{NSStringFromClass(__class__)}: loadView')
    #self.synth = Synth.new()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    #print(f'\t{NSStringFromClass(__class__)}: viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__) if (
      title := self.navigationItem.title) is None else title

    #self.synth.start()
    synth = Synth.new()
    synth.start()

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
    #self.synth.stop()

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


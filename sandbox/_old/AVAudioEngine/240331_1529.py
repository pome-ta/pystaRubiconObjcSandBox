import ctypes

from pyrubicon.objc.api import ObjCInstance, ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_property, objc_method
from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import Block

import pdbr

# --- AVAudioEngine
from math import sin, pi
from random import random

OSStatus = ctypes.c_int32

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioFormat = ObjCClass('AVAudioFormat')
AVAudioSourceNode = ObjCClass('AVAudioSourceNode')
# xxx: 定義用での呼び出しのみ?
AVAudioMixerNode = ObjCClass('AVAudioMixerNode')
AVAudioOutputNode = ObjCClass('AVAudioOutputNode')

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


class AudioEngeneWaveGenerator(NSObject, auto_rename=True):
  audioEngine: AVAudioEngine = objc_property()
  sampleRate: float
  deltaTime: float
  mainMixer: AVAudioMixerNode = property()
  outputNode: AVAudioOutputNode = property()
  format: AVAudioFormat = property()
  sourceNode = property()

  @objc_method
  def callInitialize(self):
    # todo: rubicon -> python としての変数定義的な
    self.audioEngine = AVAudioEngine.new()
    self.sampleRate = 44100.0
    self.deltaTime = 0.0
    self.time = 0.0
    self.toneA = 440.0

    bufferList_pointer = ctypes.POINTER(AudioBufferList)

    @Block
    def renderBlock(isSilence: ctypes.c_void_p, timestamp: ctypes.c_void_p,
                    frameCount: ctypes.c_void_p,
                    outputData: ctypes.c_void_p) -> OSStatus:

      ablPointer = ctypes.cast(outputData, bufferList_pointer).contents

      for frame in range(frameCount):
        sampleVal = random()

        for buffer in range(ablPointer.mNumberBuffers):
          _mData = ablPointer.mBuffers[buffer].mData
          _pointer = ctypes.POINTER(ctypes.c_float * frameCount)
          _buf = ctypes.cast(_mData, _pointer).contents
          _buf[frame] = sampleVal
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

    #pdbr.state(inputFormat)
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
  wg = AudioEngeneWaveGenerator.alloc().initAudioEngene()
  wg.start()


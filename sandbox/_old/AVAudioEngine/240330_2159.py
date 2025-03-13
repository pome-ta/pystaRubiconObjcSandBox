import ctypes

from pyrubicon.objc.api import ObjCInstance, ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_property, objc_method
from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import Block
from pyrubicon.objc.runtime import SEL  #, send_super

import pdbr

# --- AVAudioEngine
from math import sin, pi
from random import random

OSStatus = ctypes.c_int32

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioFormat = ObjCClass('AVAudioFormat')
AVAudioSourceNode = ObjCClass('AVAudioSourceNode')
# xxx: 定義用での呼び出しのみ？
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
    ('mNumberBuffers', ctypes.c_uint),
    ('mBuffers', AudioBuffer * 1),
  ]


audioEngine = AVAudioEngine.new()
sampleRate = 44100.0
deltaTime = 0.0
timex = 0.0
toneA = 440.0

mainMixer = audioEngine.mainMixerNode
outputNode = audioEngine.outputNode
format = outputNode.inputFormatForBus_(0)

sampleRate = format.sampleRate
deltaTime = 1 / sampleRate

inputFormat = AVAudioFormat.alloc(
).initWithCommonFormat_sampleRate_channels_interleaved_(
  format.commonFormat, sampleRate, CHANNEL, format.isInterleaved)

bufferList_pointer = ctypes.POINTER(AudioBufferList)


@Block
def renderBlock(isSilence: ctypes.c_void_p, timestamp: ctypes.c_void_p,
                frameCount: ctypes.c_void_p,
                outputData: ctypes.c_void_p) -> OSStatus:
  ablPointer = ctypes.cast(outputData, bufferList_pointer).contents
  #print('h')

  for frame in range(frameCount):
    sampleVal = random()#sin(toneA * 2.0 * pi * timex)
    #timex += deltaTime

    for buffer in range(ablPointer.mNumberBuffers):
      _mData = ablPointer.mBuffers[buffer].mData
      _pointer = ctypes.POINTER(ctypes.c_float * frameCount)
      _buf = ctypes.cast(_mData, _pointer).contents
      _buf[frame] = sampleVal
  return 0


sourceNode = AVAudioSourceNode.alloc().initWithRenderBlock_(renderBlock)

#sourceNode = AVAudioSourceNode.alloc().initWithFormat_renderBlock_(inputFormat, renderBlock)

audioEngine.attachNode_(sourceNode)
audioEngine.connect_to_format_(sourceNode, mainMixer, inputFormat)

audioEngine.connect_to_format_(mainMixer, outputNode, None)
mainMixer.outputVolume = 0.5

audioEngine.startAndReturnError_(None)


from math import sin, pi
import ctypes
from pyrubicon.objc.api import ObjCClass, Block
from pyrubicon.objc.runtime import load_library

import pdbr

load_library('AVFoundation')

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
    pdbr.state(audioEngine)

  player.scheduleBuffer_completionHandler_(buffer, completionHandler)
  pdbr.state(player)

  try:
    audioEngine.startAndReturnError_(None)
    player.play()
    print('play')
  except:
    print('error')


if __name__ == "__main__":
  playSineWave()


from math import sin, pi
import ctypes
from pyrubicon.objc.api import ObjCClass, Block

import pdbr

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioPlayerNode = ObjCClass('AVAudioPlayerNode')
AVAudioPCMBuffer = ObjCClass('AVAudioPCMBuffer')

audioEngine = AVAudioEngine.new()
player = AVAudioPlayerNode.new()



def playSineWave(call_time: float = 3.0):
  audioFormat = player.outputFormatForBus_(0)
  #audioFormat.channelCount = 1
  #pdbr.state(audioFormat.channelCount)
  #print(audioFormat.channelCount)

  sampleRate = audioFormat.sampleRate
  length = call_time * sampleRate

  buffer = AVAudioPCMBuffer.alloc().initWithPCMFormat_frameCapacity_(
    audioFormat, ctypes.c_uint32(int(length)))

  buffer.frameLength = ctypes.c_uint32(int(length))

  channels = int(audioFormat.channelCount)

  for ch in range(channels):
    samples = buffer.floatChannelData[ch]
    for n in range(buffer.frameLength):
      samples[n] = sin(2.0 * pi * 440.0 * float(n) / sampleRate)

  #pdbr.state(buffer.audioBufferList)
  #print(dir(buffer.audioBufferList))
  pr = buffer.audioBufferList.contents.field_1
  #field_0:  UInt32      mNumberBuffers; -> 2
  #field_1:  AudioBuffer mBuffers[1];    -> [1]
  
  print(pr)
  print(type(pr))
  print(dir(pr))
  
  #pdbr.state(pr)
  '''
  for i in pr:
    print(dir(i))
  '''
  audioEngine.attachNode_(player)
  mixer = audioEngine.mainMixerNode
  mixer.outputVolume = 0.1
  audioEngine.connect_to_format_(player, mixer, audioFormat)

  @Block
  def completionHandler() -> ctypes.c_void_p:
    #print('Play completed')
    pass

  player.scheduleBuffer_completionHandler_(buffer, completionHandler)

  try:
    audioEngine.startAndReturnError_(None)
    player.play()
    #print(audioEngine)
  except:
    print('error')


if __name__ == "__main__":
  playSineWave(0.1)


# 📝 2024/05/06


## `block` 内の処理

ctypes でこねこねするから、メモ

```.py
ctypes.cast(outputData, ctypes.POINTER(AudioBufferList))

'''
['__bool__', '__class__', '__ctypes_from_outparam__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_b_base_', '_b_needsfree_', '_objects', '_type_', 'contents']
'''


ctypes.cast(outputData, ctypes.POINTER(AudioBufferList)).contents

'''
['__class__', '__ctypes_from_outparam__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_b_base_', '_b_needsfree_', '_fields_', '_objects', 'mBuffers', 'mNumberBuffers']
'''

```


```.py

for buffer in abl.mBuffers:
  print(buffer)
  print(dir(buffer))


'''
<__main__.AudioBuffer object at 0x118ebdfc0>
['__class__', '__ctypes_from_outparam__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_b_base_', '_b_needsfree_', '_fields_', '_objects', 'mData', 'mDataByteSize', 'mNumberChannels']
'''

```

## `UnsafeMutableAudioBufferListPointer` と`UnsafeMutableBufferPointer`

なかなか、わからんのでメモしながら整理していく


```.swift
lazy var sourceNode = AVAudioSourceNode { [self] (_, _, frameCount, audioBufferList) -> OSStatus in
    // `AudioBufferList` の、`mBuffers` 配列要素を操作できるような形式になる？
    let abl = UnsafeMutableAudioBufferListPointer(audioBufferList)
    // `frameCount` = `1024` とか
    for frame in 0..<Int(frameCount) {
        let sampleVal: Float = sin(AudioEngeneWaveGenerator.toneA * 2.0 * Float(Double.pi) * self.time)
        self.time += self.deltaTime
        // `frame` 分の時間処理をしてから呼び出しをしている
        // channel としては`1` なので1回の処理
        for buffer in abl {
            // 中身が`Float` となるってこと？形としては配列みたいな？
            // ここでキャストか
            let buf: UnsafeMutableBufferPointer<Float> = UnsafeMutableBufferPointer(buffer)
            buf[frame] = sampleVal
        }
    }
    return noErr
}
```








[UnsafeMutablePointer | Apple Developer Documentation](https://developer.apple.com/documentation/swift/unsafemutablepointer)





# 📝 2024/05/04


`load_library` でframework 取ってくるか？と思っても
あまり意味なさそう

構造体を自分で作るなのかな？

[Core Audio | Apple Developer Documentation](https://developer.apple.com/documentation/coreaudio?language=objc)


`.locatble` ? みたいなのを取ってくるのかな？


## 構造体


[AudioBuffer | Apple Developer Documentation](https://developer.apple.com/documentation/coreaudiotypes/audiobuffer?language=objc)


An audio buffer holds a single buffer of audio data in its mData field. The buffer can represent two types of audio:

- A single, monophonic, noninterleaved channel of audio
- Interleaved audio with the number of channels set by the mNumberChannels field

オーディオバッファは、mDataフィールドにオーディオデータの単一のバッファを保持します。バッファは2種類のオーディオを表すことができます。

- オーディオの単一、モノフォニック、非インターリーブチャンネル
- mNumberChannelsフィールドで設定されたチャンネル数のインターリーブオーディオ


[Core Audio その1 AudioBufferとAudioBufferList | objective-audio](kVariableLengthArray)


# 📝 2024/05/03

[GitHub - TokyoYoshida/CoreAudioExamples](https://github.com/TokyoYoshida/CoreAudioExamples)




# 📝 2024/05/02

[Building a Signal Generator | Apple Developer Documentation](https://developer.apple.com/documentation/avfaudio/audio_engine/building_a_signal_generator)


```.swift
let srcNode = AVAudioSourceNode { _, _, frameCount, audioBufferList -> OSStatus in
    let ablPointer = UnsafeMutableAudioBufferListPointer(audioBufferList)
    for frame in 0..<Int(frameCount) {
        // Get the signal value for this frame at time.
        let value = signal(currentPhase) * amplitude
        // Advance the phase for the next frame.
        currentPhase += phaseIncrement
        if currentPhase >= twoPi {
            currentPhase -= twoPi
        }
        if currentPhase < 0.0 {
            currentPhase += twoPi
        }
        // Set the same value on all channels (due to the inputFormat, there's only one channel though).
        for buffer in ablPointer {
            let buf: UnsafeMutableBufferPointer<Float> = UnsafeMutableBufferPointer(buffer)
            buf[frame] = value
        }
    }
    return noErr
}
```

# 📝 2024/05/01

[swift3でCoreAudioを使う 再生編 - Pebble Coding](https://pebble8888.hatenablog.com/entry/2015/12/05/192914)

[Building a Signal Generator | Apple Developer Documentation](https://developer.apple.com/documentation/avfaudio/audio_engine/building_a_signal_generator)

# 📝 2024/03/30

[Core Audio その１ AudioBufferとAudioBufferList | objective-audio](https://objective-audio.jp/2008/03/22/core-audio-audiobufferaudiobuf/)

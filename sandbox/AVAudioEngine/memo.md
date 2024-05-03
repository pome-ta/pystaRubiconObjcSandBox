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

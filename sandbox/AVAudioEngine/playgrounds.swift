import AVFoundation

let audioEngine = AVAudioEngine()
let player = AVAudioPlayerNode()

func playSineWave() {
    let audioFormat = player.outputFormat(forBus: 0)
    let sampleRate = Float(audioFormat.sampleRate)
    let length = 3.0 * sampleRate
    
    let buffer = AVAudioPCMBuffer(pcmFormat: audioFormat, frameCapacity: UInt32(length))
    buffer?.frameLength = UInt32(length)
    
    let channels = Int(audioFormat.channelCount)
    
    for ch in (0..<channels) {
        let samples = buffer?.floatChannelData?[ch]
        for n in 0..<Int(buffer!.frameLength) {
            samples![n] = sinf(Float(2.0 * M_PI) * 440.0 * Float(n) / sampleRate)
        }
        
    }
    audioEngine.attach(player)
    let mixer = audioEngine.mainMixerNode
    audioEngine.connect(player, to: mixer, format: audioFormat)
    player.scheduleBuffer(buffer!) {
        print("play completed")
    }
    
    do {
        try audioEngine.start()
        player.play()
        
    } catch let error {
        print(error)
    }
    
}

playSineWave()


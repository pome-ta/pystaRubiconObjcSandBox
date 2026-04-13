from pyrubicon.objc.api import ObjCClass, NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super


class SoundController(NSObject):

  _shared_instance: 'SoundController'

  backgroundMusicPlayer: 'AVAudioPlayer?' = objc_property()
  popEffect: 'AVAudioPlayer?' = objc_property()

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')

    return self


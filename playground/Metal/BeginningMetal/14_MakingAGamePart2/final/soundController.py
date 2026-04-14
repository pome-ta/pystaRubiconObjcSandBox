from pathlib import Path

from pyrubicon.objc.api import NSObject, ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property, objc_classmethod
from pyrubicon.objc.runtime import send_super

from rbedge.utils import nsurl, get_str_filepath
from rbedge.utils import readonly_class_properties

AVAudioPlayer = ObjCClass('AVAudioPlayer')

ROOT_PATH = Path(__file__).parents[0]


# wip: 雑
def _get_filepath(file_name: str) -> str | None:
  root = ROOT_PATH.parents[1] / 'assets'
  return get_str_filepath(root, file_name)


def get_sound_path(soundName: str) -> str | None:
  return _get_filepath(soundName)


@readonly_class_properties('shared')
class SoundController(NSObject):

  _shared_instance: 'SoundController'

  backgroundMusicPlayer: 'AVAudioPlayer?' = objc_property()
  popEffect: 'AVAudioPlayer?' = objc_property()

  @objc_classmethod
  def shared(cls):
    if getattr(cls, '_shared_instance', None) is None:
      cls._shared_instance = cls.new()
    return cls._shared_instance

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')

    self.popEffect = self.preloadSoundEffect_('pop.wav')

    return self

  @objc_method
  def playBackgroundMusic_(self, filename: object):
    self.backgroundMusicPlayer = self.preloadSoundEffect_(filename)
    try:  # `backgroundMusicPlayer?`
      self.backgroundMusicPlayer.numberOfLoops = -1
      self.backgroundMusicPlayer.play()
    except Exception as e:
      print(e)

  @objc_method
  def playPopEffect(self):
    try:  # `popEffect?.play()`
      self.popEffect.play()
    except Exception as e:
      print(e)

  @objc_method
  def preloadSoundEffect_(self, filename: object):
    if not (assetURL := get_sound_path(filename)):
      raise ValueError(f'Asset {filename} does not exist.')
    try:
      player = AVAudioPlayer.alloc().initWithContentsOfURL_error_(
        nsurl(assetURL), None)
      player.prepareToPlay()
      return player
    except Exception:
      print(f'file {filename} not found')

    return None


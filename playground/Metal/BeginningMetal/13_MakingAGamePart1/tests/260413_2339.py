"""
dummy
"""

from pathlib import Path
from rubicon.objc import ObjCClass
from rubicon.objc.api import NSObject, objc_method, objc_classmethod, objc_property
from rubicon.objc.runtime import send_super

NSURL = ObjCClass('NSURL')
AVAudioPlayer = ObjCClass('AVAudioPlayer')


class SoundController(NSObject):
  _shared_instance = None

  backgroundMusicPlayer = objc_property()
  popEffect = objc_property()

  # ★ ポイント1: Python標準の @classmethod ではなく、@objc_classmethod を使う
  @objc_classmethod
  def shared(cls):
    if cls._shared_instance is None:
      cls._shared_instance = cls.alloc().init()
    return cls._shared_instance

  @objc_method
  def init(self):
    self = send_super(__class__, self, 'init')
    if self:
      self.popEffect = self.preloadSoundEffect_("pop.wav")
    return self

  @objc_method
  def playBackgroundMusic_(self, filename: str):
    self.backgroundMusicPlayer = self.preloadSoundEffect_(filename)
    if self.backgroundMusicPlayer is not None:
      self.backgroundMusicPlayer.numberOfLoops = -1
      self.backgroundMusicPlayer.play()

  @objc_method
  def playPopEffect(self):
    if self.popEffect is not None:
      self.popEffect.play()

  @objc_method
  def preloadSoundEffect_(self, filename: str):
    file_path = Path(__file__).parent / filename
    if not file_path.exists():
      print(f"file {filename} not found")
      return None

    url = NSURL.fileURLWithPath_(str(file_path.absolute()))
    player = AVAudioPlayer.alloc().initWithContentsOfURL_error_(url, None)

    if player is not None:
      player.prepareToPlay()
      return player
    return None


# ★ ポイント2: クラス定義の直後で、'shared' をクラスプロパティとして強制的に登録する
SoundController.declare_class_property('shared')


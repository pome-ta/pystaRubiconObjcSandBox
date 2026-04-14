from pathlib import Path

from rbedge.utils import nsurl, get_str_filepath

from pyrubicon.objc.api import ObjCClass, NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super

AVAudioPlayer = ObjCClass('AVAudioPlayer')

ROOT_PATH = Path(__file__).parents[0]




# wip: 雑
def _get_filepath(file_name: str) -> str | None:
  root = ROOT_PATH.parents[1] / 'assets'
  return get_str_filepath(root, file_name)


def get_sound_path(soundName: str) -> str | None:
  return _get_filepath(soundName)


class SoundController(NSObject):

  _shared_instance: 'SoundController'

  backgroundMusicPlayer: 'AVAudioPlayer?' = objc_property()
  popEffect: 'AVAudioPlayer?' = objc_property()

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')

    return self

  @objc_method
  def preloadSoundEffect_(self, filename: object):
    if not (assetURL := get_sound_path(filename)):
      raise ValueError(f'Asset {filename} does not exist.')
    try:
      player = AVAudioPlayer.alloc().initWithContentsOfURL_error_(nsurl(assetURL), None)
    
    return None


from pathlib import Path
from pyrubicon.objc.api import ObjCClass

NSURL = ObjCClass('NSURL')


# ref: from objc_util.py of Pythonista3 module
def nsurl(url_or_path):
  if not isinstance(url_or_path, str):
    raise TypeError('expected a string')
  return NSURL.URLWithString_(
    url_or_path) if ':' in url_or_path else NSURL.fileURLWithPath_(url_or_path)


# wip: 雑
def get_str_filepath(dir_path: Path, file_name: str) -> str | None:
  for glob_path in dir_path.glob('./**'):
    for file in glob_path.iterdir():
      if file.name == file_name:
        return str(file.resolve())
  return None


def readonly_properties(*property_names):

  def wrapper(cls):
    for name in property_names:
      cls.declare_property(name)
    return cls

  return wrapper


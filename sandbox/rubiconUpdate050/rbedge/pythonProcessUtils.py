from pathlib import Path

from pyrubicon.objc.api import ObjCClass

NSData = ObjCClass('NSData')
NSURL = ObjCClass('NSURL')


def dataWithContentsOfURL(path_str: str | Path) -> NSData:
  path = path_str if isinstance(path_str, Path) else Path(path_str)
  # xxx: `try` 等でエラー確認したい
  return NSData.dataWithContentsOfURL_(
    NSURL.fileURLWithPath_(str(path.absolute())))


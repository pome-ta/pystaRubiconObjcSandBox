from pathlib import Path

from pyrubicon.objc.api import ObjCClass, NSData

NSURL = ObjCClass('NSURL')
UIScreen = ObjCClass('UIScreen')


def dataWithContentsOfURL(path_str: str | Path) -> NSData:
  """file path を`NSData` `(ObjCInstance)` で返す
  
  `UIImage(named: "")` 等、Bundle で呼ぶAssets をPython 側で取得
  Bundle 紐付けができないため、手動でpath を指定
  
  :param path_str: 取得するfile path
  :type path_str: str | Path
  :returns: `NSData` `(ObjCInstance)` の形式
  :rtype: NSData
  """
  path = path_str if isinstance(path_str, Path) else Path(path_str)
  # xxx: `try` 等でエラー確認したい
  return NSData.dataWithContentsOfURL_(
    NSURL.fileURLWithPath_(str(path.absolute())))


# ref: [iphone - Retina display and [UIImage initWithData] - Stack Overflow](https://stackoverflow.com/questions/3289286/retina-display-and-uiimage-initwithdata)
# xxx: scale 指定これでいいのかな?
"""デフォルトの論理的解像度に対する物理的解像度の比
"""
mainScreen_scale: float = UIScreen.mainScreen.scale


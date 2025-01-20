from pathlib import Path
import json

from pyrubicon.objc.api import ObjCClass, NSData
from .enumerations import UIUserInterfaceStyle

NSURL = ObjCClass('NSURL')
UIScreen = ObjCClass('UIScreen')

# ref: [iphone - Retina display and [UIImage initWithData] - Stack Overflow](https://stackoverflow.com/questions/3289286/retina-display-and-uiimage-initwithdata)
# xxx: scale 指定これでいいのかな?
"""デフォルトの論理的解像度に対する物理的解像度の比
"""
mainScreen_scale: float = UIScreen.mainScreen.scale


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


def get_srgb_named_style(named: str,
                         userInterfaceStyle: UIUserInterfaceStyle) -> list:
  # todo: 本来`UIColor.colorNamed:` で呼び出す。asset(bundle) の取り込みが難しそうなので、独自に直で呼び出し
  _path = Path(
    f'./UIKitCatalogCreatingAndCustomizingViewsAndControls/UIKitCatalog/Assets.xcassets/{named}.colorset/Contents.json'
  )
  _str = _path.read_text()
  _dict = json.loads(_str)

  def _pick_color(colors: list[dict], style: str | None = None) -> list:
    components: dict
    for color in colors:
      if color.get('idiom') != 'universal':
        continue
      appearance, *_ = appearances if (
        appearances := color.get('appearances')) is not None else [None]
      if style is None and appearance is None:
        components = color.get('color').get('components')
        break
      if appearance is not None and style == appearance.get('value'):
        components = color.get('color').get('components')
        break

    red, green, blue, alpha = (float(components.get(clr))
                               for clr in ('red', 'green', 'blue', 'alpha'))
    # wip: エラーハンドリング
    return [red, green, blue, alpha]

  color_dicts = _dict.get('colors')
  if userInterfaceStyle == UIUserInterfaceStyle.light:
    return _pick_color(color_dicts, 'light')
  elif userInterfaceStyle == UIUserInterfaceStyle.dark:
    return _pick_color(color_dicts, 'dark')
  else:
    return _pick_color(color_dicts)


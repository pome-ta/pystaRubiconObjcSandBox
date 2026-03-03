from pyrubicon.objc.api import ObjCClass

NSURL = ObjCClass('NSURL')

# ref: from objc_util.py of Pythonista3 module
def nsurl(url_or_path):
  if not isinstance(url_or_path, str):
    raise TypeError('expected a string')
  return NSURL.URLWithString_(
    url_or_path) if ':' in url_or_path else NSURL.fileURLWithPath_(url_or_path)

